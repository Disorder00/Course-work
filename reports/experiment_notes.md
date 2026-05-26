# 实验记录

## 选题

Kaggle House Prices 房价预测竞赛。

## 评价指标

竞赛使用 RMSLE。本项目对 `SalePrice` 做 `log1p` 变换，因此在对数目标空间计算的 RMSE 与 RMSLE 等价，可作为本地交叉验证指标。

## 计划实验

| 类别 | 模型 | 目的 |
| --- | --- | --- |
| 基线模型 | Ridge Regression | 建立线性回归基准 |
| 基础集成 | Random Forest | 检验非线性树模型效果 |
| 扩展算法 | XGBoost | 梯度提升树代表方法 |
| 扩展算法 | LightGBM | 高效梯度提升树方法 |
| 扩展算法 | CatBoost | 类别特征友好的梯度提升树方法 |
| 模型融合 | Weighted Ensemble | 利用多模型互补性提升泛化性能 |

## 待填结果

运行 `python src/train.py --train data/raw/train.csv --test data/raw/test.csv` 后，将 `outputs/cv_results.csv` 的结果整理到课程报告。
