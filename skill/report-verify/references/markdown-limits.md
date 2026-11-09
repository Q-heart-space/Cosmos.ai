# Python Markdown 渲染限制速查

> **用途**：编写/修复 Markdown 时参考，避免写出渲染后与预期不一致的内容。
> **库**：Python markdown 3.x + extensions: tables, fenced_code, codehilite, toc, sane_lists

## 表格限制

| 问题 | 错误写法 | 正确写法 | 原因 |
|:--|:--|:--|:--|
| 表格内无法换行 | `<br>` 标签 / 原始换行 | **展平为单行**，用 `——` 或 `；` 分隔 | tables 扩展转义 HTML（`<br>`→`&lt;br&gt;`），且不识别行内 `\n` |
| 首列为空 | `| | 列B | 列C |` | `| 维度 | 列B | 列C |` | 空单元格产生无文本的 `<th>`，橙色背景空白 |
| 表嵌套块引用 | `> | A | B |` | 表格独立于 `>` 外 | blockquote 包裹表格，叠加背景色和左边框 |
| 分隔符格式 | `|---|` | `|:--|` | 无冒号仍可渲染但不符合 V5.3 规范 |

## TOC 锚点规则

| 问题 | 说明 |
|:--|:--|
| toc 扩展生成的 ID | 格式为 `_1`, `_1-1` 等序号——**与 MD 中手动 `[text](#anchor)` 不匹配** |
| 解决方案 | `build_html.py` 内 `add_heading_ids()` 后处理替换为 `id="1.1"` / `id="执行摘要"` 等可预测 ID |
| 目录必须包含 | 所有 H3 子节（含附录 A.1/B.1 等） |

## 其他已知限制

| 问题 | 说明 |
|:--|:--|
| emoji 渲染 | Python markdown 保留 emoji 原文，HTML 中正常显示 |
| 代码块内加粗 | `**text**` 在代码块内显示为字面量，不渲染 |
| 块引用内嵌表格 | `> |` 格式产生嵌套结构，应避免 |
| 连续 `---` | 产生多余空白间距，应合并为单个 |

## 品牌色引用

所有构建脚本从 `brand_colors.json` 读取——**不得在 CSS/MD/PDF 脚本中硬编码任何色值**。

```python
# 正确
C['_layout'].get('table_header_bg', fallback)
C['_layout'].get('table_header_text', fallback)
C['_layout'].get('table_stripe_bg', fallback)

# 禁止
background: #F39910;              # 硬编码
background: {C['apq-orange']};    # 应从 layout 段读取
```
