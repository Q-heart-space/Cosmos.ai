---
name: report-verify
version: 1.1.0-ext
distribute_external: yes
publish_face: public
agent_created: true
depends: []
suggests:
  - report-content-coherence
  - report-deliver
  - write-report
  - industry-report-studio
triggers:
  - apq-report-verify
  # 🆕 2026-11-09 旧名保留（通用化改名兼容）
  - 格式校验
  - apq-format-verify
  - 格式验证
  - 排版校验
  - 格式检查
description: 全系报告**格式**自动化校验（也作 apq-format-verify）。30项脚本校验+品牌视觉排版规范。仅在内容定稿后、构建PDF前调用一次。🛑 本技能仅检查**格式**（排版/品牌色/锚点/图表编号/分隔符等）。内容逻辑自洽请用 @report-content-coherence。触发词见下方「触发机制」。
contract: "@contract:skill scripts:_report_validator.py,scan_129_channels.py"
circuit: ⑦自审
space_scope: universal
reuse_depth: org-parameterized
scope_axis: business
layer: 叶·格式校验
usage_class: 业务类
trust_level: auto
deprecated: false
updated_at: 2026-08-13
---

## 🏛️ 宪法对齐（2026-07-15 补·CONSTITUTION_CONCEPT_COVERAGE 闭环）

> 本技能须与 Q博士 宪法级文件保持**内容同步**；宪法变更→本技能**事件驱动级联更新**（内容同步规则）。

- **AI空间（Q博士 治理空间概念）**：本技能运行于 Q博士 治理空间（第三空间）内，输出须遵循跨空间本体论五通道（Harvest-Internal/Harvest-External/Distribute-Internal/Distribute-External/Consistency）语义约束；跨空间输出须标注 space_scope。
- **分析报告归档**：本技能的产出若为分析报告，按接收方的**治理文件归档流程**落位（🆕 2026-11-09 对外化：原引用内部专有方法论名 ⇒ 改为通用表述·对接收方不引入内部术语）。
- **状态断言前置审查规则 状态断言前置审查**：技能在输出"未找到""不存在""无变化"等否定/肯定断言前，须执行取证三问（查源→交叉验证→证据锚定）。
- **多维审核框架 十维审核框架**：本技能的关键判断须覆盖十维中至少与技能域相关的维度（形式/内容/结构/关联/可验证），不得仅凭单一维度下结论。
- **数据源权威性层级规则 数据源权威性层级**：多源数据冲突时，技能须优先采信 L0 权威源（官网/datasheet）而非 L2/L3 推断或旧报告。
- **取证规则 数据+凭证双中枢**：本技能的输入数据须标注来源权威层级，优先使用 Data-全局数据仓库（双中枢）而非未经校验的外部 API 缓存。
- **P1-12 批判吸收**：引用外部权威或 AI 建议时，须执行 `critical-absorption-check` 批判吸收流程——不盲信、先验证、再吸收。
- **P1-13 提问升级**：面对模糊/宽泛/低信号问题时，须主动升级为高信号结构化提问（九维递进追问法/分层决策锚定），不得直接执行低质量指令。



# 报告格式校验（通用版）

> **适用范围**：全系报告。含海事工控机研究报告、类工控业务战略报告、客户分析报告、数据看板报告等。
> **调用时机铁律**：仅在内容定稿后、构建 PDF 前调用一次。禁止在撰写迭代阶段调用——每改一次内容就验一次格式 = 滚雪球返工。
> **单一事实来源（🆕 2026-11-09 组织参数化）**：品牌色读取 **`business:<域>/<组织>/brand/brand_colors.json`**（**组织级唯一**），禁止硬编码色值；本体只留 `references/brand_colors.template.json` 中性模板。🛑 配置缺失 ⇒ 按中性灰校验，**不猜任何组织品牌色**。

## 🔔 触发机制（三路径）

| 路径 | 如何触发 | 适用场景 |
|:--|:--|:--|
| **自动匹配** | 用户说触发词时AI自动调用 | 日常使用——用户无意中说了触发词 |
| **主动建议** | 检测到报告MD有 `**版本**：v*` 且内容已修改 → AI主动提示"需要运行格式校验吗？" | 用户修改完报告但不知道要校验 |
| **手动选择** | 用户在技能列表选择本技能，或输入"校验"/"report-verify" | 用户明确知道需要校验 |

### 触发词（覆盖正式与口语）

**直接触发**（说了就调）：报告校验、检查报告、核查报告、校验错误、验格式、verify、格式检查、格式校验、验证格式、格式有没有问题、**格式校对、校对格式**

**主动建议**（满足条件时提示）：报告定稿、最终版本、可以发布了、定稿了、准备发布、可以交付了

**全文校对 / 校对全文**：→ 请先用 @report-content-coherence 做内容校对，内容校对通过后再调本技能做格式校验。两个技能按顺序执行，不可同时触发。

**手动调起**：用户在技能列表选择 → 等同于触发 → AI直接运行Phase 1校验

> ⚠️ **重要**：当用户说"修订"/"修改"/"排查"/"统一格式"/"修复"时，如果技能未被自动匹配，AI应在完成修改后主动提示："报告内容已修改，是否需要运行 `report-verify` 格式校验？"

## 核心工作流

> **🛑 强制执行**：触发后必须运行 `python _report_validator.py --md "报告文件.md"`，**禁止口头声称"通过"**。必须贴脚本输出证明。

