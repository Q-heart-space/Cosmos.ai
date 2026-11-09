# 品牌视觉规范

> **单一事实来源**：品牌色值唯一来源＝组织配置 `business:<域>/<组织>/brand/brand_colors.json`；
> 本文件只说**角色与用途**，🛑 **不含任何组织色值、不含任何组织名**。

## 品牌配色（角色与用途）

> 色值请读取组织配置的 `colors` 字段（角色名见下表左列）。
> 🛑 **组织缺失时**：按 `references/brand_colors.template.json` 的**中性灰默认**校验，**不猜任何组织品牌色**。

| 角色名（`colors` 键） | 变量名 | 用途 |
|:--|:--|:--|
| `primary` | `--brand-primary` | ⭐ 主品牌色：标题下划线、封面Badge、页眉强调、表头强调色条 |
| `primary_light` | `--brand-primary-light` | 浅色：副标题、次要强调、hover 状态 |
| `warm_white` | `--brand-warm-white` | 暖白：表格偶数行、页面背景 |
| `deep_brown` | `--brand-deep` | 深色文字：篇章（H1）标题 |
| `light_gray` | `--brand-light-gray` | 浅灰：表格边框、卡片边框、分隔线 |
| `mid_gray` | `--brand-mid-gray` | 中灰：H2 标题、强调文字 |
| `dark_gray` | `--brand-dark-gray` | 深灰：正文、封面标题 |
| `danger` | `--brand-danger` | 警示色：H3 标题色、高危标注、P0 优先级 |
| `success` | `--brand-success` | 通过色：零质量问题、认证通过 |
| `link` | `--brand-link` | 链接色：超链接、引用标注 |
| `gold` | `--brand-gold` | 装饰色：封面 footer 文字、弱化页眉 |

## 执行规则

1. **读取组织配置**：执行前先读 `business:<域>/<组织>/brand/brand_colors.json` 的 `colors`
2. **禁止硬编码**：本文件及构建脚本中 🛑 **禁止出现具体色值**，必须按**角色名**从配置读取
3. **同步修改**：改色值时只改组织配置那一处
4. **同步到副本**：修改后须同步以下位置
   - 报告构建技能内的副本（`<构建技能>/references/brand_colors.json`）
   - 品牌色配置由**组织配置**提供：`business:<域>/<组织>/brand/brand_colors.json`（🆕 2026-11-09 组织参数化：原为某具体项目路径）
5. **角色名映射**：构建器只认**角色名**（见 `template.json` 的 `role_map`），不认组织自定义名

## 中文字体优先级

1. **微软雅黑** — `C:/Windows/Fonts/msyh.ttc`（首选）
2. **黑体** — `C:/Windows/Fonts/simhei.ttf`（备选）
3. **宋体** — `C:/Windows/Fonts/simsun.ttc`（兜底）

## 表格样式规范

| 规范项 | 取值（按角色名引用） |
|:--|:--|
| 奇数行 | `bg`（默认白） |
| 偶数行 | `warm_white` |
| 表头 | `warm_white` 稍深（由配置提供）·加粗·**不用深色背景** |
| 外框 | 0.8pt 边框 `warm_white` 稍深 |
| 内网格 | 0.3pt 边框 `warm_white` 稍深 |
| 表头底边 | 2px `primary` |

## 页眉规范

- 左：`primary` 粗体「**<组织显示名>** · [报告类型]」（20pt）
- 右：`<组织法定名>`（12pt，`mid_gray`）
- 下方：2.5px `primary` 下划线

> 🛑 **组织名来源**：`business:<域>/<组织>/brand/organization.json` 的 `display_name` / `legal_name`。
> 🅑 **缺失时**：用中性占位 `公司名` / `Company`，**不猜任何组织名**。

## 页脚规范

```
第 X 页 / 共 Y 页
```
居中显示：`display:block` + `text-align:center` + `width:100%`
