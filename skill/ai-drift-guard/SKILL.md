---
name: ai-drift-guard
description: "AI-Drift-Guard / AI跑偏守卫：分层自检协议。Tier A 信号（S5/S4）给出可被宿主强制执行的规范契约；Tier B 信号（S1/S2/S3/S6/S7/S8/S9/S10）为提示词层自检。抑制过度工程化、格式蔓延、范围膨胀与未验证的修复。平台中立——不绑定任何 AI 平台。"
version: 1.4.0
agent_created: true
creator: Q博士
tags: [guard, anti-drift, over-engineering, quality, self-check, bilingual, platform-neutral]
triggers:
  - AI跑偏守卫
  - drift guard
  - 检查是否跑偏
  - 别过度设计
platform: any
space_scope: universal
cross_space_compatible: yes
distribute_external: yes
trust_level: auto
license: MIT
---

# AI-Drift-Guard / AI 跑偏守卫

> **平台中立。** 本协议不预设任何 AI 平台、目录结构或钩子名称。
> 宿主能力由适配器提供，见 [`references/adapters.md`](references/adapters.md)。

## 设计原则：可执行性分层

协议里每一条信号都标了 **Tier**。这不是修辞，而是「谁负责执行」的区分：

| Tier | 含义 | 需要什么 | 本协议信号 |
|:--|:--|:--|:--|
| **A** | **可机械判定**，能由宿主在动作发生前**真的拦下** | 宿主提供 dispatch 前钩子（或 pre-commit / CI） | S5、S4 |
| **B** | 只能作为**提示词**约束模型，无强制力 | 无——写进上下文即可 | S1 S2 S3 S6 S7 S8 S9 S10 |

**不要声称 Tier B 信号被"保证"了。** 它们是提醒，不是中断。把 Tier B 说成机制，是这套协议最容易犯的自我欺骗。

## Pain Points You Know Too Well / 你一定遇到过的痛点

| EN | 中 |
|:--|:--|
| "Optimize this rule" → AI designs a 4-phase migration | "优化一下规则" → 它给了个4阶段迁移方案 |
| "Check the data" → AI generates an HTML report | "看看数据" → 它自动生成了HTML报告 |
| "Do it" → AI asks "Shall I?" | "执行" → 它反问"可以吗？" |
| "Stop" → AI keeps writing | "停" → 它还在继续输出 |

**EN: Root cause: AI's default tendency is "go maximal". Tier A stops it at the host; Tier B asks the model to stop itself.**
**中：根因：AI 的默认倾向是"做重做全"。Tier A 由宿主拦下，Tier B 靠模型自觉。**

## When It Triggers / 触发时机

| EN | 中 | Tier |
|:--|:--|:--|
| Writing a file that may contain unreplaced placeholders | 写出可能含未替换占位符的文件 | A（S5） |
| About to modify a global rule/composition file | 即将修改全局规则/编排文件 | A（S4） |
| Outputting a multi-step plan or design | 输出多步骤计划或设计方案 | B |
| Generating files (HTML, PDF, scripts) | 生成文件（HTML/PDF/脚本） | B |
| Batch writes or bulk modifications | 批量写入或大规模修改 | B |
| Saying "done" after fixing one thing | 修一个问题就说"完成了" | B |

## Tier A — 规范契约（Normative）

以下内容是**规范**，不是建议。任何语言的实现都应当能逐条对上，从而在不同宿主间得到相同判定。

### A.1 决策语义

宿主必须在"工具调用 dispatch 之前"提供拦截点：

```
hook(input) -> decision

input  := { tool: string, arguments: object }
decision := { kind: 'allow' }
          | { kind: 'deny', reason: string }
          | { kind: 'ask',  reason?: string }
```

- 不支持交互审批的宿主，应当把 `ask` 视为 `deny`（fail closed）。
- 判定必须是**纯函数**，除下述 ledger 外不依赖外部状态。

### A.2 会话扫描台账（scan ledger）

- 每个会话维护一个集合：**已记录过关联扫描的 basename**。
- **不跨会话持久化**——它是"这一轮有没有先看过依赖"的记录，不是长期知识。
- 记录动作发生在 A.3 第 1 步。

### A.3 判定顺序

对每次 `write` / `edit` / 搜索类调用：

1. 若 `tool` 是搜索类（如 grep / glob / search）：
   用 `arguments.pattern` 与 `arguments.path` 拼出**探测串**，
   使得转义正则与原生路径都能命中——实现应当**先去掉反斜杠**再匹配
   （否则 `cordis\.patch\.yml` 这类规范写法的转义正则将无法命中，这是本协议 v1.3 的真实缺陷）。
   探测串中出现 `globalRuleMatchers` 任一条目的 basename → 记入 ledger；返回 `allow`。
