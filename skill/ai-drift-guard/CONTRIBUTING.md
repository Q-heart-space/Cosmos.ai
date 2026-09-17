# Contributing to AI-Drift-Guard / 参与指引

Thanks for your interest in AI-Drift-Guard. 本技能位于
[`Cosmos.ai`](https://github.com/Q-heart-space/Cosmos.ai) 的 `skill/ai-drift-guard/`。

## How to give feedback

- Open a [GitHub Issue](https://github.com/Q-heart-space/Cosmos.ai/issues)
- Pick the appropriate template: **Bug report** or **Feature request**
- Include a concrete example: what you said, what the agent did, and what you expected.

## Scope

本目录只包含协议的**可移植版本**。Q博士 内部的治理工具不在此发布。

协议本体必须保持**平台中立**：不得出现任何具体 AI 平台的目录结构、钩子名称或 SDK。
平台差异一律写进 `references/adapters.md` 的适配器，不进 `SKILL.md`。

## 改动 Tier A 时必做

`references/drift-guard-core.mjs` 是 Tier A 的**唯一参考实现**，
`references/template_validator.py` 必须与它保持一致。两者判定漂移即为 bug。

```bash
node references/selftest.mjs          # 必须 ALL GREEN
node references/drift-guard-core.mjs check <file.html>
python references/template_validator.py <file.html>
```

提交前请贴出 `selftest.mjs` 的输出。**"改了逻辑"不算数，跑绿才算。**

## Code of conduct

Be constructive, be specific, and remember the protocol itself is a self-check:
if you spot a rule the maintainer is violating, file it as a bug.
