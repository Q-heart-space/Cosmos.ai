# decision/ — 决策资产 / Decision assets

> **Q博士 传播的不是「内容」（文档/代码/报告），而是已对齐的「决策单元」。**
> What Q博士 distributes is not *content* — it is **aligned decision units**.

来源 / Source：本质定位 §1.9.7（差异化定位·传播已对齐的决策单元）

## 决策单元 = 五元组 / A decision unit = 5-tuple

| 元 / Element | 含义 / Meaning |
|:--|:--|
| 决策依据 / Basis | 结论从何而来 · where the conclusion comes from |
| 替代方案评估 / Alternatives | 还评估过什么 · what else was evaluated |
| 验收标准 / Acceptance | 怎么算成立 · what counts as valid |
| 证据链 / Evidence chain | 可反查 · traceable & re-checkable |
| 授权链 + 收据链 / Authority + Receipt | 人类授权 + 可复算收据 · human authority + recomputable receipt |

**五项不变量 / Five invariants**

人类主权（Human sovereignty）· 接收者可理解（Comprehensible）· 受限可逆（Bounded & reversible）· 适配可迁移（Transferable）· 声明可证（Provable）

## 行业维度 / Industry dimension

决策单元**同时具备行业属性与共性**——面向不同行业提供不同的决策单元，同时**抽取跨行业可复用的共性**。
Decision units carry **both industry-specific attributes and cross-industry commonalities**.

```
decision/
├── common/        # 共性 · 跨行业可复用的通用决策单元 / cross-industry reusable units
└── <industry>/    # 行业专属 / industry-specific — ipc / maritime / fae / ...
```

**抽取共性原则 / How commonality is extracted**：当 ≥2 个行业出现同一决策结构（同依据／同替代集／同验收标准），该结构**上提为 `common/`**，行业目录只保留差异部分——避免「每个行业各写一份」。
When ≥2 industries share the same decision structure, it is promoted to `common/`; industry folders keep only the differences.

## 收录判据 / Inclusion criteria

| 条件 | 说明 |
|:--|:--|
| **① 五元组齐** | 决策依据 ＋ 替代方案评估 ＋ 验收标准 ＋ 证据链 ＋ 授权链/收据链——缺一不收 |
| **② 证据可反查** | 证据链里的每条都能被独立复算——不可反查的不收 |
| **③ 有授权** | 能指出人类授权的那一次决定——无授权不收 |
| **④ 可理解** | 接收者不需要内部上下文就能读懂 |
| **⑤ 已脱敏** | 剥离内部路径、主机名、凭据与内部代号 |

## 收什么 · 不收什么 / What belongs here

| 收 | 不收 |
|:--|:--|
| 已对齐的决策单元（五元组齐） | 单条结论、单份文档 |
| 跨行业共性结构（≥2 行业同构 ⇒ 上提 `common/`） | 只对一个行业成立的差异（留在行业目录） |
| 可迁移的判断框架 | 一次性会议记录 |

## 怎么进 / How to add

1. 判「这条决策属共性还是行业专属」：**≥2 个行业出现同一决策结构 ⇒ 上提 `common/`**；否则进 `<industry>/`。
2. 按五元组写成一个决策单元（依据 → 替代 → 验收 → 证据链 → 授权/收据）。
3. 跑一次脱敏检查（⑤），确认无内部痕迹。
4. 走标准发布流程（见仓库根 `CONTRIBUTING.md`），过域门禁后才进本目录。

> **本目录现况 / Current contents**：骨架已就位（`common/` 与行业目录约定如上）；
> 首批决策单元按上面四条判据逐个收录，**每条都须五元组齐**。

