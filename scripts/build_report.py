from pathlib import Path

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "高级机器学习理论课程报告_李小茹_扩展版.docx"
FIG_DIR = ROOT / "reports" / "figures"
GITHUB_URL = "https://github.com/Disorder00/Course-work"


def set_run_font(run, size=None, bold=None, italic=None, color=None, name="SimSun"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color is not None:
        run.font.color.rgb = RGBColor.from_string(color)


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell_width(cell, width_in):
    cell.width = Inches(width_in)
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_w = tc_pr.first_child_found_in("w:tcW")
    if tc_w is None:
        tc_w = OxmlElement("w:tcW")
        tc_pr.append(tc_w)
    tc_w.set(qn("w:w"), str(int(width_in * 1440)))
    tc_w.set(qn("w:type"), "dxa")


def set_cell_text(cell, text, bold=False, size=10, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.08
    run = p.add_run(str(text))
    set_run_font(run, size=size, bold=bold)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def paragraph(doc, text="", first_line=True, align=None, size=11, after=6):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.18
    if first_line:
        p.paragraph_format.first_line_indent = Inches(0.28)
    run = p.add_run(text)
    set_run_font(run, size=size)
    return p


def heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14 if level == 1 else 9)
    p.paragraph_format.space_after = Pt(7 if level == 1 else 5)
    run = p.add_run(text)
    if level == 1:
        set_run_font(run, size=15, bold=True, color="2E74B5")
    elif level == 2:
        set_run_font(run, size=13, bold=True, color="2E74B5")
    else:
        set_run_font(run, size=12, bold=True, color="1F4D78")
    return p


def caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    set_run_font(run, size=10, bold=True)


def add_figure(doc, filename, cap, width=5.8):
    path = FIG_DIR / filename
    if not path.exists():
        paragraph(doc, f"[图缺失：{filename}]", first_line=False)
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(str(path), width=Inches(width))
    caption(doc, cap)


def table(doc, headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        set_cell_text(t.rows[0].cells[i], h, bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_shading(t.rows[0].cells[i], "F2F4F7")
        if widths:
            set_cell_width(t.rows[0].cells[i], widths[i])
    for row in rows:
        cells = t.add_row().cells
        for i, item in enumerate(row):
            align = WD_ALIGN_PARAGRAPH.CENTER if i < 3 else WD_ALIGN_PARAGRAPH.LEFT
            set_cell_text(cells[i], item, size=9.5, align=align)
            if widths:
                set_cell_width(cells[i], widths[i])
    doc.add_paragraph()
    return t


def setup(doc):
    sec = doc.sections[0]
    sec.top_margin = Inches(1)
    sec.bottom_margin = Inches(1)
    sec.left_margin = Inches(1)
    sec.right_margin = Inches(1)
    sec.header_distance = Inches(0.492)
    sec.footer_distance = Inches(0.492)
    normal = doc.styles["Normal"]
    normal.font.name = "SimSun"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")
    normal.font.size = Pt(11)
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = footer.add_run("高级机器学习理论课程报告")
    set_run_font(r, size=9, color="555555")


def cover(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(56)
    r = p.add_run("研究生“高级机器学习理论”课程报告")
    set_run_font(r, size=22, bold=True)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(30)
    r = p.add_run("题 目：基于梯度提升树与模型融合的Kaggle房价预测研究")
    set_run_font(r, size=16, bold=True)

    paragraph(doc, "选题方向：", first_line=False, size=12)
    for item in [
        "□ 三个以上的基础算法解决经典的仿真问题",
        "☑ 扩展算法解决竞赛问题或实际问题",
        "□ 提出了创新性的算法思路解决实际问题",
    ]:
        p = paragraph(doc, item, first_line=False, size=12)
        p.paragraph_format.left_indent = Inches(1.1)

    rows = [
        ("学号", "Y202502064"),
        ("姓名", "李小茹"),
        ("专业", "计算机科学与技术"),
        ("课程指导教师", "伍东睿、朱力军、程骋"),
        ("院（系、所）", "研究生院"),
        ("日期", "2026年5月26日"),
    ]
    t = doc.add_table(rows=0, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for k, v in rows:
        cells = t.add_row().cells
        set_cell_text(cells[0], k, bold=True, size=12, align=WD_ALIGN_PARAGRAPH.RIGHT)
        set_cell_text(cells[1], v, size=12)
        set_cell_width(cells[0], 1.8)
        set_cell_width(cells[1], 3.9)
    doc.add_page_break()


def title_block(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("基于梯度提升树与模型融合的Kaggle房价预测研究")
    set_run_font(r, size=16, bold=True)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("李小茹")
    set_run_font(r, size=11)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("（研究生院，计算机科学与技术）")
    set_run_font(r, size=11)


def abstract(doc):
    title_block(doc)
    paragraph(
        doc,
        "摘要：房价预测是结构化表格数据建模中的典型回归任务。本文以 Kaggle House Prices - Advanced Regression Techniques 竞赛为研究对象，围绕包含数值变量、类别变量、缺失值和非线性特征交互的住宅成交价预测问题，构建了从基线模型到扩展集成算法的完整机器学习实验流程。研究首先对房价分布、缺失特征、关键数值变量相关性以及代表性房屋属性进行探索性分析；随后以 Ridge Regression 和 Random Forest 作为基线，进一步引入 XGBoost、LightGBM、CatBoost 三类具有代表性的梯度提升树算法，并实现基于验证误差倒数的加权融合方法。实验采用 5 折交叉验证，在 log1p(SalePrice) 目标空间中计算 RMSE，作为 Kaggle RMSLE 指标的本地等价形式。结果表明，梯度提升树模型显著优于线性基线和随机森林，其中 CatBoost 取得最优本地 RMSLE 0.12029，XGBoost 以 0.12039 紧随其后；将 CatBoost 最优模型提交至 Kaggle 后，Public Score 为 0.12481，与本地验证结果较为一致。本文进一步从模型机制、数据特征、融合失败原因、泛化误差和后续改进方向等方面进行分析，说明梯度提升树仍是中小规模结构化竞赛任务中的强基线与有效扩展算法。",
        first_line=False,
    )
    paragraph(doc, "关键词：机器学习；房价预测；结构化数据；梯度提升树；CatBoost；Kaggle", first_line=False)
    doc.add_page_break()


def body(doc):
    heading(doc, "1 引言", 1)
    paragraph(doc, "随着城市化发展和房地产市场交易数据的积累，基于机器学习的房价预测逐渐成为数据挖掘、金融风控和智能评估中的重要问题。房屋价格并非由单一变量决定，而是受到建筑面积、整体质量、地段、楼龄、装修状态、地下室、车库、社区属性等多重因素共同影响。这类数据具有变量类型混合、缺失模式复杂、特征间非线性关系明显、异常样本存在等特点，因此适合作为高级机器学习课程中的综合实验对象。")
    paragraph(doc, "Kaggle House Prices 竞赛提供了一个较为规范的公开基准。训练集包含 1460 条住宅样本，测试集包含 1459 条样本，特征数量接近 80 个，目标变量为 SalePrice。竞赛评价指标 RMSLE 关注预测值与真实值的相对比例误差，对高价房和低价房具有更均衡的惩罚效果。与单纯追求线上分数不同，本文更加关注模型选择、算法机制、实验设计和结果解释，目标是形成一份可复现、可分析、可扩展的课程实验报告。")
    paragraph(doc, "本文的主要工作包括四点。第一，完成数据探索和可视化分析，解释为什么需要对房价进行对数变换。第二，比较线性模型、Bagging 树模型和 Boosting 树模型在同一任务上的差异。第三，构建自动化训练脚本，实现数据读取、预处理、5 折交叉验证、模型融合、图表保存和 Kaggle 提交文件生成。第四，将本地验证结果与 Kaggle 线上 Public Score 对照，分析本地验证策略的可靠性。")

    heading(doc, "2 相关工作", 1)
    paragraph(doc, "梯度提升树是结构化数据建模中最成功的算法族之一。Friedman 提出的 Gradient Boosting Machine 将弱学习器按加法模型逐步组合，通过拟合损失函数的负梯度来降低经验风险。Chen 和 Guestrin 提出的 XGBoost 在目标函数中显式引入正则化项，并使用二阶泰勒展开近似损失，使分裂增益计算更精确，成为大量 Kaggle 竞赛中的强力基线。")
    paragraph(doc, "LightGBM 针对大规模特征和样本训练效率进行了优化，采用基于直方图的分裂查找、叶子优先生长策略、互斥特征捆绑和基于梯度的单边采样，在保持模型精度的同时提高训练速度。CatBoost 则重点解决类别特征处理和预测偏移问题，通过有序目标统计和有序提升机制降低目标泄露风险，对类别变量较多的表格数据具有良好适应性。")
    paragraph(doc, "近年来，深度学习在视觉、语音和自然语言处理领域取得巨大成功，但在中小规模表格数据上，树模型仍然经常优于深度神经网络。Grinsztajn 等研究指出，在不进行大规模预训练的条件下，基于树的模型在许多真实表格任务上仍具优势。Borisov 等综述也表明，表格数据中的异质变量、稀疏类别和非平滑决策边界使得梯度提升树依然具有很强竞争力。因此，本文选择梯度提升树作为扩展算法，符合当前结构化数据建模的主流实践。")
    add_figure(doc, "model_family.png", "图 1 本文比较的模型族及其关系")

    heading(doc, "3 问题定义与评价指标", 1)
    paragraph(doc, "给定训练集 D={(xi, yi)}，其中 xi 表示第 i 套房屋的特征向量，yi 表示成交价格。模型学习函数 f，使得预测值 f(xi) 尽可能接近真实房价 yi。由于房价为正且分布右偏，本文对目标变量进行 z=log(1+y) 变换。模型在 z 空间中训练，预测时再通过 y_hat=exp(z_hat)-1 还原到原始价格空间。")
    paragraph(doc, "Kaggle 使用 RMSLE 作为评价指标。其形式可以理解为真实价格与预测价格取 log1p 后的均方根误差。该指标相比 RMSE 更关注相对误差，能够避免高价样本对损失函数的绝对主导。由于本文直接在 log1p(SalePrice) 空间计算 RMSE，因此本地交叉验证指标与 RMSLE 等价。")
    table(doc, ["符号", "含义", "本文设置", "说明"], [
        ("xi", "第 i 个样本特征", "房屋属性向量", "包含数值和类别变量"),
        ("yi", "真实房价", "SalePrice", "训练集目标变量"),
        ("zi", "对数目标", "log1p(SalePrice)", "缓解右偏分布"),
        ("K", "交叉验证折数", "5", "平衡评估稳定性和计算成本"),
        ("RMSLE", "评价指标", "log 空间 RMSE", "与 Kaggle 指标一致"),
    ], widths=[0.8, 1.4, 1.7, 2.5])

    heading(doc, "4 数据集与探索性分析", 1)
    paragraph(doc, "House Prices 数据集来自 Ames 房价数据的竞赛化版本，变量覆盖住宅建筑、位置、质量、空间、地下室、车库和交易时间等方面。训练集有 1460 条样本，测试集有 1459 条样本。该数据规模不大，但变量类型丰富，适合比较不同机器学习算法在结构化数据上的表现。")
    add_figure(doc, "target_distribution.png", "图 2 SalePrice 原始分布")
    paragraph(doc, "图 2 表明 SalePrice 呈明显右偏分布，少数高价房屋会拉大原始价格空间中的误差。若直接使用 RMSE，模型可能更加关注高价样本的绝对误差，而忽略普通价位房屋的相对误差。因此本文采用 log1p 变换，与竞赛 RMSLE 指标保持一致。")
    add_figure(doc, "log_target_distribution.png", "图 3 log1p(SalePrice) 分布")
    paragraph(doc, "经过 log1p 变换后，目标变量分布更加接近对称形态。这有助于线性模型满足误差分布假设，也能使树模型在训练时更稳定。虽然梯度提升树并不要求目标变量严格服从正态分布，但更平滑的目标空间往往有利于泛化。")
    add_figure(doc, "missing_values.png", "图 4 缺失率最高的特征")
    paragraph(doc, "缺失值是本数据集的重要特征。部分变量的缺失并不一定表示信息丢失，而可能表示“没有该设施”，例如 PoolQC 缺失通常表示没有泳池，Alley 缺失可能表示没有巷道入口。因此，报告中的程序采用通用策略：数值变量用中位数填补，类别变量用众数填补；在后续改进中，可以进一步针对语义型缺失构造显式类别。")
    add_figure(doc, "correlation_top15.png", "图 5 与 SalePrice 相关性最高的数值特征")
    paragraph(doc, "数值相关性分析显示，OverallQual、GrLivArea、GarageCars、GarageArea、TotalBsmtSF 等变量与房价高度相关。这符合经验：房屋整体质量、居住面积、车库容量和地下室面积通常显著影响成交价。但相关性只能刻画线性关系，无法反映类别变量和高阶交互，因此仍需使用更强的非线性模型。")
    add_figure(doc, "overallqual_box.png", "图 6 OverallQual 与 SalePrice 的关系")
    add_figure(doc, "grlivarea_saleprice.png", "图 7 GrLivArea 与 SalePrice 的散点关系")
    add_figure(doc, "yearbuilt_saleprice.png", "图 8 YearBuilt 与 SalePrice 的关系")
    paragraph(doc, "图 6 至图 8 展示了关键变量与房价的关系。OverallQual 与房价呈明显单调关系，说明质量评分是强预测因子；GrLivArea 与房价总体正相关，但存在少量大面积低价异常点；YearBuilt 与房价也存在趋势，新房整体价格较高，但不同年代房屋的价格分散程度较大。这些现象说明模型既需要学习主效应，也需要处理异常样本和变量交互。")

    heading(doc, "5 算法原理", 1)
    heading(doc, "5.1 Ridge Regression", 2)
    paragraph(doc, "Ridge Regression 是加入 L2 正则化的线性回归。其目标函数由平方误差项和权重平方惩罚项组成。L2 正则化可以抑制过大的系数，在特征相关性较强时提高模型稳定性。本文将 Ridge 作为线性基线，用于衡量非线性集成模型的提升幅度。")
    heading(doc, "5.2 Random Forest", 2)
    paragraph(doc, "Random Forest 通过 Bootstrap 采样构造多棵决策树，并在每个节点随机选择部分特征进行分裂，最终对所有树的预测结果取平均。该方法降低了单棵树的方差，能够捕捉非线性关系，但每棵树独立训练，不能像 Boosting 一样逐步修正前一轮残差。")
    heading(doc, "5.3 XGBoost", 2)
    paragraph(doc, "XGBoost 将模型表示为若干回归树的加法组合。每一轮新增一棵树，用于拟合当前模型的残差方向。其核心特点包括二阶梯度近似、正则化复杂度惩罚、列采样、行采样和缺失值默认方向学习。这些机制使 XGBoost 在保证精度的同时具有较强的泛化能力。")
    heading(doc, "5.4 LightGBM", 2)
    paragraph(doc, "LightGBM 使用直方图近似连续特征分裂点，大幅降低分裂搜索成本。其叶子优先生长策略每次选择增益最大的叶子继续分裂，理论上能更快降低训练误差。但如果数据规模较小或参数控制不足，该策略也可能带来过拟合风险，因此需要配合叶子数、最小样本数和采样参数。")
    heading(doc, "5.5 CatBoost", 2)
    paragraph(doc, "CatBoost 的优势在于类别特征处理和有序提升。传统目标编码容易引入目标泄露，即某个样本的标签信息被编码进自身特征。CatBoost 通过随机排列和有序统计降低这种偏差，并通过对称树结构提高推理效率。虽然本文预处理阶段使用了统一独热编码，但 CatBoost 的 Boosting 机制仍表现出很强竞争力。")
    heading(doc, "5.6 加权融合", 2)
    paragraph(doc, "加权融合将多个模型的预测结果按权重线性组合。本文使用验证误差倒数确定权重，即验证误差越低的模型权重越高。该方法简单透明，但未必最优，因为不同模型之间可能高度相关，简单加权无法保证误差互补。实验结果也显示，当前加权融合略差于最优 CatBoost 单模型。")

    heading(doc, "6 软件结构与复现流程", 1)
    paragraph(doc, f"本文代码仓库地址为 {GITHUB_URL}。仓库给出了环境配置、数据下载方式、样例数据、训练脚本、报告生成脚本和实验记录。为了保证可复现性，代码固定随机种子为 2026，使用相同的 5 折划分比较所有模型。")
    add_figure(doc, "software_structure.png", "图 9 项目软件结构")
    add_figure(doc, "pipeline_diagram.png", "图 10 实验流水线")
    table(doc, ["模块", "文件或目录", "功能", "复现作用"], [
        ("数据", "data/raw", "存放 Kaggle train.csv 与 test.csv", "提供正式实验输入"),
        ("样例", "data/sample", "小型 CSV 样例", "无 Kaggle 数据时测试程序"),
        ("训练", "src/train.py", "模型训练、交叉验证和提交文件生成", "核心实验入口"),
        ("工具", "src/utils.py", "目录创建和绘图函数", "减少重复逻辑"),
        ("图表", "scripts/make_report_assets.py", "生成 EDA 和论文图", "支撑报告分析"),
        ("报告", "scripts/build_report.py", "生成 Word 报告", "复现实验文档"),
    ], widths=[0.8, 1.55, 2.1, 2.0])

    heading(doc, "7 实验设计", 1)
    paragraph(doc, "实验在相同训练集上比较六类模型。预处理流程包括：删除 Id 标识符；对数值变量使用中位数填补；对类别变量使用众数填补；对类别变量进行独热编码；对目标变量 SalePrice 进行 log1p 变换。所有模型均在相同的 5 折交叉验证划分上评估。")
    table(doc, ["模型", "类别", "关键设置", "实验目的"], [
        ("Ridge", "线性模型", "alpha=12.0", "建立线性基线"),
        ("Random Forest", "Bagging 树", "450 棵树，最大深度 18", "检验基础非线性集成"),
        ("XGBoost", "Boosting 树", "900 轮，学习率 0.035，深度 3", "检验强梯度提升树"),
        ("LightGBM", "Boosting 树", "1100 轮，学习率 0.03，num_leaves=31", "检验高效 GBDT"),
        ("CatBoost", "Boosting 树", "900 轮，学习率 0.035，深度 6", "检验类别友好提升树"),
        ("Weighted Ensemble", "融合模型", "误差倒数加权", "检验模型互补性"),
    ], widths=[1.25, 1.1, 2.35, 1.75])
    paragraph(doc, "由于课程报告强调算法比较和实验分析，本文没有进行大规模自动超参数搜索，而采用较稳定的经验参数。这样做的好处是实验流程清晰、计算成本可控；不足是线上成绩仍有进一步提升空间。")

    heading(doc, "8 实验结果与分析", 1)
    paragraph(doc, "表 5 给出了各模型在 5 折交叉验证中的平均 RMSLE 和标准差。结果表明，CatBoost、XGBoost 和 LightGBM 均显著优于 Ridge 与 Random Forest，说明 Boosting 机制对于本任务的非线性拟合和误差修正更加有效。")
    table(doc, ["模型", "平均 RMSLE", "标准差", "分析"], [
        ("CatBoost", "0.12029", "0.00532", "最优单模型，泛化稳定"),
        ("XGBoost", "0.12039", "0.00514", "与 CatBoost 几乎持平"),
        ("Weighted Ensemble", "0.12187", "0.00000", "简单融合未超过最优单模型"),
        ("LightGBM", "0.12817", "0.00128", "稳定但精度略低"),
        ("Random Forest", "0.14251", "0.00580", "优于部分线性折，但整体不足"),
        ("Ridge Regression", "0.14399", "0.02627", "线性假设限制明显"),
    ], widths=[1.45, 1.1, 1.0, 2.9])
    add_figure(doc, "model_comparison.png", "图 11 各模型交叉验证平均 RMSLE 对比")
    add_figure(doc, "fold_scores.png", "图 12 各模型分折验证结果")
    paragraph(doc, "从平均结果看，CatBoost 与 XGBoost 的差异仅为 0.00010，说明两者在该数据集上的预测能力非常接近。LightGBM 的标准差最小，说明其分折表现较稳定，但平均误差高于 CatBoost 和 XGBoost。Ridge 在第二折上误差明显偏高，表明线性模型对数据划分较敏感。")
    paragraph(doc, "Random Forest 的表现低于 Boosting 模型，原因可能在于房价预测任务需要逐步修正残差中的细粒度模式，而 Random Forest 的树之间相互独立，主要通过降低方差提升稳定性，对偏差的降低不如梯度提升树明显。")
    paragraph(doc, "加权融合结果为 0.12187，未超过 CatBoost。理论上，融合只有在模型误差具有互补性时才能稳定提升；若强模型已经学习到相似模式，简单平均反而可能引入弱模型误差。本文使用的误差倒数权重较简单，未对融合权重进行优化，因此该结果是合理的。")

    heading(doc, "9 Kaggle 线上评测", 1)
    paragraph(doc, "本文将本地交叉验证最优的 CatBoost 模型用于生成测试集预测文件 best_model_submission.csv，并提交至 Kaggle。线上 Public Score 为 0.12481。本地 5 折验证 RMSLE 为 0.12029，两者差距约 0.00452，说明本地验证与线上测试分布基本一致，没有出现严重过拟合。")
    table(doc, ["提交文件", "本地模型", "本地 RMSLE", "Kaggle Public Score"], [
        ("best_model_submission.csv", "CatBoost", "0.12029", "0.12481"),
    ], widths=[2.0, 1.3, 1.3, 1.8])
    paragraph(doc, "从竞赛实践角度看，Public Score 只能反映测试集公开部分的表现，并不能完全代表最终 Private Score。因此报告中更重视本地交叉验证的稳定性。若要进一步提升线上成绩，应避免反复根据 Public Score 调参，以免对公开榜单过拟合。")

    heading(doc, "10 消融与误差讨论", 1)
    paragraph(doc, "虽然本文没有进行逐特征消融实验，但从模型族对比可获得若干结论。第一，log1p 目标变换是必要的，因为它使目标分布更平滑，也与 RMSLE 指标一致。第二，Boosting 模型显著优于 Ridge 和 Random Forest，说明逐轮残差修正比单纯线性拟合或 Bagging 平均更适合该任务。第三，CatBoost 和 XGBoost 的结果非常接近，说明当前性能瓶颈可能不在模型类别，而在特征工程和参数搜索。")
    paragraph(doc, "误差来源可能包括四类。其一，部分变量存在语义型缺失，统一填补策略没有充分利用“缺失本身就是信息”的性质。其二，异常样本可能影响模型对面积和价格关系的学习。其三，类别变量独热编码会产生较高维稀疏特征，可能削弱某些模型对类别统计信息的利用。其四，模型参数主要来自经验设置，尚未通过系统搜索达到最优。")
    paragraph(doc, "针对这些问题，后续可加入总面积特征、房龄特征、翻修间隔、质量面积交互、社区均价统计等人工特征；也可在交叉验证内进行贝叶斯优化或随机搜索；融合方面可以使用 Stacking，让二层模型基于 out-of-fold 预测学习最优组合，而不是手工设定权重。")

    heading(doc, "11 与 SCI 论文规范的对照", 1)
    paragraph(doc, "按照 SCI 论文常见结构，本文包含问题背景、相关工作、方法、实验设置、数据说明、结果分析、讨论、局限性和参考文献。与正式 SCI 论文相比，本文仍属于课程报告，创新点主要体现在对竞赛问题的工程化复现和扩展算法比较，而不是提出全新算法。")
    paragraph(doc, "为了增强论文式表达，报告中尽量避免只给出“跑分结果”，而是解释指标选择、算法机制、分布特征和误差来源。实验部分同时报告本地交叉验证和 Kaggle 线上成绩，能够体现模型选择与外部评测之间的一致性。")

    heading(doc, "12 局限性与未来工作", 1)
    paragraph(doc, "本文存在以下局限。第一，特征工程仍然较基础，没有针对每个变量的业务语义进行细粒度处理。第二，超参数搜索范围有限，无法保证各模型均达到最优状态。第三，融合方法较简单，没有使用 Stacking、Blending 或基于验证集优化的权重学习。第四，报告没有使用 Private Score，因此线上泛化结论仍需谨慎。")
    paragraph(doc, "未来工作可从三个方向展开。首先，构建更丰富的特征体系，例如 TotalSF、HouseAge、RemodAge、QualArea、HasPool、HasGarage 等。其次，引入 Optuna 等自动调参工具，对树深、学习率、叶子数、正则化和采样率进行系统搜索。最后，使用分层交叉验证、异常值鲁棒处理和 Stacking 融合，以进一步提高成绩和稳定性。")

    heading(doc, "13 总结", 1)
    paragraph(doc, "本文以 Kaggle House Prices 房价预测竞赛为对象，完成了扩展算法解决竞赛问题的完整实验。通过数据探索、模型训练、交叉验证、线上提交和误差分析，证明梯度提升树在中小规模结构化回归任务上具有明显优势。CatBoost 取得本地 RMSLE 0.12029 和 Kaggle Public Score 0.12481，是本文最优模型。")
    paragraph(doc, "从课程学习角度看，本实验不仅比较了不同算法的性能，也体现了机器学习项目的完整流程：问题定义、数据理解、算法选择、软件实现、实验验证、结果解释和复现提交。这些环节共同构成了机器学习理论与实践之间的桥梁。")

    heading(doc, "参考文献", 1)
    refs = [
        "[1] Kaggle. House Prices - Advanced Regression Techniques[EB/OL]. https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques.",
        "[2] De Cock D. Ames, Iowa: Alternative to the Boston Housing Data as an End of Semester Regression Project[J]. Journal of Statistics Education, 2011, 19(3).",
        "[3] Friedman J H. Greedy Function Approximation: A Gradient Boosting Machine[J]. The Annals of Statistics, 2001, 29(5):1189-1232.",
        "[4] Breiman L. Random Forests[J]. Machine Learning, 2001, 45:5-32.",
        "[5] Hoerl A E, Kennard R W. Ridge Regression: Biased Estimation for Nonorthogonal Problems[J]. Technometrics, 1970, 12(1):55-67.",
        "[6] Chen T, Guestrin C. XGBoost: A Scalable Tree Boosting System[C]. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2016:785-794.",
        "[7] Ke G, Meng Q, Finley T, et al. LightGBM: A Highly Efficient Gradient Boosting Decision Tree[C]. Advances in Neural Information Processing Systems, 2017.",
        "[8] Prokhorenkova L, Gusev G, Vorobev A, Dorogush A V, Gulin A. CatBoost: unbiased boosting with categorical features[C]. Advances in Neural Information Processing Systems, 2018.",
        "[9] Dorogush A V, Ershov V, Gulin A. CatBoost: gradient boosting with categorical features support[EB/OL]. arXiv:1810.11363, 2018.",
        "[10] Grinsztajn L, Oyallon E, Varoquaux G. Why do tree-based models still outperform deep learning on tabular data?[C]. Advances in Neural Information Processing Systems, 2022.",
        "[11] Borisov V, Leemann T, Seßler K, Haug J, Pawelczyk M, Kasneci G. Deep Neural Networks and Tabular Data: A Survey[J]. IEEE Transactions on Neural Networks and Learning Systems, 2022.",
        "[12] Shwartz-Ziv R, Armon A. Tabular Data: Deep Learning is Not All You Need[J]. Information Fusion, 2022, 81:84-90.",
        "[13] Gorishniy Y, Rubachev I, Khrulkov V, Babenko A. Revisiting Deep Learning Models for Tabular Data[C]. Advances in Neural Information Processing Systems, 2021.",
        "[14] Hancock J T, Khoshgoftaar T M. CatBoost for big data: an interdisciplinary review[J]. Journal of Big Data, 2020, 7:94.",
        "[15] Hastie T, Tibshirani R, Friedman J. The Elements of Statistical Learning[M]. Springer, 2009.",
        "[16] Kuhn M, Johnson K. Applied Predictive Modeling[M]. Springer, 2013.",
        "[17] Pedregosa F, Varoquaux G, Gramfort A, et al. Scikit-learn: Machine Learning in Python[J]. Journal of Machine Learning Research, 2011, 12:2825-2830.",
        "[18] Hunter J D. Matplotlib: A 2D Graphics Environment[J]. Computing in Science & Engineering, 2007, 9(3):90-95.",
    ]
    for ref in refs:
        paragraph(doc, ref, first_line=False, size=10, after=4)

    heading(doc, "附录 A 代码运行说明", 1)
    paragraph(doc, "1. 创建环境并安装依赖：python -m venv .venv；pip install -r requirements-extended.txt。")
    paragraph(doc, "2. 下载数据：kaggle competitions download -c house-prices-advanced-regression-techniques -p data/raw，并解压得到 train.csv 和 test.csv。")
    paragraph(doc, "3. 运行实验：python src/train.py --train data/raw/train.csv --test data/raw/test.csv。")
    paragraph(doc, "4. 生成图表：python scripts/make_report_assets.py。")
    paragraph(doc, "5. 生成报告：python scripts/build_report.py。")
    paragraph(doc, f"6. 代码仓库：{GITHUB_URL}。")

    heading(doc, "附录 B 程序输出文件", 1)
    table(doc, ["输出文件", "内容", "是否提交 Git", "用途"], [
        ("outputs/cv_results.csv", "模型交叉验证结果", "否", "报告表格来源"),
        ("outputs/figures/cv_results.png", "模型对比图", "否", "快速查看结果"),
        ("outputs/submissions/best_model_submission.csv", "CatBoost 提交文件", "否", "Kaggle 线上提交"),
        ("outputs/submissions/weighted_ensemble_submission.csv", "融合模型提交文件", "否", "对比融合效果"),
        ("reports/figures/*.png", "报告图表", "是", "支撑论文式分析"),
        ("reports/高级机器学习理论课程报告_李小茹_扩展版.docx", "最终报告", "是", "课程提交材料"),
    ], widths=[2.2, 1.7, 1.0, 1.5])


def main():
    doc = Document()
    setup(doc)
    cover(doc)
    abstract(doc)
    body(doc)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
