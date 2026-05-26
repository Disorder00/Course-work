from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "高级机器学习理论课程报告_李小茹.docx"
FIG = ROOT / "outputs" / "figures" / "cv_results.png"
GITHUB_URL = "https://github.com/Disorder00/Course-work"


def set_run_font(run, size=None, bold=None, color=None, name="SimSun"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run._element.rPr.rFonts.set(qn("w:ascii"), "Calibri")
    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Calibri")
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color is not None:
        run.font.color.rgb = RGBColor.from_string(color)


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell_text(cell, text, bold=False, size=10.5, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def set_cell_width(cell, width_in):
    cell.width = Inches(width_in)
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_w = tc_pr.first_child_found_in("w:tcW")
    if tc_w is None:
        tc_w = OxmlElement("w:tcW")
        tc_pr.append(tc_w)
    tc_w.set(qn("w:w"), str(int(width_in * 1440)))
    tc_w.set(qn("w:type"), "dxa")


def add_paragraph(doc, text="", style=None, align=None, first_line=True):
    p = doc.add_paragraph(style=style)
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.1
    if first_line:
        p.paragraph_format.first_line_indent = Inches(0.28)
    run = p.add_run(text)
    set_run_font(run, size=11)
    return p


def add_heading(doc, text, level=1):
    p = doc.add_heading(level=level)
    p.paragraph_format.space_before = Pt(12 if level == 1 else 8)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    set_run_font(run, size=16 if level == 1 else 13, bold=True, color="2E74B5")
    return p


def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    hdr_cells = table.rows[0].cells
    for idx, header in enumerate(headers):
        set_cell_text(hdr_cells[idx], header, bold=True, size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_shading(hdr_cells[idx], "F2F4F7")
        if widths:
            set_cell_width(hdr_cells[idx], widths[idx])
    for row in rows:
        cells = table.add_row().cells
        for idx, value in enumerate(row):
            align = WD_ALIGN_PARAGRAPH.CENTER if idx != len(row) - 1 else WD_ALIGN_PARAGRAPH.LEFT
            set_cell_text(cells[idx], str(value), size=10, align=align)
            if widths:
                set_cell_width(cells[idx], widths[idx])
    doc.add_paragraph()
    return table


def setup_styles(doc):
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)

    normal = doc.styles["Normal"]
    normal.font.name = "SimSun"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")
    normal.font.size = Pt(11)

    for style_name in ["Heading 1", "Heading 2", "Heading 3"]:
        style = doc.styles[style_name]
        style.font.name = "SimSun"
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")
        style.font.color.rgb = RGBColor(46, 116, 181)
        style.font.bold = True


def add_cover(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(48)
    r = p.add_run("研究生“高级机器学习理论”课程报告")
    set_run_font(r, size=20, bold=True)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(28)
    r = p.add_run("题 目：基于梯度提升树与模型融合的Kaggle房价预测研究")
    set_run_font(r, size=16, bold=True)

    choices = [
        "□ 三个以上的基础算法解决经典的仿真问题",
        "☑ 扩展算法解决竞赛问题或实际问题",
        "□ 提出了创新性的算法思路解决实际问题",
    ]
    add_paragraph(doc, "选题方向：", first_line=False)
    for choice in choices:
        p = add_paragraph(doc, choice, first_line=False)
        p.paragraph_format.left_indent = Inches(1.2)

    rows = [
        ("学号", "Y202502064"),
        ("姓名", "李小茹"),
        ("专业", "计算机科学与技术"),
        ("课程指导教师", "伍东睿、朱力军、程骋"),
        ("院（系、所）", "研究生院"),
        ("日期", "2026年5月26日"),
    ]
    table = doc.add_table(rows=0, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for label, value in rows:
        cells = table.add_row().cells
        set_cell_text(cells[0], label, bold=True, size=12, align=WD_ALIGN_PARAGRAPH.RIGHT)
        set_cell_text(cells[1], value, size=12, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell_width(cells[0], 1.8)
        set_cell_width(cells[1], 3.8)

    doc.add_page_break()


def add_report_body(doc):
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

    add_paragraph(
        doc,
        "摘要：本文以 Kaggle House Prices - Advanced Regression Techniques 房价预测竞赛为研究对象，围绕结构化表格数据回归预测问题，构建了从线性基线到树集成模型、再到梯度提升树和加权融合的实验流程。实验采用 Ridge Regression、Random Forest、XGBoost、LightGBM、CatBoost 和 Weighted Ensemble 六类模型，对 SalePrice 进行 log1p 变换后，以 5 折交叉验证下的 RMSE 作为 RMSLE 的本地等价指标。结果表明，CatBoost 在本地验证中取得最优 RMSLE 0.12029，Kaggle Public Score 为 0.12481，明显优于 Ridge 和 Random Forest 基线。实验说明梯度提升树能够较好处理房屋属性中的非线性关系和特征交互，是解决该类竞赛问题的有效扩展算法。",
        first_line=False,
    )
    add_paragraph(doc, "关键词：机器学习；房价预测；梯度提升树；CatBoost；Kaggle", first_line=False)

    add_heading(doc, "1 引言", 1)
    add_paragraph(
        doc,
        "房价预测是机器学习在实际经济和生活场景中的典型应用。房屋成交价格受建筑面积、整体质量、建造年份、地理位置、地下室、车库、装修状态等多因素影响，变量之间具有明显的非线性关系和交互效应。传统线性模型能够提供可解释的基线，但在复杂结构化数据上往往难以充分刻画高阶特征关系。",
    )
    add_paragraph(
        doc,
        "本文选择 Kaggle House Prices 竞赛作为课程报告的竞赛问题。该任务要求根据训练集中的房屋特征预测测试集房价，线上评价指标为均方根对数误差 RMSLE。本文的动机是比较基础模型与近年常用的梯度提升树扩展算法在同一竞赛问题上的表现，并分析模型效果差异及改进方向。",
    )

    add_heading(doc, "2 方法或算法", 1)
    add_paragraph(
        doc,
        "设训练样本为 (xi, yi)，其中 xi 表示第 i 套房屋的多维特征，yi 表示成交价格。由于房价分布通常右偏，本文对目标变量进行 log1p 变换，即 zi=log(1+yi)。模型在 z 空间中训练和评估，最终预测时使用 expm1 还原为房价。",
    )
    add_heading(doc, "2.1 基线模型", 2)
    add_paragraph(
        doc,
        "Ridge Regression 在线性回归损失函数中加入 L2 正则化项，能够缓解特征共线性带来的过拟合问题。Random Forest 通过对多个决策树进行 Bagging 集成，能够捕捉一定的非线性关系，作为树模型基线。",
    )
    add_heading(doc, "2.2 扩展算法", 2)
    add_paragraph(
        doc,
        "XGBoost、LightGBM 和 CatBoost 均属于梯度提升树框架。梯度提升树通过逐轮拟合前一轮模型的残差或负梯度，不断降低损失函数。XGBoost 引入二阶梯度、正则化和列采样，具有较强的泛化能力；LightGBM 采用直方图算法和叶子优先生长策略，训练效率较高；CatBoost 对类别特征和有序提升机制进行了专门设计，在包含大量类别变量的结构化数据上表现稳定。",
    )
    add_paragraph(
        doc,
        "本文还实现了 Weighted Ensemble。其基本思想是根据各单模型交叉验证误差的倒数分配权重，使验证误差更低的模型在融合预测中占更大比例。该方法实现简单，能够检验不同模型预测结果是否具有互补性。",
    )

    add_heading(doc, "3 软件结构和软件实现方法", 1)
    add_paragraph(
        doc,
        f"项目代码已上传至 GitHub：{GITHUB_URL}。仓库中提供了环境配置、数据获取说明、样例输入和完整训练脚本。运行入口为 src/train.py，脚本自动完成数据读取、缺失值填补、类别变量独热编码、目标变量对数变换、5 折交叉验证、结果保存和提交文件生成。",
    )
    add_table(
        doc,
        ["路径", "作用"],
        [
            ("src/train.py", "主训练脚本，包含模型定义、交叉验证、融合与提交文件生成。"),
            ("src/utils.py", "通用工具，包括目录创建、指标图保存等。"),
            ("data/raw", "存放 Kaggle 原始 train.csv 和 test.csv，原始数据不提交到 Git。"),
            ("data/sample", "小型样例输入，用于验证程序运行流程。"),
            ("outputs", "保存交叉验证结果、图表和 Kaggle 提交文件。"),
            ("reports", "保存实验记录和课程报告。"),
        ],
        widths=[1.45, 5.0],
    )

    add_heading(doc, "4 数据描述", 1)
    add_paragraph(
        doc,
        "Kaggle House Prices 数据集包含 1460 条训练样本和 1459 条测试样本。每条样本描述一套房屋，特征包括数值型变量和类别型变量，例如 LotArea、OverallQual、YearBuilt、GrLivArea、GarageCars、Neighborhood、MSZoning 等。预测目标为训练集中的 SalePrice。",
    )
    add_table(
        doc,
        ["项目", "说明"],
        [
            ("数据来源", "Kaggle House Prices - Advanced Regression Techniques"),
            ("训练集规模", "1460 条样本"),
            ("测试集规模", "1459 条样本"),
            ("特征类型", "数值特征与类别特征混合"),
            ("预测目标", "SalePrice"),
            ("评价指标", "RMSLE；本地实验使用 log1p 目标空间 RMSE 等价计算"),
        ],
        widths=[1.6, 4.8],
    )

    add_heading(doc, "5 实验结果", 1)
    add_paragraph(
        doc,
        "实验采用 5 折交叉验证。所有模型使用相同的数据划分、预处理流程和随机种子 2026。表 1 给出了各模型在本地验证集上的平均 RMSLE 和标准差。",
    )
    add_table(
        doc,
        ["模型", "平均 RMSLE", "标准差", "说明"],
        [
            ("CatBoost", "0.12029", "0.00532", "本地交叉验证最优模型"),
            ("XGBoost", "0.12039", "0.00514", "与 CatBoost 非常接近"),
            ("Weighted Ensemble", "0.12187", "0.00000", "简单加权融合略差于最优单模型"),
            ("LightGBM", "0.12817", "0.00128", "训练稳定，但本配置下低于 XGBoost/CatBoost"),
            ("Random Forest", "0.14251", "0.00580", "基础树集成模型"),
            ("Ridge Regression", "0.14399", "0.02627", "线性基线模型"),
        ],
        widths=[1.6, 1.2, 1.0, 2.6],
    )

    if FIG.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(str(FIG), width=Inches(5.8))
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cap.add_run("图 1 各模型 5 折交叉验证 RMSLE 对比")
        set_run_font(r, size=10, bold=True)

    add_paragraph(
        doc,
        "从实验结果可以看出，CatBoost 和 XGBoost 的误差最低，说明梯度提升树能够有效学习房价数据中的非线性结构和特征交互。LightGBM 的表现也明显优于 Ridge 和 Random Forest，但在当前参数设置下不及 CatBoost 和 XGBoost。Ridge Regression 作为线性基线，难以充分表达复杂的房屋属性关系；Random Forest 虽能处理非线性，但其逐树独立训练的 Bagging 机制在该任务中不如 Boosting 类模型。",
    )
    add_paragraph(
        doc,
        "本文将本地交叉验证最优的 CatBoost 模型生成提交文件 best_model_submission.csv，并提交至 Kaggle。线上 Public Score 为 0.12481，与本地 5 折交叉验证 RMSLE 0.12029 较为接近，说明本地验证方案能够较好反映模型的泛化性能。简单加权融合没有超过最优单模型，可能原因是各强模型之间预测相关性较高，且当前权重仅由误差倒数确定，未进行专门的融合权重搜索。",
    )

    add_heading(doc, "6 总结", 1)
    add_paragraph(
        doc,
        "本文围绕 Kaggle 房价预测竞赛，完成了从数据准备、模型构建、交叉验证、线上提交到结果分析的完整机器学习实验流程。实验表明，梯度提升树模型整体优于线性模型和基础随机森林，其中 CatBoost 取得了最佳本地验证成绩和较稳定的线上得分。",
    )
    add_paragraph(
        doc,
        "后续改进可以从三个方向展开：第一，增加更细致的特征工程，如房屋总面积、房龄、翻修年限、质量交互项等；第二，对 XGBoost、LightGBM、CatBoost 进行更系统的超参数搜索；第三，采用 Stacking 或基于验证集优化的融合策略，替代简单误差倒数加权，以进一步提升 Kaggle 成绩。",
    )

    add_heading(doc, "参考文献", 1)
    refs = [
        "[1] Kaggle. House Prices - Advanced Regression Techniques[EB/OL]. https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques.",
        "[2] Chen T, Guestrin C. XGBoost: A Scalable Tree Boosting System[C]. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2016.",
        "[3] Ke G, Meng Q, Finley T, et al. LightGBM: A Highly Efficient Gradient Boosting Decision Tree[C]. Advances in Neural Information Processing Systems, 2017.",
        "[4] Prokhorenkova L, Gusev G, Vorobev A, et al. CatBoost: unbiased boosting with categorical features[C]. Advances in Neural Information Processing Systems, 2018.",
        "[5] Hastie T, Tibshirani R, Friedman J. The Elements of Statistical Learning[M]. Springer, 2009.",
    ]
    for ref in refs:
        add_paragraph(doc, ref, first_line=False)


def add_running_footer(doc):
    section = doc.sections[0]
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer.add_run("高级机器学习理论课程报告")
    set_run_font(run, size=9, color="555555")


def main():
    doc = Document()
    setup_styles(doc)
    add_running_footer(doc)
    add_cover(doc)
    add_report_body(doc)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
