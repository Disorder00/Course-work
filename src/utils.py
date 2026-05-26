import os
from pathlib import Path
from typing import Union

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", str(Path("outputs/.matplotlib").resolve()))

import matplotlib.pyplot as plt
import pandas as pd


def rmsle_from_log_rmse(log_rmse: float) -> float:
    """For log1p-transformed targets, RMSE in log space is RMSLE."""
    return float(log_rmse)


def ensure_dirs() -> None:
    Path("outputs").mkdir(exist_ok=True)
    Path("outputs/figures").mkdir(parents=True, exist_ok=True)
    Path("outputs/submissions").mkdir(parents=True, exist_ok=True)


def save_cv_plot(results: pd.DataFrame, path: Union[str, Path]) -> None:
    ordered = results.sort_values("mean_log_rmse")
    plt.figure(figsize=(9, 5))
    bars = plt.barh(ordered["model"], ordered["mean_log_rmse"], color="#3D6FB6")
    plt.xlabel("5-fold CV log RMSE / RMSLE")
    plt.ylabel("Model")
    plt.title("Model Comparison on House Prices")
    plt.grid(axis="x", alpha=0.25)

    for bar, value in zip(bars, ordered["mean_log_rmse"]):
        plt.text(
            value + 0.001,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.5f}",
            va="center",
            fontsize=9,
        )

    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
