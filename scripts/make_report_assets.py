from pathlib import Path
import os

import matplotlib

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "outputs" / ".matplotlib"))
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


RAW = ROOT / "data" / "raw"
OUT = ROOT / "reports" / "figures"


def save(path):
    plt.tight_layout()
    plt.savefig(path, dpi=220, bbox_inches="tight")
    plt.close()


def draw_box(ax, xy, text, width=0.23, height=0.12, color="#E8EEF5"):
    rect = plt.Rectangle(xy, width, height, facecolor=color, edgecolor="#2E74B5", linewidth=1.2)
    ax.add_patch(rect)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center", fontsize=9)


def draw_arrow(ax, start, end):
    ax.annotate("", xy=end, xytext=start, arrowprops=dict(arrowstyle="->", lw=1.2, color="#333333"))


def pipeline_diagram():
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.axis("off")
    boxes = [
        ((0.02, 0.55), "Kaggle\ntrain/test"),
        ((0.20, 0.55), "Missing value\nimputation"),
        ((0.38, 0.55), "One-hot\nencoding"),
        ((0.56, 0.55), "5-fold CV\ntraining"),
        ((0.74, 0.55), "RMSLE\ncomparison"),
        ((0.74, 0.22), "Kaggle\nsubmission"),
    ]
    for xy, text in boxes:
        draw_box(ax, xy, text)
    for x in [0.25, 0.43, 0.61]:
        draw_arrow(ax, (x, 0.61), (x + 0.10, 0.61))
    draw_arrow(ax, (0.79, 0.55), (0.79, 0.34))
    draw_arrow(ax, (0.79, 0.34), (0.79, 0.34))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    save(OUT / "pipeline_diagram.png")


def software_diagram():
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.axis("off")
    draw_box(ax, (0.05, 0.65), "data/raw\nKaggle data", 0.22, 0.13, "#F4F6F9")
    draw_box(ax, (0.39, 0.65), "src/train.py\nmodel training", 0.22, 0.13, "#E8EEF5")
    draw_box(ax, (0.73, 0.65), "outputs\nresults", 0.22, 0.13, "#F4F6F9")
    draw_box(ax, (0.39, 0.30), "scripts/build_report.py\nDOCX builder", 0.24, 0.13, "#E8EEF5")
    draw_box(ax, (0.73, 0.30), "reports\nfinal paper", 0.22, 0.13, "#F4F6F9")
    draw_arrow(ax, (0.27, 0.71), (0.39, 0.71))
    draw_arrow(ax, (0.61, 0.71), (0.73, 0.71))
    draw_arrow(ax, (0.84, 0.65), (0.51, 0.43))
    draw_arrow(ax, (0.63, 0.36), (0.73, 0.36))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    save(OUT / "software_structure.png")


def model_family_diagram():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis("off")
    draw_box(ax, (0.39, 0.78), "House price\nregression models", 0.25, 0.13, "#F2F4F7")
    branches = [
        ((0.05, 0.45), "Linear baseline\nRidge"),
        ((0.30, 0.45), "Bagging trees\nRandom Forest"),
        ((0.55, 0.45), "Boosting trees\nXGBoost/LightGBM/CatBoost"),
        ((0.78, 0.45), "Model fusion\nWeighted Ensemble"),
    ]
    for xy, text in branches:
        draw_box(ax, xy, text, 0.2, 0.14, "#E8EEF5")
        draw_arrow(ax, (0.515, 0.78), (xy[0] + 0.1, xy[1] + 0.14))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    save(OUT / "model_family.png")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    train = pd.read_csv(RAW / "train.csv")
    cv = pd.read_csv(ROOT / "outputs" / "cv_results.csv")

    sns.set_theme(style="whitegrid", font="DejaVu Sans")

    plt.figure(figsize=(8, 4.5))
    sns.histplot(train["SalePrice"], bins=35, kde=True, color="#3D6FB6")
    plt.title("SalePrice Distribution")
    plt.xlabel("SalePrice")
    save(OUT / "target_distribution.png")

    plt.figure(figsize=(8, 4.5))
    sns.histplot(np.log1p(train["SalePrice"]), bins=35, kde=True, color="#2F8F6B")
    plt.title("log1p(SalePrice) Distribution")
    plt.xlabel("log1p(SalePrice)")
    save(OUT / "log_target_distribution.png")

    missing = train.drop(columns=["SalePrice"]).isna().mean().sort_values(ascending=False).head(20)
    plt.figure(figsize=(8, 5))
    sns.barplot(x=missing.values * 100, y=missing.index, color="#C56B4A")
    plt.xlabel("Missing ratio (%)")
    plt.ylabel("Feature")
    plt.title("Top Missing Features")
    save(OUT / "missing_values.png")

    numeric = train.select_dtypes(include=[np.number])
    corr = numeric.corr(numeric_only=True)["SalePrice"].drop("SalePrice").abs().sort_values(ascending=False).head(15)
    plt.figure(figsize=(8, 5))
    sns.barplot(x=corr.values, y=corr.index, color="#3D6FB6")
    plt.xlabel("|Correlation with SalePrice|")
    plt.ylabel("Numeric feature")
    plt.title("Top Numeric Correlations")
    save(OUT / "correlation_top15.png")

    plt.figure(figsize=(7.5, 5))
    sns.scatterplot(data=train, x="GrLivArea", y="SalePrice", alpha=0.65, color="#3D6FB6", edgecolor=None)
    plt.title("GrLivArea vs SalePrice")
    save(OUT / "grlivarea_saleprice.png")

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=train, x="OverallQual", y="SalePrice", color="#E8EEF5")
    plt.title("OverallQual and SalePrice")
    save(OUT / "overallqual_box.png")

    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=train, x="YearBuilt", y="SalePrice", alpha=0.55, color="#2F8F6B", edgecolor=None)
    plt.title("YearBuilt vs SalePrice")
    save(OUT / "yearbuilt_saleprice.png")

    ordered = cv.sort_values("mean_log_rmse")
    plt.figure(figsize=(8, 4.5))
    sns.barplot(data=ordered, x="mean_log_rmse", y="model", color="#3D6FB6")
    plt.xlabel("Mean RMSLE")
    plt.ylabel("Model")
    plt.title("Cross-validation Performance")
    save(OUT / "model_comparison.png")

    fold_rows = []
    for _, row in cv.iterrows():
        scores = [float(x) for x in str(row["fold_scores"]).split(";") if x]
        if len(scores) > 1:
            for idx, score in enumerate(scores, start=1):
                fold_rows.append({"model": row["model"], "fold": idx, "RMSLE": score})
    fold_df = pd.DataFrame(fold_rows)
    plt.figure(figsize=(8.5, 5))
    sns.lineplot(data=fold_df, x="fold", y="RMSLE", hue="model", marker="o")
    plt.xticks([1, 2, 3, 4, 5])
    plt.title("Fold-wise Validation Scores")
    save(OUT / "fold_scores.png")

    pipeline_diagram()
    software_diagram()
    model_family_diagram()


if __name__ == "__main__":
    main()