```
内容定稿 MD
      ↓
Phase 0: 前置确认（< 10秒）
  · 从当前会话上下文确认 @report-content-coherence 13项已在本会话中 PASS
  · 🛑 coherence 未在本会话执行或 FAIL → 禁止进入格式校验 → 先调 coherence
  · ⚠️ TOC映射/编号一致性由 coherence #2 负责，本Phase不重复检查
      ↓ 通过
Phase 1: 30项自动校验（门禁，每次必跑）
  · 运行 _report_validator.py --md "报告文件.md" --type <报告类型>
  · 任何一项不通过 → STOP → 修复 → 重跑
  · 🛑 必须贴脚本输出
      ↓ 通过
Phase 2-6: 按需执行（编号重排/锚点/图表/摘要/逻辑）
      ↓ 全部通过
  → 交接给 @skill:report-deliver
```

#### 🆕 MD 表格列数自检（2026-06-23 channel-report 错误复盘）

> ⚠️ **事故**：`scan_129_channels.py` 生成的 MD 表格表头 5 列但分隔行仅 4 列，导致渲染错乱。

**全局预防**：所有生成 MD 报告的脚本，写入文件后**必须**运行表格列数对齐校验：

```python
# 🛑 写入后自检：表格列数对齐
import re
table_errors = 0; header_cols = 0; in_table = False
for i, line in enumerate(report_lines):
    stripped = line.strip()
    if stripped.startswith('|') and '|' in stripped[1:]:
        cells = [c.strip() for c in stripped.split('|')[1:-1]]
        if all(re.match(r'^[\s:|-]+$', c) for c in cells):
            if header_cols != len(cells):
                print(f'❌ 表格列数不匹配(行{i+1}): 表头{header_cols}列, 分隔行{len(cells)}列')
                table_errors += 1
            continue
        if not in_table: in_table = True; header_cols = len(cells)
        continue
    if in_table and not stripped.startswith('|'): in_table = False; header_cols = 0
```

**适用脚本**：`scan_129_channels.py`、`regenerate_md.py`、以及所有含 `report_lines.append('|...')` 的 MD 生成脚本。


## 报告类型参数

| 类型 | 适用场景 | 专用检查 |
|:--|:--|:--|
| `maritime` | 海事工控机研究报告 | 五篇完整性、竞品排列顺序、篇章编号 |
| `strategy` | 战略报告（类工控等） | 执行摘要编号连续性、▓过渡标记一致性、决策框架完整性 |
| `data` | 数据分析报告 | 图表编号系统、数据来源标注、统计汇总格式 |
| `client` | 客户报告 | 客户名一致性、敏感信息脱敏、客户画像格式 |

## 核心规则

### 1. 调用约束
- **仅内容定稿后调用一次**：避免内容-格式交叉污染
- **30项不通过 → 禁止构建**：硬门禁
- 日常修改小段落不触发格式校验
- **跨报告复用**：无论海事/类工控/客户报告，只要是**该组织系**报告，都应调用本技能

### 2. 原子化任务拆解
每条独立需求拆为独立 task，逐项执行+验收。禁止批量执行+一次性交差。

### 3. 模型选择
默认 `deepseek-v4-pro`。禁止短上下文使用 glm-5.1。

### 4. 批量修复脚本
先跑 5 行 snippet 验证匹配逻辑 → 确认后写完整脚本 → 禁止 `re.sub()` 全局操作编号/锚点。

## 资源索引

| 文件 | 用途 | 何时读取 |
|:--|:--|:--|
| `business:<域>/<组织>/brand/brand_colors.json` | **品牌色值（组织级单一事实来源）** | 任何涉及色值操作时 |
| `references/brand-guide.md` | 品牌视觉规范 | 构建时 |
| `references/layout-spec.md` | 排版布局规范 | 排版优化时 |
| `references/checks.md` | 30项自动校验详细规则 | 执行校验时 |
| `references/markdown-limits.md` | **Python markdown 渲染限制速查**（表格/锚点/emoji） | 编写/修复 Markdown 时 |
| `references/orchestration.md` | 编排工作流 | 编排时 |
| `references/fact-check.md` | 事实核查+上角标引用规范 | 事实核查时 |
| `references/version-management.md` | 版本号同步 | 版本升级时 |
| `references/batch-fix-template.md` | 修复脚本模板 | 写修复脚本前 |

## 禁止行为

| 反模式 | 正确做法 |
|:--|:--|
| 撰写迭代阶段反复调格式校验 | 内容定稿后才调一次 |
| 修改后不跑 30 项校验 | 门禁每次必跑 |
| 短上下文中使用 glm-5.1 | 默认 deepseek-v4-pro |
| 全局正则替换操作编号 | 行级别标志位法 |
| 校验不通过强行构建 PDF | 不通过禁止构建 |
| 仅在海事报告中使用 | 所有**该组织系**报告强制使用 |
| 用户说了"验一下格式"但不触发 | 触发词已扩展到20+口语化表达 |
| coherence 未通过就调 verify | Phase 0 门禁：coherence 必须 PASS |
| 检查内容逻辑（编号/引用/数据一致性） | 这些是 coherence 的职责，不是本技能 |

## 版本与数据一致性（治理规则G，来自用户 MEMORY.md）

- **分类口径统一**：升级 `classify_product` 后必须用新规则重跑历史趋势数据。
- **版本三统一**：输出文件名 = 报告标题 = `<title>` 标签。
- **关联公司合并双通道**：`CHANNEL_MERGE` 必须同时应用于销售订单与售后维修数据。
- 🆕 **修正版报告标记**：修订后第3版起，版本号旁标注 `（修正v3, 2026-06-XX）`。

> 完整定义见 `<host_config_dir>/MEMORY.md`（运行期由 `host_paths.host_config_dir()` 解析）。


## 盲区与自审（反模式#45）

- 盲区声明：30 项校验是固定清单，未列入的新格式问题漏检；仅查格式不查内容（内容自洽需 @report-content-coherence，二者不可交叉）
- 自审：report-verify 的方法边界若在实战中失效，登记反模式门禁映射表 + 更新本段落