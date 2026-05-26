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

## 正式实验结果

正式实验使用 Kaggle House Prices 原始训练集和测试集。训练集共 1460 条样本，测试集共 1459 条样本。本地评估采用 5 折交叉验证，在 `log1p(SalePrice)` 空间中计算 RMSE，该指标与 RMSLE 等价。

| 模型 | 平均 RMSLE | 标准差 | 说明 |
| --- | ---: | ---: | --- |
| CatBoost | 0.12029 | 0.00532 | 本地交叉验证最优模型 |
| XGBoost | 0.12039 | 0.00514 | 与 CatBoost 非常接近 |
| Weighted Ensemble | 0.12187 | 0.00000 | 加权融合略差于最优单模型 |
| LightGBM | 0.12817 | 0.00128 | 训练稳定，但本配置下低于 XGBoost/CatBoost |
| Random Forest | 0.14251 | 0.00580 | 基础树集成模型 |
| Ridge Regression | 0.14399 | 0.02627 | 线性基线模型 |

结论：梯度提升树模型整体优于线性基线和随机森林，其中 CatBoost 和 XGBoost 的效果最好。加权融合没有超过最优单模型，说明当前融合权重仍偏简单，后续可以尝试 Stacking、基于验证集的权重搜索或更细致的特征工程。
