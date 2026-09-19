# detector-signal-triage 技能边界与转交链

> 2026-08-31·新增技能标准化补齐（建前查存量 + 职责正交 + 路由登记）

## 一、为什么需要（必要性·查存量结论）

Q博士 现有 5 个审计类技能，审计对象各不相同，**无一覆盖"检测器报警值本身是真是假"**：

| 技能 | 审计对象 | 是否审查检测器报警值 |
|:--|:--|:--|
| adversarial-audit | AI 的产出（≥3 Agent 执行结果） | ❌ |
| infrastructure-audit | 存量（建前查存量·全空间查询取证） | ❌ |
| governance-deep-audit | 治理体系结构性缺陷（路由/链路/声明） | ❌ |
| constitution-steward | 宪法文件格式与内容合规 | ❌ |
| cross-space-governance-steward | 外部空间治理补强 | ❌ |
| **detector-signal-triage** | **检测器报出的异常值**（红灯/0分/孤立项） | ✅ **本技能** |

**定位**：分诊前置层——其他审计技能的**上游**。先判报警真假，再决定是否需要治理、转交给谁。

## 二、转交链（职责正交）

```
检测器报警（红灯/0分/CRITICAL/孤立项）
        │
        ▼
  [detector-signal-triage 分诊]
        │
        ├─ ① 模型缺陷 ──────► 修检测器度量模型（补缺失维度）·无需转交
        ├─ ② 口径缺陷 ──────► 修检测器实现（补引用形态/并真相源）·无需转交
        │
        └─ ③ 真问题 ────────► 转交下游：
                                ├─ 需查存量/影响面 ──► infrastructure-audit
                                ├─ 体系结构性缺陷 ──► governance-deep-audit
                                ├─ 涉及宪法文件 ────► constitution-steward
                                ├─ 跨空间传播 ──────► cross-space-governance-steward
                                └─ 需对抗验证产出 ──► adversarial-audit
```

## 三、触发词与路由（铁律C 精确路由）

- 本技能触发词：`检测器报警` / `红灯深挖` / `0分假零` / `孤立脚本` / `覆盖率CRITICAL` / `指标不可信` / `why is this red`
- 与相邻技能**无触发词冲突**（adversarial-audit 用"对抗式审查/对抗审计"；infrastructure-audit 用"查存量"；governance-deep-audit 用"治理深审"）
- 路由表：由 `sync_skill_registry.py` 自动生成 `task-router/references/skill_routes.json`

## 四、标准化创建流程（新增技能必走）

1. **建前查存量**（infrastructure-audit / 铁律BR）：确认无同职责技能·或明确写出职责正交性（本文档）
2. 写好 `SKILL.md` frontmatter（name / description / agent_created）
3. **运行 `python scripts/sync_skill_registry.py`** → 自动同步 4 处交付物（注册表文档 / asset_registry / FILE_MANIFEST / task-router 路由表）
4. 落地三验：真跑一次触发场景·确认路由可达

> ⚠️ 本次首轮创建**直接 Write 未查存量**（流程违规）·本文件为补齐动作。
