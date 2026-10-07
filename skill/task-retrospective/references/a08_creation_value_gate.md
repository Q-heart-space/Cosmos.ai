# 🆕 Step A0.8：交付物创建价值门（阻断级）

## 🆕 Step A0.8：交付物创建价值门（新增·2026-07-13·CL-44·Phase 3）

> ⚠️ **来源**：four-mode-retrospective 废弃裁决暴露元教训——"建交付物前缺'该不该存在'门"。本门禁在 FDG（A0.7·"设计够深吗"）之前先回答"该不该存在"——防止越进化越膨胀、什么都创建。

**触发时机**：任何新建脚本/技能/规则/自动化/宪法文件/概念注册前。

**执行步骤**：

1. 运行创建价值门：
   ```bash
   python scripts/preflight_check.py --check creation_value --file <目标文件路径>
   ```

2. 按三元判定决策：
   - `score < 50` → 🛑 block：拒绝创建，检查替代方案（复用现有交付物）
   - `50 ≤ score < 70` → ⚠️ review：边界确认，按 R-Level 找对应人类审批
   - `score ≥ 70` → ✅ pass：继续，按 R-Level 执行对应处置层级

3. preflight_check 是真阻断路径（区别于 pre_write_check 的 advisory max P1）。block 时 exit 1，阻断后续流程。

**与 A0.7 的关系**：
- A0.7（FDG）：问「设计够深吗」——决定功能的**质量深度**
- A0.8（创建价值门）：问「该不该存在」——决定交付物的**存在正当性**
- 两者互补：先过 A0.8（该不该建）→ 再走 A0.7（够不够深）

**执行规则**：
- 未运行创建价值门就新建交付物 → 视为违规，复盘时必须标注
- 复盘时检查：本次的新增交付物是否通过了创建价值门？blocked 的是否有替代方案？
- 参考技能：`pre_creation_gate`（D2·core-governance）

---


