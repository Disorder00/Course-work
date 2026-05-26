import argparse
import importlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler

from utils import ensure_dirs, save_cv_plot


RANDOM_STATE = 2026
N_SPLITS = 5


@dataclass
class ModelResult:
    name: str
    fold_scores: List[float]
    oof_pred: np.ndarray
    test_pred: np.ndarray

    @property
    def mean_score(self) -> float:
        return float(np.mean(self.fold_scores))

    @property
    def std_score(self) -> float:
        return float(np.std(self.fold_scores))


def optional_import(module_name: str) -> Any:
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None


def build_preprocessor(features: pd.DataFrame) -> ColumnTransformer:
    numeric_features = features.select_dtypes(include=["number"]).columns.tolist()
    categorical_features = [col for col in features.columns if col not in numeric_features]

    try:
        onehot = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        onehot = OneHotEncoder(handle_unknown="ignore", sparse=False)

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", RobustScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", onehot),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ]
    )


def get_models() -> Dict[str, object]:
    models: Dict[str, object] = {
        "ridge": Ridge(alpha=12.0, random_state=RANDOM_STATE),
        "random_forest": RandomForestRegressor(
            n_estimators=450,
            max_depth=18,
            min_samples_leaf=2,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
    }

    xgboost = optional_import("xgboost")
    if xgboost is not None:
        models["xgboost"] = xgboost.XGBRegressor(
            n_estimators=900,
            learning_rate=0.035,
            max_depth=3,
            subsample=0.85,
            colsample_bytree=0.75,
            reg_alpha=0.02,
            reg_lambda=1.2,
            objective="reg:squarederror",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )

    lightgbm = optional_import("lightgbm")
    if lightgbm is not None:
        models["lightgbm"] = lightgbm.LGBMRegressor(
            n_estimators=1100,
            learning_rate=0.03,
            num_leaves=31,
            feature_fraction=0.80,
            bagging_fraction=0.85,
            bagging_freq=1,
            min_child_samples=20,
            random_state=RANDOM_STATE,
            verbose=-1,
        )

    catboost = optional_import("catboost")
    if catboost is not None:
        models["catboost"] = catboost.CatBoostRegressor(
            iterations=900,
            learning_rate=0.035,
            depth=6,
            loss_function="RMSE",
            random_seed=RANDOM_STATE,
            verbose=False,
        )

    return models


def evaluate_model(
    name: str,
    model: object,
    x: pd.DataFrame,
    y_log: np.ndarray,
    x_test: pd.DataFrame,
) -> ModelResult:
    kfold = KFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    oof_pred = np.zeros(len(x))
    test_pred_folds = []
    fold_scores = []

    for fold, (train_idx, valid_idx) in enumerate(kfold.split(x), start=1):
        x_train, x_valid = x.iloc[train_idx], x.iloc[valid_idx]
        y_train, y_valid = y_log[train_idx], y_log[valid_idx]

        pipeline = Pipeline(
            steps=[
                ("preprocess", build_preprocessor(x_train)),
                ("model", model),
            ]
        )
        pipeline.fit(x_train, y_train)

        valid_pred = pipeline.predict(x_valid)
        test_pred = pipeline.predict(x_test)
        score = rmse(y_valid, valid_pred)

        oof_pred[valid_idx] = valid_pred
        test_pred_folds.append(test_pred)
        fold_scores.append(float(score))
        print(f"{name} fold {fold}: log RMSE={score:.5f}")

    return ModelResult(
        name=name,
        fold_scores=fold_scores,
        oof_pred=oof_pred,
        test_pred=np.mean(test_pred_folds, axis=0),
    )


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def make_ensemble(results: List[ModelResult], y_log: np.ndarray) -> ModelResult:
    # Better single models receive larger weights through inverse validation error.
    scores = np.array([r.mean_score for r in results])
    weights = 1 / np.maximum(scores, 1e-8)
    weights = weights / weights.sum()

    oof_pred = np.sum([w * r.oof_pred for w, r in zip(weights, results)], axis=0)
    test_pred = np.sum([w * r.test_pred for w, r in zip(weights, results)], axis=0)
    score = rmse(y_log, oof_pred)

    print("ensemble weights:")
    for result, weight in zip(results, weights):
        print(f"  {result.name}: {weight:.3f}")
    print(f"weighted_ensemble full OOF: log RMSE={score:.5f}")

    return ModelResult(
        name="weighted_ensemble",
        fold_scores=[float(score)],
        oof_pred=oof_pred,
        test_pred=test_pred,
    )


def load_data(train_path: Path, test_path: Path) -> Tuple[pd.DataFrame, np.ndarray, pd.DataFrame, pd.Series]:
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)

    if "SalePrice" not in train.columns:
        raise ValueError("train.csv must contain SalePrice.")
    if "Id" not in train.columns or "Id" not in test.columns:
        raise ValueError("Both train.csv and test.csv must contain Id.")

    y_log = np.log1p(train["SalePrice"].to_numpy())
    x = train.drop(columns=["SalePrice"])
    test_ids = test["Id"].copy()

    # Id is a row identifier, not a predictive feature.
    x = x.drop(columns=["Id"])
    x_test = test.drop(columns=["Id"])
    return x, y_log, x_test, test_ids


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", type=Path, default=Path("data/raw/train.csv"))
    parser.add_argument("--test", type=Path, default=Path("data/raw/test.csv"))
    args = parser.parse_args()

    ensure_dirs()
    x, y_log, x_test, test_ids = load_data(args.train, args.test)
    models = get_models()

    results = []
    for name, model in models.items():
        print(f"\n=== {name} ===")
        results.append(evaluate_model(name, model, x, y_log, x_test))

    if len(results) >= 2:
        results.append(make_ensemble(results, y_log))

    result_frame = pd.DataFrame(
        {
            "model": [r.name for r in results],
            "mean_log_rmse": [r.mean_score for r in results],
            "std_log_rmse": [r.std_score for r in results],
            "fold_scores": [";".join(f"{s:.5f}" for s in r.fold_scores) for r in results],
        }
    ).sort_values("mean_log_rmse")
    result_frame.to_csv("outputs/cv_results.csv", index=False)
    save_cv_plot(result_frame, "outputs/figures/cv_results.png")

    best = min(results, key=lambda r: r.mean_score)
    final_price_pred = np.expm1(best.test_pred)
    final_price_pred = np.maximum(final_price_pred, 0)

    submission = pd.DataFrame({"Id": test_ids, "SalePrice": final_price_pred})
    submission_path = Path("outputs/submissions/ensemble_submission.csv")
    submission.to_csv(submission_path, index=False)

    print("\nSaved results:")
    print("  outputs/cv_results.csv")
    print("  outputs/figures/cv_results.png")
    print(f"  {submission_path}")
    print(f"Best local model: {best.name}, log RMSE/RMSLE={best.mean_score:.5f}")


if __name__ == "__main__":
    main()