2. 若 `tool` 不属于 `write` / `edit`：返回 `allow`。
3. **S5**：路径扩展名为 `.html` / `.htm` 时执行 A.4；有发现 → `deny`。
4. **S4**：路径匹配 `globalRuleMatchers` 且其 basename 不在 ledger → `deny`。
5. 否则 `allow`。

### A.4 S5 检测（规范性算法）

1. 仅对扩展名（小写）为 `.html` / `.htm` 的路径生效。
2. 逐行扫描内容。占位符模式：`{` + Unicode 字母/数字/下划线 + `}`，即 `/\{[\p{L}\p{N}_]+\}/gu`。
   **必须 Unicode 感知**，否则 `{标题}` 这类中文占位符会漏检。
3. 整行跳过，当且仅当该行 `trim()` 后满足以下任一条：
   - 匹配 `^\s*\{\d+\}\s*$` —— CSS 字重简写，如 `{3}`
   - 匹配 `^[^:]*:\s*\{[^}]+\}$` —— CSS 属性值
   - 含 JS 注释标记。**检测注释前必须先把 URL 的 `://` 中和掉**
     （例如替换为 `:\u002F\u002F`），否则任何含 `https://` 的行都会被整行跳过——
     这是原实现（v1.3 及以前）的真实盲区：`<script src="https://…">{placeholder}</script>` 不会被发现。
4. 逐个出现处跳过，当且仅当：标识符在 `IGNORE_KEYWORDS` 中，或全为数字。
5. 每行**最多报告一处**，格式固定为：
   `line <行号>: <token> in: <trimmed 行内容，截断到 100 字符>`
6. 发现列表非空 → `deny`，`reason` 中列出最多 5 条发现，并说明"修好内容后才能重试"。

`IGNORE_KEYWORDS` 与 `IGNORE_PATTERNS` 的权威副本见
[`references/drift-guard-core.mjs`](references/drift-guard-core.mjs)（与
`references/template_validator.py` 必须保持一致）。

> 为什么用"忽略关键字"而不是更聪明的解析：**门禁的误报比漏报更贵**。
> 一份会拦住正常 Chart.js 配置的守卫，会在第二天被关掉。

### A.5 宿主必须提供（适配器接口）

| 名称 | 含义 | 本协议是否预设 |
|:--|:--|:--|
| `hookPoint` | dispatch 前的拦截能力 | ❌ 不预设。宿主自定 |
| `globalRuleMatchers` | **该平台自己的**"全局规则/编排文件"清单 | ❌ 不预设。**协议不含任何平台路径** |
| `logSink` | 每条决策的落点 | ❌ 不预设。可为文件 / stdout / CI 日志 |

参考实现把这三项收敛成一个 `createGuard(config)`，见 `drift-guard-core.mjs`。

### A.6 记录格式

每次 `deny` 追加一行 JSON（JSONL）：

```json
{"seq":1,"at":1789621858955,"signal":"S5","tool":"write",
 "target":"…/report.html","reason":"leaked template placeholders",
 "detail":["line 5: {page_title} in: <title>{page_title}</title>"]}
```

**这条记录是"每次自阻断都记日志"从声明变成事实的唯一方式。**
没有落点的宿主，应当在 `deny` 的 reason 里显式回报"日志不可用"，而不是静默吞掉。

## Tier B — 提示清单（无强制力）

| # | 触发 | 正确反应 |
|:--|:--|:--|
| **S1** | 用户说"分析/看看"但没说要文件 | 降级为文字摘要 |
| **S2** | 用户说"执行"但 AI 反问"可以吗？" | 直接执行 |
| **S3** | 脚本/批量写入即将执行 | 先检查模型与任务是否匹配 |
| **S6** | 修了一个问题就要说"完成了" | 先搜同类问题，一并修 |
| **S7** | 用户简短确认（"对"/"嗯"） | 确认意图后再动 |
| **S8** | 多步骤任务中途跳过中间步骤 | 回到第一个未完成步骤 |
| **S9** | 用户说"停" / "stop" | **硬截断**：下一轮回复以 0 字符结束——没有标点、没有 emoji、没有"好的" |
| **S9-INPUT** | 用户本轮第一条消息就是"停" | 不要开始生成。不分析、不道歉、不解释 |
| **S10** | 方案 ≥3 阶段 / ≥2 个新文件 / ≥5 步 | 本回合先交付最小可用切片 |

**S9 的诚实说明**：它要求的是"模型在你说话的瞬间停住"。这**属于模型推理层或客户端层**，
提示词做不到。把它列为 Tier B 而不是假装它是机制，是本协议 v1.4 的修正。

**S11（已移除）**：旧版有一条 S11 引用 `your project's sync-validation routine`——
这是一个未绑定的占位符，在公开库中对任何读者都是死文本。它属于某个具体项目的私有流程，
不符合本库"只放可公开迁移资产"的边界，故移除。若你需要等价能力，请把它实现为
你自己宿主的 `globalRuleMatchers` 条目（Tier A 机制，配置在宿主侧）。

