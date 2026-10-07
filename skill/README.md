# skill/ — 可安装使用的技能

Q博士 对外发布的**技能便携版**（portable build）。每个技能占**一个子目录**，互不混叠。

## 已发布技能

| 技能 | 一句话 | 版本 |
|:--|:--|:--|
| [`ai-drift-guard/`](ai-drift-guard/) | AI-Drift-Guard / AI跑偏守卫：分层协议。Tier A 信号（S5/S4/S | 1.5.0-ext |
| [`competitor-product-analysis/`](competitor-product-analysis/) | 竞品嵌入式硬件产品的标准化查询与分析方法论 v1.5.0。含前置预检(P0-P3)、七步查询 | 1.5.0-ext |
| [`industry-intelligence-sourcebook/`](industry-intelligence-sourcebook/) | 行业情报源手册（知识型技能·无用户触发词·供自动化任务和跨项目复用）——提供经验证的竞品公司 | 1.1.1-ext |
| [`report-iteration-steward/`](report-iteration-steward/) | 通用内容迭代管家 v2.1（核心专注报告迭代·🆕 v2.1 2026-09-15 A1 同类 | 2.1.0-ext |
| [`skill-review/`](skill-review/) | 技能质量审阅 v1.3.0——对业务技能包（SKILL.md+references+scri | 1.3.0-ext |
| [`write-report/`](write-report/) | 研究报告撰写方法论——结构设计→研究→大纲→分章撰写→数据核查→终稿 | 1.0.0-ext |

## 用法

1. 选一个技能子目录
2. 按其 `README.md` 安装 —— 🎯 **复制到你所用的宿主之技能目录**（🅑 各宿主不同，见下），或用该宿主的导入功能
3. 用自然语言触发词使用

> 🎯 **本库**宿主无关**** —— 🅑 同一个技能可装到**任何**支持该形态的宿主。
> 🅑 常见宿主之技能目录（🅑 举例·🛑 非穷举·🛑 亦非推荐）：`<宿主配置根>/skills/` ／ `<宿主配置根>/skills/`（🅑 各宿主名字不同）等 —— 🎯 **具体以该宿主文档为准**。

## 结构约定

| 项 | 必需？ | 说明 |
|:--|:--|:--|
| `SKILL.md` | 🎯 **必需** | 技能定义（触发词 ＋ 协议） |
| `references/` | 🎯 **必需** | 参考实现 / 清单 |
| `LICENSE` | 🎯 **必需** | 该技能的许可 |
| `README.md` | 🅑 **建议** | 安装与使用（🅑 少数技能以 `SKILL.md` 自带用法） |
| `CHANGELOG.md` | 🅑 **建议** | 版本历史（🅑 少数技能以 `SKILL.md` 之版本字段为准） |
| `CONTRIBUTING.md` | 🅑 **建议** | 该技能的贡献说明 |

```
skill/<skill-name>/
├── SKILL.md          # 🎯 必需
├── references/       # 🎯 必需
├── LICENSE           # 🎯 必需
├── README.md         # 🅑 建议
├── CHANGELOG.md      # 🅑 建议
└── CONTRIBUTING.md   # 🅑 建议
```
