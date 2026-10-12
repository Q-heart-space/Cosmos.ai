# AI-Drift-Guard

A portable, self-check protocol for AI agents to detect drift before acting.
- [SKILL.md](SKILL.md) — the full signal protocol
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to file issues or suggest improvements
- [CHANGELOG.md](CHANGELOG.md) — version history
License: MIT


## Limitations / 限制：S9 的三种“停止”能力

**S9 的技能规则不等于平台级取消生成。** 停止工具调用、禁止继续输出和中断模型推理是三种不同能力；“零输出”不能作为推理已取消的证据。

| 能力 | 含义 | 技能与宿主的边界 |
|:--|:--|:--|
| 停止工具调用 | 不再发起或派发后续工具调用 | 提示词要求模型停止调用；只有宿主接入对应门禁才能强制拒绝尚未派发的调用。不能据此声称已取消正在执行的工具，也不能撤销已发生的副作用。 |
| 禁止继续输出 | 不输出文本、确认语或 emoji | 技能规则约束模型输出，但不保证停止指令在当前生成中即时被处理。当前协议 A.7 的宿主 pre-step `reject` 可在步骤开始前拒绝生成；它不是对已开始推理的中断。 |
| 中断模型推理 | 取消已开始的推理 / 深度思考 / 生成 | 超出技能层能力，需要模型 / 推理服务层与客户端层共同支持取消协议；技能无法替代平台停止按钮。 |

**EN:** Stopping future tool dispatch, suppressing output, and cancelling in-flight inference are separate capabilities. Prompt rules cannot cancel inference. A host pre-step rejection prevents a new step from starting; it does not interrupt inference already in progress.

### 已验证记录与版本 / Evidence and versions

[Issue #1](https://github.com/Q-heart-space/Cosmos.ai/issues/1) 记录了以下历史修复与测试结论：

- `v1.2.0-ext` 在 [bcec0e4](https://github.com/Q-heart-space/Cosmos.ai/commit/bcec0e4) 中加入“停止所有工具调用、不输出文本”的 S9 规则。
- [7bfdf4c](https://github.com/Q-heart-space/Cosmos.ai/commit/7bfdf4c)、[5aaa338](https://github.com/Q-heart-space/Cosmos.ai/commit/5aaa338)、[3edc511](https://github.com/Q-heart-space/Cosmos.ai/commit/3edc511) 进一步强调零输出：不输出 emoji、“OK”或“got it”。这些提交强化的是规则，不是平台级取消能力。
- [用户测试后的结论](https://github.com/Q-heart-space/Cosmos.ai/issues/1#issuecomment-4949844280)：WorkBuddy 的停止按钮未能中断模型推理阶段；技能可约束输出，不能真正取消该阶段的生成。该结论限于 Issue 所记录的测试环境。
- [平台讨论](https://github.com/Q-heart-space/Cosmos.ai/issues/1#issuecomment-4949930787) 还提及 Claude、Kimi、ChatGPT、WorkBuddy 的相似限制。这是该评论中的记录，不代表本库对各平台所有版本、模式或当前实现的独立验证，也不据此断言“所有平台都无法中断”。

当前 [SKILL.md](SKILL.md) 保留 `1.5.0-ext` 版本及 S9 的宿主 pre-step 规范；历史 `v1.2.0-ext` 修复与当前生成前门禁都不应被描述为“已实现可中断推理”。

### 当前可行的缓解方式 / Mitigation

- 使用 S9 停止词要求停止后续工具调用并保持零输出；只有模型 / 宿主实际收到并处理该指令时，规则才有机会生效。不要将无文本输出视为后台计算已停止。
- 宿主支持时接入 A.7 的 pre-step `reject`，在下一步骤开始前拒绝生成；工具 dispatch 前门禁可阻止后续调用。分别验证这些拦截点，不以“安装了技能”代替验证。现有 [DSH 集成](../../integration/units/ai-drift-guard/README.md) 明确未强制执行 S9，不能假定所有适配器已接入。
- 将长任务拆为较短步骤，在步骤间设置用户确认点，减少停止请求到可处理边界之间的工作量；这只能缓解，不能取消当前推理。
- 需要立即停止时，使用宿主提供的原生取消机制，并核对任务和工具状态；若当前宿主不能中断推理，只能等待该轮结束后再继续或重新发起任务。已运行的工具须按其自身取消能力单独处理。
- 真正中断进行中的推理需要平台改进：客户端向推理层发送取消信号，推理层支持并处理该信号。Issue #1 将此列为平台层需求，超出本技能修复范围。
