# skill/ — 可安装使用的技能 / Skills you can install

> 🎯 **本域每个子目录是一个**独立技能**** —— 🅑 你拿一个走就能用，🅑 不必装别的。
> **怎么找到你要的那个** —— 🅑 **先问你遇到的是哪类事**：

| 🎯 你遇到的事 | 🎯 去这里 |
|:--|:--|
| 🅑 「**我怕有东西没查到、审得不狠**」 | 🎯 **审计与审查** |
| 🅑 「**同一类问题反复出，我想断根**」 | 🎯 **复盘与改进** |
| 🅑 「**我要拍板，但想要依据**」 | 🎯 **决策与规划** |
| 🅑 「**不是我一个人干，要分工**」 | 🎯 **协作与团队** |
| 🅑 「**上次的教训下次用不上**」 | 🎯 **记忆与回传** |
| 🅑 「**我要写东西 / 分享出去**」 | 🎯 **报告与写作** |
| 🅑 「**AI 跑着跑着偏了**」 | 🎯 **护栏** |
| 🅑 「**我要看外面什么情况**」 | 🎯 **情报与竞品** |
| 🅑 「**我要把它发出去 / 加个检查器**」 | 🎯 **发布与工程** |

---

## 一、🎯 审计与审查 —— 🅑 我怕漏

| 🎑 技能 | 🎯 它替你做 |
|:--|:--|
| [`adversarial-audit/`](adversarial-audit/) | 🎯 **对抗式审查 ＋ 递归闭环修复** —— 🅑 把「审完了」变成「审得住」：🅑 攻击结论、找反例、逐维核、闭环回原问题 |
| [`detector-signal-triage/`](detector-signal-triage/) | 🎯 **红灯三分法** —— 🅑 报警先判性质（🅑 模型缺陷 ／ 口径缺陷 ／ 真问题）再动手 |
| [`qdr-full-chain-audit/`](qdr-full-chain-audit/) | 🎯 **全链路批处理审计** —— 🅑 检查器组批量跑 → 分类 → 分流 → 批量修 → 快验 → 全量 |
| [`skill-review/`](skill-review/) | 🎯 **技能包质量审阅** —— 🅑 按 7 阶段出 P0–P3 任务 ＋ 验收单 |
| [`meta-library-steward/`](meta-library-steward/) | 🎯 **沉淀层巡检** —— 🅑 查重复 ／ 查质量 ／ 查生命周期 |

## 二、🎯 复盘与改进 —— 🅑 我想断根

| 🎑 技能 | 🎯 它替你做 |
|:--|:--|
| [`task-retrospective/`](task-retrospective/) | 🎯 **复盘到位的方法** —— 🅑 从「发生了什么」到「下次怎么不再发生」，🅑 含分析、判据、检查单与模式库 |
| [`report-iteration-steward/`](report-iteration-steward/) | 🎯 **内容迭代管家** —— 🅑 专治「计划很大、执行救火」（🅑 迭代预检 ／ 版式 ／ 模块完整性 ／ 版本一致） |

## 三、🎯 决策与规划 —— 🅑 我要拍板

| 🎑 技能 | 🎯 它替你做 |
|:--|:--|
| [`decision-expert/`](decision-expert/) | 🎯 **决策单元** —— 🅑 每个决策留下依据、选项、取舍与复盘点 |
| [`qdr-deep-governance-planning/`](qdr-deep-governance-planning/) | 🎯 **多轮深挖 ＋ 第一原理** ⇒ 🅑 产出**可执行分解计划** |
| [`infrastructure-audit/`](infrastructure-audit/) | 🎯 **建前查存量** —— 🅑 先搜（🅑 查重 ／ 影响面 ／ 同类），🅑 搜不到再取证 |
| [`dynamic-archives-steward/`](dynamic-archives-steward/) | 🎯 **动态档案表管理** —— 🅑 前置审计 ／ 数据血缘 ／ 字段来源 ／ 刷新记录 |

