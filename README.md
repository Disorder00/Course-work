# 高级机器学习理论课程报告代码

## 题目

Kaggle 房价预测竞赛：基于梯度提升树与模型融合的房价回归预测

## 选题方向

扩展算法解决竞赛问题或实际问题。

## 问题简介

本项目基于 Kaggle 竞赛 **House Prices - Advanced Regression Techniques**。任务是根据房屋面积、质量、年份、地理位置、地下室、车库等结构化特征预测最终成交价 `SalePrice`。竞赛评价指标为 RMSLE，本项目在本地实验中使用对数房价空间下的 RMSE 作为等价交叉验证指标。

## 方法路线

项目从基础模型开始，逐步扩展到更强的集成学习算法：

- Ridge Regression：线性基线模型。
- Random Forest：Bagging 类树模型。
- XGBoost：二阶梯度提升树。
- LightGBM：基于直方图和叶子优先生长的梯度提升树。
- CatBoost：对类别变量处理更友好的梯度提升树。
- Weighted Ensemble：对多个强模型结果进行加权融合。

## 环境配置

建议使用 Python 3.10 或以上版本。

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

完整实验建议继续安装扩展模型依赖：

```bash
pip install -r requirements-extended.txt
```

## 数据准备

使用 Kaggle CLI 下载数据：

```bash
kaggle competitions download -c house-prices-advanced-regression-techniques -p data/raw
```

解压后确保：

```text
data/raw/train.csv
data/raw/test.csv
```

也可以从 Kaggle 页面手动下载后放入 `data/raw`。

## 运行实验

```bash
python src/train.py --train data/raw/train.csv --test data/raw/test.csv
```

快速功能测试可以使用仓库内置的小型样例：

```bash
python src/train.py --train data/sample/train_sample.csv --test data/sample/test_sample.csv
```

脚本会输出：

- `outputs/cv_results.csv`：各模型交叉验证结果。
- `outputs/submissions/best_model_submission.csv`：本地交叉验证最优模型的 Kaggle 提交文件。
- `outputs/submissions/weighted_ensemble_submission.csv`：加权融合模型的 Kaggle 提交文件。
- `outputs/figures/cv_results.png`：模型效果对比图。

## 项目结构

```text
.
├── data/
│   ├── raw/                 # Kaggle 原始数据，不提交到 Git
│   └── processed/
├── outputs/
│   ├── figures/             # 实验图表
│   └── submissions/         # 预测提交文件
├── reports/                 # 课程报告与实验记录
├── src/
│   ├── train.py             # 主训练与评估脚本
│   └── utils.py             # 指标、绘图和通用工具
├── requirements.txt
└── README.md
```

## 结果说明

完整实验结果将在运行脚本后自动保存，并在课程报告中整理为表格和图示。

## 生成课程报告

```bash
python scripts/build_report.py
```

报告文件会生成到：

```text
reports/高级机器学习理论课程报告_李小茹.docx
```
