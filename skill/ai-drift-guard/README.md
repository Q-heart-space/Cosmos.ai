# AI-Drift-Guard

A portable, platform-neutral self-check protocol for AI agents — and, for the
part that can be checked mechanically, a real runtime gate.

> 一份平台中立的 AI 跑偏自检协议；其中**可机械判定**的部分可以变成真正的运行时门禁。

## Layout / 文件结构

```
skill/ai-drift-guard/
├── SKILL.md                     # 协议本体（Tier A 规范契约 + Tier C 提示清单）
├── references/
│   ├── first-principles.md      # 【先读】为什么是三层，以及什么永远做不到
│   ├── adoption.md              # 采用指南：你可能不需要本技能
│   ├── prior-art.md             # 先例调查：哪些问题别人已经解决了
│   ├── drift-guard-core.mjs     # Tier A 参考实现（零依赖，可当 CLI 独立跑）
│   ├── adapters.md              # 宿主适配器契约 + 实例（DSH / pre-commit / 其他）
│   ├── template_validator.py    # S5 的 Python 实现（与 core 同步）
│   └── selftest.mjs             # 可复现的自检（24 项）；提交前必须 ALL GREEN
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

## 三层分层 / Three tiers

一条规则能有多硬，**取决于它能挂在 agent loop 的哪个接缝上**，而不是写得多好。
完整推导：[`references/first-principles.md`](references/first-principles.md)。

| Tier | 机制 | 保证 | 信号 |
|:--|:--|:--|:--|
| **A 硬拦截** | dispatch 前拒绝、步骤拒绝 | 动作**不会发生** | S5、S4、S9 |
| **B 确定性注入** | 在对的时机把提醒放进上下文 | 提醒**必然在场** | 本协议未规范 |
| **C 纯提示** | 只写进上下文 | 读不读全看模型 | S1 S2 S3 S6 S7 S8 S10 |

## 三种用法 / Three ways to use it

| 你的宿主能力 | 得到什么 |
|:--|:--|
| 只有"技能目录" | 只有 **Tier C** 生效——技能本身就是缝1 |
| 有工具／步骤钩子 | **Tier A**（S5/S4/S9 真拦截），见 `references/adapters.md` |
| 只想要产物约束 | 把核心当 **pre-commit / CI** 用，**不需要任何 AI 平台** |

```bash
# 平台中立：约束产物，不约束模型
node references/drift-guard-core.mjs check path/to/page.html

# 自检
node references/selftest.mjs
```

## 核心主张 / What it does not claim

- Tier C 信号（S1/S2/S3/S6/S7/S8/S10）**没有强制力**。它们是提醒，不是中断。
- 只有 Tier A（S5 模板占位符泄漏、S4 全局规则文件门禁、S9 说停就停）是可机械判定的。
- Tier B（确定性注入）本协议**只给机制、不规定规则**——加不加、加哪些，由宿主自己判断。
- 协议本体**不含任何平台的路径、钩子名或 SDK**。
- **你可能根本不需要它**：见 [`references/adoption.md`](references/adoption.md)。
- 哪些问题别人已经解决了：见 [`references/prior-art.md`](references/prior-art.md)。

## License

MIT — see [LICENSE](LICENSE).