## 四、🎯 协作与团队 —— 🅑 要分工

| 🎑 技能 | 🎯 它替你做 |
|:--|:--|
| [`agent-team-orchestration/`](agent-team-orchestration/) | 🎯 **团队怎么组、怎么交接、怎么收口** —— 🅑 角色 ／ 生命周期 ／ 交接协议 ／ 评审 |
| [`governance-audit-team/`](governance-audit-team/) | 🎯 **治理审计团** —— 🅑 五步编队：🅑 入口审视 → 规划 → 全链路 → 对抗审查 → 深审收口 |

## 五、🎯 记忆与回传 —— 🅑 教训要能用上

| 🎑 技能 | 🎯 它替你做 |
|:--|:--|
| [`memory-management/`](memory-management/) | 🎯 **五层记忆防线** —— 🅑 权威源 ／ 强制加载 ／ 写前路由 ／ 归因写入 ／ 回溯审计 |
| [`harvest-push/`](harvest-push/) | 🎯 **回传通道**（🅑 现场 → 中枢）—— 🅑 采纳反馈、可复用发现、复盘结果，🅑 **追加**而不覆盖 |
| [`inject-push/`](inject-push/) | 🎯 **注入通道**（🅑 中枢 → 现场）—— 🅑 让现场用上最新规则与样本，🅑 **不必自己去追** |

## 六、🎯 报告与写作 —— 🅑 我要写东西

| 🎑 技能 | 🎯 它替你做 |
|:--|:--|
| [`write-report/`](write-report/) | 🎯 **研究报告方法论** —— 🅑 结构设计 → 研究 → 大纲 → 分章 → 数据核查 → 终稿 |
| [`report-desensitize/`](report-desensitize/) | 🎯 **脱敏** —— 🅑 把内部完整版转成可对外分享的版本（🅑 自动识别 ＋ 分级） |

## 七、🎯 护栏 —— 🅑 AI 别跑偏

| 🎑 技能 | 🎯 它替你做 |
|:--|:--|
| [`ai-drift-guard/`](ai-drift-guard/) | 🎯 **跑偏守卫** —— 🅑 分层协议：🅑 一部分信号可被宿主**强制拒绝**，🅑 一部分只写入上下文 |

## 八、🎯 情报与竞品 —— 🅑 看外面

| 🎑 技能 | 🎯 它替你做 |
|:--|:--|
| [`competitor-product-analysis/`](competitor-product-analysis/) | 🎯 **竞品分析** —— 🅑 前置预检 ／ 七步查询 ／ 三表输出 ／ 信源分级 ＋ 置信度 |
| [`industry-intelligence-sourcebook/`](industry-intelligence-sourcebook/) | 🎯 **行业情报源手册** —— 🅑 经验证的竞品公司 ／ 展会 ／ 标准组织 ／ 官渠 ／ 媒体分层清单 |

## 九、🎯 发布与工程 —— 🅑 我要把它发出去

| 🎑 技能 | 🎯 它替你做 |
|:--|:--|
| [`qdr-external-publish/`](qdr-external-publish/) | 🎯 **对外发布的流程与判据** —— 🅑 四步：🅑 切面门禁 → 本地库 → 云端库 → 发布回执 |
| [`qdr-new-script-pipeline/`](qdr-new-script-pipeline/) | 🎯 **新脚本落地流程** —— 🅑 建 → 注册 → 三验 → 接线 → 复跑 |

---

## 🎯 怎么用 / How to use

🅑 **每个技能目录内有 `SKILL.md`** —— 🅑 那是**它的本体**（🅑 **先读它**）。
🅑 **其余件是该技能的补充**（🅑 `references/` 详法 ／ `scripts/` 可跑 ／ `dependencies/` 自备项）。
🛑 **本体不在的目录** ⇒ 🅑 **它尚未可用**（🅑 而本库有门禁拦这种情况）。
