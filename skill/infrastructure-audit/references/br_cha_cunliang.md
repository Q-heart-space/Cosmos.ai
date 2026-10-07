# 铁律BR·建前查存量协议（Step 0-9·十步八域）

## 🆕 铁律BR·建前查存量 查存量协议（v1.2·2026-08-13·经验#34+#35）

> 🆕 **跨域同源预检（v1.7·2026-08-23）**：查存量前先跑 `python scripts/infrastructure_truth_query.py --candidate "<候选描述>"`——五域（META/技能/任务/脚本/术语）一次查完·命中≥1 域 = 同源·复用/扩展（铁律BR.1）·防「局部查目标文件内部」漏全空间同源（T-4-016 三版判据迭代实证·2026-08-23）。

触发词"建前查存量"/"查存量"/"BR.1"/"部分匹配"/"提示存量债"/"判断是否需要专门窗口"时，必须执行查存量协议（**实时 grep 真相源·非记忆检索**·铁律1「源头即真相」落地）：

### Step 0：查任务主表（四层核验·非简单 grep 标题）🆕🆕 v1.2.1

> **⚠️ 去重本质 = 避免重复劳动，非避免重复标题。** 本步骤是「四层核验任务是否真正完成」机制的**唯一真相源**（2026-08-13 由 qdr-deep-governance-planning Step 5 + 标准模板自检同步归位·铁律X 共享逻辑提取）。任何「去重」「查存量」「避免重复任务」操作，一律引用本定义，禁止在别处重新展开四层文本（防漂移）。

查存量/登记新任务前，必须四层核验「已登记任务是否真正完成」——杜绝「grep 标题无重复就跳过」导致的假闭环重复劳动（反模式#43 规模数字先实测 / #44 检测器假阳性未修）。

| 层 | 核验 | 本质 | 绑定铁律 |
|:--|:--|:--|:--|
| **L1 标题** | grep `constitution/综合工作规划.md` 任务主表·找相似任务标题 | 表层 | 铁律BR.1 部分匹配 |
| **L2 状态** | 读该任务状态（Done/Now/Later）+ 结论（success/partial/failed）——Done 但 partial/failed = 未完成 | 声明层 | 铁律AN 状态断言前置（"我以为的状态≠真的状态"） |
| **L3 痕迹** | Done 任务声称的产物（脚本存在？验证通过？接线通电？）是否真实存在 | 物证层 | 铁律AN + 反模式#44 假闭环（判例 T-3-099 validate_growth 标 Done 但脚本不存在） |
| **L4 效果** | 跑对应检测器拿实测数，不信 Done 声明 | 真相层 | 铁律AB 数据源权威性 + 反模式#43 规模数字先实测（判例：「16 个回路不一致」实测 269 个） |

**判定（必随结论输出）**：
- **L1-L4 全通过** → 确认「已登记且真正完成」→ 扩展/复用而非新建（铁律BR.1 >50% 匹配默认扩展）
- **任一层「Done 声明」与「实测痕迹」不符** → 该任务「执行不彻底」→ 补「修复任务」而非新建「重复任务」（避免重复劳动）
- **L1 无匹配** → 正常新建·继续 Step 1-3

> **🆕 2026-08-13 治理维度化（v1.2.1）**：四层核验已从「逐技能手写文本」**上升为跨切面治理维度**——代码执行唯一真相源 = `scripts/four_layer_verify.py`（文本定义仍为本 Step 0）。本质是「基础设施查询手段」：任何「查/建」动作自动 invoke，无需逐文件找查重机会（铁律X 共享逻辑提取·防漂移）。
>
> **自动接线（源头控制·有「查」这个动作即触发）**：
> - 任务创建：`task_factory.pre_create_check` 检查3 → `four_layer_verify(domain="task")`
>
> **🆕 记忆继承维度（v1.7·T-3-1367·2026-08-26）**：查存量/查基础设施时增加「业务空间记忆继承完整性」维度——当前空间 MEMORY.md 是否含铁律继承指针（L1 三件套单行引用·BZ.1）：缺 → `python scripts/business_space_memory_check.py --repair` 自动补注入（IPC 铁律U 违规判例：业务空间未读 L1 致误判授权/新建脚本不查存量·根因=规则层分发断层）。任何业务空间任务启动前必检（对齐 qdr-preguard Step 0.7）。
> - 任务批量去重：`task_dedup.filter_duplicates(verify=True)` 命中已登记任务时 → `four_layer_verify`
> - 元模式登记：`register_meta` 去重命中（标题/语义/内容）→ `four_layer_verify(domain="meta")`
> - 元模式同源预检：`meta_homolog_dedup` 同源命中 → `four_layer_verify(domain="meta")`
> - 规划同步：`planning_sync` 去重（复用 task_dedup）
> - 术语登记：`term_registry_sync.apply_sync` 写入前 → `four_layer_verify(domain="term")`（防第二真相源）
> - 反模式登记：`anti_pattern_gate_router --check-dedup <名>` → `four_layer_verify(domain="pattern")`
> - 术语/反模式查询：`infrastructure_truth_query --term/--pattern`（查询维度·互补）
>
> **注册类资产覆盖（跨切面治理维度——所有「会重复登记的有编号/身份资产」·抽象层源头）**：
> - `task`（任务·综合工作规划）｜`meta`（元模式·drq/meta_patterns）｜`term`（术语/概念·核心概念术语表+concept_registry）｜`pattern`（反模式·反模式门禁映射表）
> - `script`（脚本·circuit_wiring_map.scripts 518+self_test_registry）｜`skill`（技能·circuit_wiring_map.skills 50+~/.workbuddy/skills）
> - `automation`（自动化·~/.workbuddy/workbuddy.db·由 automation_update 工具管理·查询走 truth_query·暂不做四层核验）
>
> **维度语义**：`four_layer_verify(query, domain)` 返回 `verdict ∈ {no_match, confirmed_done, fake_done, incomplete}`；`confirmed_done`→跳过、`fake_done`/`incomplete`→补修复而非跳过/重复创建。
> - `term` 完成语义：`stable/active/evolving`+定义体真实+被消费 → confirmed_done；`proposed/?` → incomplete；`stable` 但 definition 空 → fake_done（壳概念）；`deprecated` → confirmed_done 变体（提示用新名）。
> - `pattern` 完成语义：状态列含「闭合」+门禁脚本存在 → confirmed_done；状态「—」→ incomplete；已闭合但脚本缺失 → fake_done。
> - `script` 完成语义：接线+self_test登记+可执行 → confirmed_done；存在但未接线 → incomplete（孤儿脚本）；接线但脚本缺失 → fake_done（僵尸条目）。
> - `skill` 完成语义：活跃+SKILL.md充实 → confirmed_done；登记但 SKILL.md 缺失 → fake_done（假技能）；SKILL.md 空壳 → incomplete；废弃 → confirmed_done 变体。
> - 所有消费方仅调用此能力，禁止各自重写四层逻辑（铁律X·防漂移）。

