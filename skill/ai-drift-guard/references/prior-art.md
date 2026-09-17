# 先例调查：这个问题别人做到哪一步了

本文件的目的不是"致敬"，而是**避免重复发明**，并让读者知道遇到同类问题该先用哪个现成方案。

> **结论先说**：本技能的**机制几乎没有新东西**。
> 它的价值不在"10 条信号"（那是这个领域的公共知识），而在
> **第一原理分层**（[`first-principles.md`](first-principles.md)）和**不撒谎的边界声明**。

---

## 1. 接缝已经被标准化了

Claude Code 的 hook 体系（`PreToolUse` / `PostToolUse` / `UserPromptSubmit` / `Stop` / `SessionStart`）
与 DSH 的钩子面几乎一一对应，参见 [`first-principles.md`](first-principles.md) 附录。

生态索引：[awesome-claude-code-hooks](https://github.com/loqimean/awesome-claude-code-hooks) ——
收录了各 runtime 的事件目录与真实实现。

**含义**：插座是平台装的，而且是公开的。任何"跑偏守卫"都只能做插上去的电器，
**不可能带来平台能力之外的东西**。

## 2. 逐信号找先例

| 本技能信号 | 已有的成熟实现 |
|:--|:--|
| S3 破坏性操作前拦截 | [kenryu42/cc-safety-net](https://github.com/kenryu42/cc-safety-net)（跨 Claude Code / Codex / Cursor / Gemini）、[dwarvesf/claude-guardrails](https://github.com/dwarvesf/claude-guardrails)、[yurukusa/cc-safe-setup](https://github.com/yurukusa/cc-safe-setup) |
| S5 产物校验 | [Sting25/ai-coding-rules-scaffold](https://github.com/Sting25/ai-coding-rules-scaffold) 的 forbidden-patterns + pre-commit + CI |
| **S8 不许提前收尾** | [blader/taskmaster](https://github.com/blader/taskmaster) 的 `Stop` hook：「keeps the agent working until all plan items and user requests are fully complete」 |
| S1 / S2 / S7 提示词层 | [severity1/claude-code-prompt-improver](https://github.com/severity1/claude-code-prompt-improver) 的 `UserPromptSubmit` |
| S10 文件膨胀 | ai-coding-rules-scaffold 的 **500 行硬上限**（比"≥2 个文件"准得多） |
| 独立复核 | [first-fluke/oh-my-agent](https://github.com/first-fluke/oh-my-agent) 的 stop-hook gates + independent judges |
| 保密（不在本技能范围） | [JeongJaeSoon/agent-guard](https://github.com/JeongJaeSoon/agent-guard)、[DataFog/datafog-python](https://github.com/DataFog/datafog-python) |

同类技能集合：[awesome-agent-skills](https://gitcode.com/GitHub_Trending/aweso/awesome-agent-skills)（含 "Anti-over-engineering skill with 5 variants and 10 platforms"）、
[aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills)。

本技能致谢的 [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills)
是**提示层**的同类实践。

## 3. 最该对照的一个：ai-coding-rules-scaffold

它和本技能的野心高度重合，而且更成熟。逐条对照：

| 它有的 | 本技能曾有 / 现状 |
|:--|:--|
| 两层强制（pre-commit + CI），**共用同一套 `lib/check-*` 脚本**，两层不可能漂移 | 本技能 v1.4 才写下"适配器不许重写核心"——同一个想法，晚了一步 |
| **agent 无关**：走 [`AGENTS.md` 标准](https://agents.md)，跨 Cursor / Claude Code / Aider / Codex | 本技能 v1.4 才去平台绑定；社区**已有标准答案** |
| `scaffold-doctor.sh` / `verify`：**证明守卫真的武装了** | 本技能 v1.5 起用 `boot.jsonl` + `selftest.mjs`，是雏形 |
| 逃生阀：行内 `# scaffold-allow`、按路径配限、`.scaffold.toml` | 本技能只有"先 grep 再写" |
| **明确写出它不解决什么** | 本技能 v1.3 起才有 Limitations |
| 失效模式分析来自**一个真实生产故事** | 本技能的来源是"40+ 天观察"，说服力更弱 |

它公开的四个失效模式（跨会话模式不一致 / 文件无界增长 / 调试语句静默上线 / 禁用模式复发）
与本技能的痛点表高度重叠——但它是从**后果**出发的，本技能是从**现象**出发的。

## 4. 结论：什么是不重复的

本技能**不应**继续扩张信号数量——那个赛道已经拥挤，而且别人做得更细。

它剩下的差异化只有三点：

1. **第一原理分层**：解释"什么能强制、什么只能提醒、什么永远做不到"。
   这是**否定性知识**——它省掉别人白费力气的尝试。市面上真正缺的是这个。
2. **中文语境优先**。
3. **不撒谎的边界声明**：明写"技能是指令，不是系统钩子"。同类项目基本不敢写这句。

## 5. 给读者的选型建议

| 你想解决的问题 | 先用什么 | 而不是 |
|:--|:--|:--|
| 别让 AI 写危险命令 | 平台沙箱 + 权限策略 + cc-safety-net | 本技能 |
| 别让 AI 无界改文件 | 平台 plan mode / 只读模式 | 本技能 |
| 产物别带泄漏/密钥 | pre-commit + CI（ai-coding-rules-scaffold） | 本技能 |
| 别提前收尾 | todo 工具 + Stop hook（taskmaster） | 本技能 |
| 项目规矩 | `AGENTS.md` | 本技能 |
| **想搞清楚"哪些规则值得写成闸门"** | **本技能的 [`first-principles.md`](first-principles.md)** | —— |