## Engineering vs. Gradualism / 工程化 vs 渐进式

> EN: Not every fix needs a system. Not every cleanup needs structure.
> 中：不是每个改进都要建系统，不是每个清理都要搭架构。

| Trigger Profile (EN) | 触发特征（中） | Right Approach / 正确做法 |
|:--|:--|:--|
| Systemic risk, cross-project, recurring | 系统性风险·跨项目·多次发生 | ✅ Build it properly / 该工程化 |
| One-off, single-point fix | 单点小问题·一次性场景 | ❌ Over-engineering / 过度工程化 |
| Clear verification path, reusable | 有验证路径·可跨场景复用 | ✅ Build it properly / 该工程化 |
| Pure hypothesis, unverified | 纯假设·未验证 | ❌ Over-engineering / 过度工程化 |
| User said "build a system" | 用户说"建一个系统" | ✅ Full design / 全量设计 |
| User said "optimize/fix/clean" | 用户说"优化/修复/清理" | ⚠️ Start minimal / 先最小可行 |

## 安装 / Installation

本技能**不依赖任何特定平台**。三条路径按宿主能力递增：

**1）只有"技能目录"的宿主** —— 把本目录整体拷进去即可，此时只有 Tier B 生效。
不要因为技能装上了就以为 Tier A 也在运行。

**2）支持工具钩子的宿主** —— 额外启用 Tier A。契约见
[`references/adapters.md`](references/adapters.md)。该文件同时给出一个 DSH 适配器实例
（**只是一个实例，不是要求**）以及为自己的宿主写适配器的检查清单。

**3）不需要任何 AI 平台** —— S5 可以直接当作**提交前检查 / CI 步骤**运行：

```bash
node references/drift-guard-core.mjs check path/to/page.html
# 退出码 0 = 干净；1 = 有泄漏占位符
```

这是最中立的强制方式：它约束的是**产物**，而不是模型。

## 可验证性 / Verifiability

旧版写着"过度工程化方案：趋近零"。那是一个**不可证伪**的声明——没有度量、没有基线、没有记录。

v1.4 起，把效果声明换成可核对的量：

| 声明 | 怎么核对 |
|:--|:--|
| S5/S4 拦截生效 | 造一个应交由 A.4 判定的文件，看宿主是否 `deny`，且**该文件未落盘** |
| 无误报 | 造一个含 `{data}` / `{labels: [...]}` 的合法 HTML，确认被放行 |
| 每次自阻断有记录 | 打开 `logSink`，逐条比对 |

没做过这三项核对的宿主，不应声称已启用 Tier A。

## What This Skill CAN and CANNOT Control / 能力边界

| Layer | Tier A CAN | 本协议 CANNOT |
|:--|:--|:--|
| 工具调用 | ✅ 在 dispatch 前拒绝 | ❌ 中断已经开始执行的调用（客户端层） |
| 输出文本 | ✅ — | ❌ 取消模型推理/深度思考（模型层） |
| 客户端 UI | ✅ — | ❌ 覆盖宿主的"停止"按钮（平台层） |
| 落盘产物 | ✅ 经 pre-commit / CI 拦截 | ❌ 阻止绕过钩子的写入 |

**关键边界**：Tier A 只在宿主**提供了钩子**时才成立；Tier B 永远只是提示词。
没有任何一层能"保证"模型不发散——能保证的只有"发散产物进不了主干"。

## 迭代记录

| 版本 | 日期 | 变更 |
|:--|:--|:--|
| v1.0 | 2026-06 | 初始发布：10 条偏航信号 + 工程化 vs 渐进式 |
| v1.1 | 2026-06 | 前端元数据修正 |
| v1.2 | 2026-07-04 | S4/S6/S10 增强；新增 S11；新增 related-project checklist |
| v1.3 | 2026-07-12 | S9 硬截断 + S9-INPUT；新增 Limitations；新增 Release Governance；Export Audit 脚本化 |
| **v1.4** | **2026-09-17** | **平台中立化重构**：信号按可执行性分 Tier A/B；新增 Tier A 规范契约（决策语义/scan ledger/判定顺序/S5 算法/适配器接口/记录格式）；**修复 S5 的 `://` 注释盲区**；**修复转义正则无法解除 S4 的缺陷**；移除未绑定的 S11；把不可证伪的效果声明换成可核对项；`triggers` 补全；安装说明去平台绑定 |

## Credits / 致谢

Created by **Q博士** / **Q博士创作**。
基于 40+ 天高频 AI 协作中观察和系统化的真实跑偏模式。
v1.4 的分层契约与 S5 盲区修复，来自一次真实的跨平台移植
（把本协议接入一个基于 Cordis 的宿主时的实测结果）。

Companion to [Andrej Karpathy's Four Rules](https://github.com/forrestchang/andrej-karpathy-skills).