### Step 1：查清单矩阵

→ 确认 10×4 矩阵未标注 ✅ 已有工具覆盖

### Step 2：查 wiring_map

→ 确认无已注册脚本可扩展而非新建

### Step 3：查反模式映射表

→ 确认反模式已被已有检查覆盖·不重复实现

### Step 4：查同类校验逻辑（🆕 v1.4·2026-08-15·按交付物九类目录全空间查）

→ **「给门禁补检查」=「新增检查」**·必须全空间查「是否有同类已在做」——而非只查目标文件内部。
→ **可执行命令**：`python scripts/infrastructure_truth_query.py --similar "<功能关键词>"`（🆕 v1.4 按交付物九类目录全空间查——constitution/governance/audits/research/products/scripts/workspace/drq·覆盖文本+.py 脚本·补「只查脚本」的类型维盲区）。
→ 判例：补「ID 唯一性门禁」时只查 steward_gate 内部（无）就下「系统缺 ID 唯一性」结论——`--similar "编号唯一"` 会立刻返回 planning_table_validator.py（早有「编号唯一」校验）·重复实现被撤销（铁律X）。
→ **根因**：局部查（目标文件内部）≠ 全空间查存量（grep 同类校验逻辑）。「缺 X」断言必须先全空间查 X 的已有实现，否则就是「局部空缺→误判整体空缺」的认知陷阱。
→ **🆕 自动接线（2026-08-16·T-3-831/1159 误判根因修复）**：`task_factory.pre_create_check` 检查7「缺位断言查同类」——任务标题含「缺X/无门禁/盲区/分裂/未统一/未覆盖/未接线」等缺位断言时，自动调 `--similar` 查 X 同类实现·软警告「可能误判」·AI 复核而非硬阻断（判例：T-3-831「Move无门禁」未查 circuit_power_check 已有引用完整性检测→误判整体无门禁；T-3-1159「字段分裂」未查两字段方向相反语义→误判分裂）。

### Step 5：查元模式（🆕 v1.3·六域补齐）

→ `grep "模式关键词" drq/meta_patterns/*.json` 确认无已登记 META 可复用（meta 域）

### Step 6：查术语/概念（🆕 v1.3·六域补齐）

→ `python scripts/infrastructure_truth_query.py --term "<概念名>"` 确认无已定义术语（term 域·防第二真相源）

### Step 7：查技能（🆕 v1.3·六域补齐）

→ `ls ~/.workbuddy/skills/` + `grep 触发词` 确认无已建技能可复用（skill 域）

### Step 8：查管道体系（触发线）🆕 v1.4·2026-08-15·对抗式审计收敛·八步补齐

→ 查 `governance/管道体系架构.md` §一（14 管道 + 6 类触发机制）+ §〇（收录四标准）——确认新脚本属于哪条管道、走哪类触发线（实时·write_guard / 定时·22:00 / 事件·Done / 事件·注册+日治 / 实时·任意写入 / 多通道），**不是默认接日治**（门禁→写入钩子线·检测器→定时线·感知器→感知线）。

### Step 9：查文本同类（级联维）🆕 v1.5·2026-08-15·补「查同类只查脚本」文本维盲区

→ `python scripts/concept_cascade_engine.py --on-change <拟建文件>` 或 `--consumers <概念名>`——查「这个概念/文件关联了哪些**文本+脚本**」（semantic_references 的 defines/uses 覆盖 .md+.py·非仅脚本）。与 Step 4「查同类」（--similar 只查 scripts/*.py）互补：**Step 4 = 脚本维·Step 9 = 文本维**。防「改一个 .md 治理文档漏关联下游」+「重复造文本治理文档」。

### 判例
2026-08-10：pre_write_check 新增 NEW_SCRIPT_REGISTRATION 时未执行以上查询——register_asset.py v1.2 已在清单标注 ✅·consumer_check 已覆盖——重复实现·浪费 2 轮修复窗口。


