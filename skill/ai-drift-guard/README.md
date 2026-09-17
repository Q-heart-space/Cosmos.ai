# AI-Drift-Guard

A portable, platform-neutral self-check protocol for AI agents — and, for the
part that can be checked mechanically, a real runtime gate.

> 一份平台中立的 AI 跑偏自检协议；其中**可机械判定**的部分可以变成真正的运行时门禁。

## Layout / 文件结构

```
skill/ai-drift-guard/
├── SKILL.md                     # 协议本体（Tier A 规范契约 + Tier B 提示清单）
├── references/
│   ├── drift-guard-core.mjs     # Tier A 参考实现（零依赖，可当 CLI 独立跑）
│   ├── adapters.md              # 宿主适配器契约 + 实例（DSH / pre-commit / 其他）
│   ├── template_validator.py    # S5 的 Python 实现（与 core 同步）
│   └── selftest.mjs             # 可复现的自检；提交前必须 ALL GREEN
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

## 三层用法 / Three ways to use it

| 你的宿主能力 | 得到什么 |
|:--|:--|
| 只有"技能目录" | 只有 **Tier B**（提示词自检）生效 |
| 有工具调用钩子 | **Tier A**（S5/S4 真拦截）+ Tier B，见 `references/adapters.md` |
| 只想要产物约束 | 把核心当 **pre-commit / CI** 用，**不需要任何 AI 平台** |

```bash
# 平台中立：约束产物，不约束模型
node references/drift-guard-core.mjs check path/to/page.html

# 自检
node references/selftest.mjs
```

## 核心主张 / What it does not claim

- Tier B 信号（S1/S2/S3/S6/S7/S8/S9/S10）**没有强制力**。它们是提醒，不是中断。
- 只有 Tier A（S5 模板占位符泄漏、S4 全局规则文件门禁）是可机械判定的。
- 协议本体**不含任何平台的路径、钩子名或 SDK**——这是 v1.4 的重构目标。

## License

MIT — see [LICENSE](LICENSE).
