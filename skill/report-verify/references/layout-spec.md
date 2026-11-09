# 排版布局规范

## 标题层级

| 层级 | Markdown | 字号 | 颜色 | 样式 |
|------|----------|------|------|------|
| 篇章 (H1) | `# 第X篇 标题` | 17pt | 深棕 `primary_dark` | 底边 3px 橙线，bold 700 |
| 章 (H2) | `## 一、标题` | 12pt | 暖棕 `text_strong` | 左 4px 橙线（无背景——Edge CDP色彩管理会偏移近白色，禁止用 background） |
| 节 (H3) | `### 1.1 标题` | 10.5pt | 警示红 `danger` | 底边 1px 暖米色线 |
| 子节 (H4) | `#### 标题` | 9.5pt | 暖棕 `text_strong` | 无特殊样式 |

**编号规范**：
- H2: 中文数字后跟中文顿号（`## 一、`）
- H3: 阿拉伯数字 + 点号（`### 1.1`），编号 = 篇章号.节号
- H1: `# 第X篇 标题`，`篇` 与标题之间**仅一个空格**（ASCII U+0020）

## 分页控制

> ⚠️ PDF 生成使用 Edge CDP `Page.printToPDF` + `preferCSSPageSize: True`，分页必须通过**内联 style** 实现，CSS 中的 `page-break-*` 规则被忽略。以下 CSS 仅用于浏览器预览。

```css
/* 浏览器预览用（非 PDF 生成） */
.chapter-h2 { page-break-before: always; }
.page-break { page-break-before: always; }
table { page-break-inside: auto; }
tr { page-break-inside: avoid; }
thead { display: table-header-group; }
h2, h3, h4 { page-break-after: avoid; }
img, pre, blockquote { page-break-inside: avoid; }
```

**PDF 分页实现（内联 style）**：
在 `md_to_html()` 中通过正则插入：
1. 目录前：`<h2>目录</h2>` 前插入 `<div style="page-break-before: always;"></div>`
2. 目录后：`<hr>` 后插入 `<div style="page-break-after: always;"></div>`
3. 正文前：`第一章前` 插入 `<div style="page-break-before: always;"></div>`

**必须分页的位置**：封面、目录（独立页·前+后均分页）、每个 `## 中文数字、` 篇章标题、附录标题

## 图表规范

- ASCII 架构图用 ` ``` ` 代码块包裹
- 图片必须有图注（`*图注文字*` 斜体）
- 表格后必须跟数据来源说明
- 图片路径：优先放在 `report_images/` 目录

## 竞品编排顺序

```
国外欧美 → 中国台湾 → 中国大陆
```

| 区域 | 厂商示例 |
|------|----------|
| 国外（欧美） | Hatteland, Siemens, Kontron, Cincoze, Beijer |
| 中国台湾 | Winmate, Axiomtek, Neousys, Advantech, NEXCOM, IEI, Moxa |
| 中国大陆 | 达文, 稳信, 阿普奇 |

## 报告章节标准顺序

1. 🎯 报告概要
2. 📈 统计汇总
3. 🔥 重点商机
4. 🚨 客诉记录
5. 🔴 风险预警
6. 🎯 行动建议

## 风险等级标注

| 级别 | 图标 | 颜色 |
|------|------|------|
| 高 | 🔴 | `danger` |
| 中 | 🟡 | `warning` |
| 低 | 🟢 | 默认文字色 |
