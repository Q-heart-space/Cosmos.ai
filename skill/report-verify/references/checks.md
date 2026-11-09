# 30 项自动校验清单（通用版）

> **适用范围**：<组织>全系报告（maritime/strategy/data/client）
> 对应脚本：`_report_validator.py`（待适配各报告类型）

## 全报告通用校验（18项，所有类型强制执行）

| # | 检查项 | 级别 | 说明 |
|---|--------|------|------|
| 1 | 版本号全局一致性 | ERROR | 元数据块+版本修订表+文件名 三处一致 |
| 2 | 版本修订记录连续性 | ERROR | 版本号无跳跃、日期无倒序 |
| 3 | H2/H3 标题不重复 | ERROR | 所有标题唯一 |
| 4 | 全链路标题层级验证 | ERROR | H1→H2→H3→H4 父子编号一致 |
| 5 | H2 过渡文字检查 | ERROR | 每个 H2 后必有过渡文字（≥30字） |
| 6 | 数据引用一致性 | ERROR | 百分比/金额数据有来源标注 |
| 7 | 敏感措辞移除 | ERROR | 无敏感词 |
| 8 | 重复内容检测 | ERROR | 无完全重复的章节/段落 |
| 9 | 重复表头/图注检测 | ERROR | 无双重表头、无重复编号 |
| 10 | Markdown表格结构完整性 | ERROR | 每张表 header/delimiter 列数一致 |
| 11 | 多格式一致性预检 | WARNING | 表格列数/图片路径/代码块配对 |
| 12 | 交叉引用有效性 | ERROR | 所有章节/图表引用指向存在的内容 |
| 13 | 锚点 ID 完整性 | WARNING | 目录引用锚点均已定义且唯一 |
| 14 | 图表编号系统校验 | WARNING | 图/表编号与引用一致（如适用） |
| 15 | 上下文逻辑衔接 | WARNING | 段落衔接词/术语一致性 |
| 16 | 关键数据橙色高亮 | WARNING | 执行摘要中核心量化数据必须加粗 `**数字**`, strong 色为 `danger`（统一品牌红） |
| 17 | 品牌色来源校验 | ERROR | 品牌色从 `brand_colors.json` 读取（通过 `brand_css.py` 共享模块变量替换）。PDF 通过 Edge CDP 渲染 HTML 实现，主橙色为 `primary`，非硬编码 |
| 18 | 表格格式统一性 | WARNING | 表头=浅暖底 `warm_white` + 2px 橙底线，斑马纹偶数行 `warm_white`，边框 `border`（暖米色）。对齐行使用 `|:--|` 标准格式，表格标题后有空行 |
| 26 | 块引用内嵌表格检测 | WARNING | 表格不应嵌套在 `>` 块引用中——会导致CSS渲染器将表格包裹在blockquote样式中，视觉上与正文表格不一致。检测 `> |` 格式的行 |
| 27 | 表格首列空表头检测 | WARNING | 表格首行首列不应为空 `| |` ——在Python markdown渲染中会产生无文本的表头单元格，破坏视觉一致性。应添加维度标签（如 `| 维度 |`） |
| 28 | 表格单元格多行内容检测 | WARNING | 表格单元格内不应使用 `<br>` 标签或原始换行符。Python markdown 的 tables 扩展会转义 `<br>` 为可见文本，且不识别行内换行。多行内容应**展平为单行**，使用 `——` 或 `；` 分隔 |
| 29 | 目录独立页检查 | WARNING | 目录必须独占一页：① 目录前有 `page-break-before: always`（断开摘要）；② 目录后有 `page-break-after: always`（断开正文）。验证 HTML 中存在 3 处分页点：目录前、目录后、第一章前 |
| 30 | 大篇章分页检查 | WARNING | 每个大篇章（H2标题）在PDF中应从新页开始。验证 HTML 中 H2 标题前有 `<div style="page-break-before: always;"></div>` 内联 style（Edge CDP `preferCSSPageSize: True` 时忽略 CSS `page-break-*` 规则） |
| 31 | PDF页眉页脚检查 | WARNING | 页眉：`file_id \| <组织显示名> \| 内部机密`（`gold` 暖棕灰）。页脚：`第 X 页 / 共 X 页`（中文），`gold`，橙色 `primary` 顶线。Edge CDP `Page.printToPDF` 需启用 `displayHeaderFooter: True` |

## 按报告类型专用校验（6项，按需启用）

| # | 检查项 | 适用类型 | 级别 | 说明 |
|---|--------|---------|------|------|
| 19 | 篇章完整性 | maritime | ERROR | 五篇各出现且仅出现1次 |
| 20 | 竞品排列顺序 | maritime | WARNING | 国外→台湾→大陆 |
| 21 | 执行摘要编号连续性 | strategy | WARNING | 编号式结论列表连续无跳号 |
| 22 | ▓过渡标记一致性 | strategy | WARNING | 层注释标记与章节匹配 |
| 23 | 客户名一致性 | client | ERROR | 全文客户名无混用 |
| 24 | 个人人名校验 | all | WARNING | 无法定代表人名/高管姓名 |
| 25 | TOC正文标题映射校验 | strategy | WARNING | 提取目录中所有锚点链接，与正文H2/H3标题逐一比对——报告编号不一致/缺失/多余的条目。**同时扫描正文中 `**X.Y.Z` 格式的遗留旧章节编号。附录子节（A.1/A.2/B.1-B.9等）须在目录中列出** |

## 来源分级标准（全报告通用）

| 级别 | 来源类型 | 示例 |
|:--|:--|:--|
| **A+** | 内部系统实测数据（最高权威） | 金蝶ERP出货记录、卫瓴CRM跟进记录、简道云客诉数据 |
| **A** | 官网规格书/官方文档 | apq.com.cn, limyee01.com, senke.com, 1688官方 |
| **B** | 行业报告/研究机构 | pmarketresearch, valuates, GlobalInfoResearch |
| **C** | 媒体/博客/百科 | baijiahao, sohu, zhihu, csdn, 百度文库 |
| **D** | 推测/估计 | 无明确来源的估算值 |

| 报告类型 | 表格编号格式 | 示例 |
|:--|:--|:--|
| maritime | `**表 X-Y 数据表**` | `**表 2-3 数据表**` |
| strategy | 不加编号（仅粗体标题） | `**凌壹供板四场景可行性矩阵**` |
| data/client | `表X.Y：标题` | `表1.1：客户分层` |

## 校验器使用

```bash
cd "D:\Workbuddy\<项目目录>"
python _report_validator.py --md "报告文件.md" --type strategy
```
