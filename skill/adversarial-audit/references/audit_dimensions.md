> 🆕 孤儿文件标注（2026-09-16 技能审阅）：本文件未被 SKILL.md 或 references 引用·可能为历史遗留/已废弃·保留待清理。

# 十一维审计详细参考（audit_dimensions.md · 0A-R 重建）

> 由 8 维扩展为 11 维（对齐 SKILL.md v3.19「Step 3: 11维审计」）。
> 新增：⑨宪法模板完整性 ⑩第一原理推导完整性 ⑪名称语义准确性（v3.1 扩展）。

## 11维×4层 交叉点矩阵

| 维 \ 层 | C Constitution | G Governance | S Scripts | A Automation |
|:--|:--|:--|:--|:--|
| ① 代码完整性 | 宪法文件语法 | 治理文件语法 | `test_meta_pipeline 6/6` | E2E自动验证 |
| ② 数据一致性 | 术语表计数一致 | index↔JSON同步 | lifecycle/source/maturity | daily_tasks align |
| ③ 接线通电 | 宪法文件 wiring | governance wiring | **daily_tasks调度≠空** | closure调度验证 |
| ④ 版本对齐 | 宪法版本号 | 治理版本号 | 脚本头vs变更 | version_drift 0 |
| ⑤ 宪法一致 | §九-A L5前提 | CFM T-3-834 Done | 术语表=registry | — |
| ⑥ 管线验证 | — | bridge scan | closure pileup | term_registry_sync |
| ⑦ 杀伤链 | — | reclassify | conversion_rate | L2→L3 pipeline |
| ⑧ 落地通电 | **prevention工程化** | **solution通电** | **artifacts完整** | **L5真实性** |
| ⑨ 宪法模板完整性 | 模板字段齐全 | 模板字段齐全 | 头字段齐全 | — |
| ⑩ 第一原理推导完整性 | 结论锚定第一定律 | 决策可溯源 | 判据有第一原理 | — |
| ⑪ 名称语义准确性 | 概念命名准确 | 术语语义准确 | 脚本名符职责 | — |

## ⚠️ 通电≠PASS（保留）

清单验证「通电（被调度）」不验证「PASS（内容通过）」。对抗审计必须区分两层：
- 架构层验证（通电）：工具是否被调度？→ **维③**
- 内容层验证（PASS）：工具输出是否通过？→ **维⑧**

## 每层检查命令（保留）

| 层 | 命令 |
|:--|:--|
| C | `python scripts/constitution_steward_gate.py --check` |
| G | `python scripts/doc_script_version_aligner.py --check --json` |
| S | `python scripts/pattern_to_task_bridge.py --scan --json` |
| A | closure_verification P0=0·conversion_rate >15% |
