# Cosmos.ai — Q博士 对外公开库 / Public library

> Q博士（信息↔决策第三空间治理系统）对外的能力公开入口。本库只放**脱敏后的派生知识**，不含内部治理原文。
> The public capability library of Q博士 (the information↔decision third-space governance system). Only **desensitized derivative knowledge** lives here — no internal governance source text.

一句话：**不是发布「一个现成的智能体」，而是发布「能长出它的治理系统」+「已验证的方法论资产」。**
In one line: we do not ship *a ready-made agent* — we ship **the governance system that can grow one**, plus **validated methodology assets**.

## 目录导航（按对外能力分类）/ Directory map (by outward capability)

| 目录 · Directory | 你能拿到什么 · What you get | 适合谁 · For whom |
|:--|:--|:--|
| [`decision/`](decision/) · 决策资产 | 可验证的**决策单元**（五元组） | 要做判断的人 · those making decisions |
| [`skill/`](skill/) · 技能 | 可安装使用的**技能**（每技能一子目录） | 想让 AI 立刻具备某能力 · want instant capability |
| [`expert/`](expert/) · 专家 | **专家角色**包（含多角色协作协议） | 需要专业角色视角 · need a specialist role |
| [`methodology/`](methodology/) · 方法论 | 可迁移的**方法论**（含案例） | 想学这套治理方法 · want to learn the method |
| [`whitepaper/`](whitepaper/) · 白皮书 | **白皮书**与理论 | 想读懂原理 · want the theory |

## 快速开始 / Quick start

| 我想… · I want to… | 去哪 · Go to |
|:--|:--|
| 直接用某个能力 · use a capability | [`skill/`](skill/) → 选技能子目录 → 按其 README 安装 |
| 要一个可验证的决策包 · get a verifiable decision package | [`decision/`](decision/) |
| 了解这套系统 · understand the system | [`whitepaper/`](whitepaper/) |
| 参与贡献 · contribute | [CONTRIBUTING.md](CONTRIBUTING.md) |

## 回传（外部 → Q博士）/ Feedback (external → Q博士)

本库**不另设回传目录**——回传是动态事务，不是静态文件，走仓库原生协作面：
This library has **no dedicated feedback folder** — feedback is a dynamic transaction, not a static file. Use the native collaboration surfaces:

| 回传类型 · Type | 通道 · Channel |
|:--|:--|
| 问题 / 建议 · Issues | [Issues](../../issues) |
| 贡献技能 / 代码 · Contributions | Pull Request（评审后并入对应能力域） |
| 开放讨论 · Discussion | [Discussions](../../discussions) |

Q博士 对回传的**内部蒸馏**存于治理侧，**不进入本库**；库内仅保留脱敏致谢 [CONTRIBUTORS.md](CONTRIBUTORS.md)。

## 边界 / Boundaries

- 只含**脱敏派生知识**——内部宪法 / 治理原文不外泄
- 每技能独立子目录 `skill/<skill-name>/`，互不污染
- 发布走标准化流程：脱敏 → 自闭环四件 → 出口审计 5 项
- 决策资产迁移须有 `TransferEvent`（边界切面 + 不变量 + 接收方证据卡），不以「文件已投递」冒充「已采纳」

## License

MIT — 见 [LICENSE](LICENSE)
