# 12 步 SOP（对抗式审查核心流程）

## 12 步 SOP（🆕 v3.3：+宪法锚定层+Agent宪法判决）

```
宪法架构前置判决   → Step -1 🔗 语义级朕  → Step 0 🔬 自审
  → Step 1 🔍 基线 → Step 1.5 🔬 原子扫描
  → Step 2 🧠 Agent（4人·每人含宪法前提声明）
  → Step 3 🔎 11维审计 → Step 4 📋 分级（T0-T5路由）
  → Step 5 🔧 修复 → Step 5.5 ⚡ 单维快验 → Step 6 ✅ 全量复验
  → Step 7 🔄 元循环 → Step 8 ♻️ 自审 → 停止或回到Step 3
```

### Step -1：语义级朕完整性检查 🔗（🆕 v3.2）

**必检**（任何脚本注册或概念新增后强制执行）：

```bash
# ① 概念依赖完整性
python scripts/term_registry_sync.py --check-missing-deps

# ② 脚本→概念锚定
# 提取脚本 docstring → 解析核心概念 → 比对术语表

# ③ 治理决策依赖验证
# 提取决策文件"依赖"行 → 验证引用的概念全部存在
```

**P0**：依赖的宪法概念未定义。→ 停审计·先补宪法·不得绕过。

---

### Step 0：技能自审 🔬

必检：SKILL.md 版本 ≥ v3.24·含宪法架构前置判决第四题(记忆完整性)·盲区 1-8 + 14-20（9-13 历史未落地·见 references 完整性声明）·校准器接入·反模式 83/83（实测以映射表为准）（🆕 v3.20 单源化：以反模式门禁映射表实测 83 条为准·原 40/40/67/67/77 均过时·2026-08-23 XSG-D0-03 实测校准 76→77→2026-08-25 RC元教训转化落地 77→83）·**映射表版本 ≥ 技能版本**（反模式门禁映射表 v1.x 必须覆盖本 SKILL 声明的全部反模式·用 `anti_pattern_gate_router.py --audit` 验证）

---

### Step 1：基线采集 + Step 1.5：原子必检

**Step 1.5 原子必检清单**（🆕 v3.5·T0.5 六轮教训·每条必须有可执行命令）：

| # | 检查项 | 可执行命令 | 盲区来源 |
|:--|:--|:--|:--|
| ① | 代码空壳 | `shell_script_detector.py --json` | v3.0 |
| ② | 回路一致性 | `reconcile_asset_wiring.py --audit-circuits` | v3.0 |
| ③ | 占位头 | `grep -rl '待补充' scripts/*.py \| wc -l` | v3.0 |
| ④ | 模板空壳 | `template_scoring.py --scan --json` | v3.0 |
| ⑤ | 消费者覆盖 | `consumer_check.py --json` | v3.0 |
| ⑥ | 记忆写入验证 | 检查流程日记/成长记录/L3日志/L2 MEMORY.md 四层 | v3.4 |
| ⑦ | **字段存在性检查** 🆕 | `python -c "import os; print(sum(1 for f in os.listdir('scripts') if f.endswith('.py') and '用途' not in open('scripts/'+f).read()[:700]))"` ——不仅查已有字段质量·必须查字段是否存在 | 2026-08-10·46 个真实脚本零用途字段被 4 轮审计漏检·conformity≠completeness |
| ⑧ | **文件完整性验证** 🆕 | 对比关键文件行数与基线——`wc -l scripts/closure_verification.py`≥1000·`wc -l scripts/write_guard.py`≥200——批量修复工具可能摧毁被修复对象 | 2026-08-10·batch 脚本将 closure 1720→7行·不自毁铁律复发 |
| ⑨ | **参数链路闭环检查** 🆕 | 新增 CLI 参数后验证三步链路——`grep "parser.add_argument.*--新参数" scripts/*.py`→`grep "新参数=" 调用点`→`grep "args.新参数" main()`——防止"校验函数正确但参数从未传递" | 2026-08-10·write_guard --receipt 声明但函数签名缺参数·main() 不传递·secure_write 不传递——完整接收链从未走通 |
| ⑩ | **建成未通电检测** 🆕 | 新脚本编译后立即验证——`grep "新脚本名" scripts/circuit_wiring_map.json`≥1 + `grep "新脚本名" governance/data/daily_tasks.json`≥1（或确认在自动化中）。建成+注册+调度三件套缺一不可。 | 2026-08-10·Phase 2 三脚本建成但 wiring_map 0 注册 + daily_tasks 0 调度——经验 #18 第五次复发（backup·portable·pattern_to_task_bridge·reconciler·reusable 五连） |
| ⑪ | **消费者真实性验证** 🆕 | wiring_map expected_consumers 中的条目必须是可执行代码文件（scripts/*.py），不得包含纯文档文件（constitution/*.md·governance/*.md）。consumer_check 设计为验证代码级调用链，文档不是消费者。 | 2026-08-10·reusable_object_declaration 注册了 constitution/复用对象定义.md 为 consumer→假绿 P0 误报 |
| ⑫ | **建前查存量验证** 🆕 | 新增功能/脚本/检查前验证三步——`grep 功能关键词 核心设计原则落地检查清单.md`→`grep 功能关键词 circuit_wiring_map.json`→`grep 反模式 反模式门禁映射表.md`——防止重复实现已有工具。违反者适用经验 #34 判例。 | 2026-08-10·pre_write 新增检查时未查询清单·register_asset+consumer_check 已覆盖·重复实现→浪费 2 轮修复 |
| ⑬ | **矩阵真实性验证** 🆕 | 对清单矩阵每个 ✅ 检查三项——`wiring_map 注册？`+`daily_tasks 调度？`+`至少一次运行输出？`——未通过三项的自动降级为 ⚠️ 并告警。实际通过 `circuit_power_check` + `consumer_check` + `execution_recorder` 联合验证。 | 2026-08-10·经验#32·⑩A 列为 ✅ 但 3/5 wiring_map 未注册+4/5 零调度——清单矩阵假绿·自动化调度缺失导致清单网关失准 |
| ⑭ | **文件完整性自保检测** 🆕 | `wc -l scripts/closure_verification.py scripts/write_guard.py scripts/pre_write_check.py`——对比关键脚本行数与基线（closure≥2000·write_guard≥700·pre_write_check≥4000）。每次修复后强制复检行数变化·防止调试注入/批量修复意外清空文件。 | 2026-08-11·closure_verification.py 调试注入→0字节·从tar.gz恢复·耗时25min定位+恢复——不自毁铁律复发（经验#9同源）|
| ⑮ | **审计发现可追溯性检查** 🆕 | 任何"文件缺失"/"功能缺失"断言必须先 `grep` wiring_map + `grep` self_test_registry 确认该资产曾被注册——防止语义推断制造假阳性（如 T-3-741 命名漂移）。 | 2026-08-11·daily_perception_sensor + blind_spot_detector 从未注册过——"缺失"是审计脚本语义推断产物·浪费13轮排查 |
| ⑯ | **Agent 执行健康检查+校准器查询** 🆕 v3.10 | 多 Agent 并行前两步——步骤①: 查询 `.workbuddy/calibrator_suggestions_cache.json` 获取数据驱动超时建议·无历史时 cold_start 兜底（1.5×估算·≥90s）·详见 Step 2 前置校准器预查询；步骤②: 单 Agent 超时取 max(校准器建议, 90s)·总时长上限 = max(各Agent超时)+60s。校准器查询失败自动降级到 90s·不阻塞审计主流程。 | 2026-08-11·2/3 Agent 超时后实际已完成·被误判失败·2026-08-12 接入 timeout_calibrator v2.1 cold_start |
| ⑰ | **关键文件备份就绪检查** 🆕 | 修改 scripts/ 下任何一个核心脚本（closure_verification/write_guard/pre_write_check/circuit_wiring_map）前——必须先确认 `Backups/full_2026-08-11_*.tar.gz` 存在·不含需改文件则先执行全量备份。 | 2026-08-11·closure_verification 0字节恢复耗时25min——备份缺失导致恢复路径断裂 |
| ⑱ | **职责语义归位验证** 🆕 v3.11 | 新增/合并脚本功能前判定职责语义正交性——事件检测(milestone_detector)/事实检测(growth_drift_check)/行为检测(drift_enforcer)是正交维度·正交职责独立文件·禁止硬塞进单一文件（铁律X）。方法：`grep 用途 scripts/` 对比职责语义是否同构·同构才可合并·正交必须独立。 | 2026-08-13·GROWTH_SOURCE_MAP 修复第一轮把事实漂移硬塞进事件检测器 milestone_detector(650→950行)·被迫回退·反模式#41 |
| ⑲ | **定位保持验证** 🆕 v3.11 | 修改文件前记录核心定位元素（映射表=映射列·编年史=时间线·清单=检查项·反模式表=反模式→门禁映射）·修改后验证保留——丢失核心定位=文件变质（反模式#42）。方法：改前 `grep 核心列名/结构 <file>`·改后对比是否仍存在。 | 2026-08-13·GROWTH_SOURCE_MAP v2.0 丢「源头→章节」映射列·从映射表变质为脚本分工图·v2.1 恢复·反模式#42 |
| ⑳ | **规模数字先实测 + 修数据必查检测器** 🆕 v3.12 | ①「规模/计数」断言（如"16个不一致""40处漂移"）必须先跑检测器拿实测数——不信记录/摘要里的二手数字（反模式#43 同源·真相源层级）；②修数据不一致时必须同时审查检测器判定逻辑是否有假阳性（如 split("|") 不处理 ·→+ 分隔符）——只修数据不修检测器=检测器永远误报（反模式#44·闭环双面性）。 | 2026-08-13·回路治理「16个」实为269·classify()兜底⑦自审制造254假接线·audit split("|") 假阳性·反模式#43/#44 |
| ㉑ | **检测器自反身性验证（盲区声明+盲区发现+盲区固化）** 🆕 v3.13 | 检测器/技能必须具三层自反身性：①**盲区声明**——检测器声明「已知盲区清单」（如「我的正则漏检缺结尾|的残缺行」）②**盲区发现**——selftest 覆盖「残缺输入」（缺结尾|/空表/单列/超长单元格）+「边界输入」③**盲区固化**——发现盲区→登记反模式+META+更新 selftest 回归用例+bump 版本。验证：`grep "盲区\|selftest" <检测器>` 判断是否有盲区声明·无声明=反模式#45。 | 2026-08-13·md_table_validator v1.1 漏检缺尾管道符残缺行·报告0问题实际5行不一致·v1.2修复（反模式#44/#45） |
| ㉓ | **三轨定位对齐验证** 🆕 v3.14 | 任何治理计划必须对齐三轨定位（why产品化/what自进化/how治理深度）——局部治理脱离三轨=治理者脱离存在意义（宪法前置法A3+本质定位§1.2三轨定位）。方法：检查计划的每阶段是否产出「可交付交付物（产品化）·接入进化管道（自进化）·量化G/V/κ提升（治理深度）」。判例：交付物治理原5属性遗漏三轨→修正为8属性。 | 2026-08-13·交付物治理计划三视角审视·5属性→8属性 |
| ㉒ | **路径分隔符一致性检查（正斜杠硬编码 vs Windows 反斜杠）** 🆕 v3.14 | 所有含 `startswith('scripts/')`/`'scripts/' in`/`split('/')` 路径检查的脚本，必须确认上游路径用 `.as_posix()` 或 `.replace('\\','/')` 正常化。验证：`grep -rn "startswith('scripts/\|'scripts/' in\|split('/')" scripts/*.py` → 逐个追查 rel_path 来源是否正常化。裸 `str(Path)` 反斜杠 + 正斜杠检查 = 门禁在 Windows 从未生效（反模式#46）。 | 2026-08-13·FIX_BEFORE_INFRA_CHECK 路径 bug 门禁从未生效·v1.23 修复（反模式#46） |
| ㉔ | **四层核验交叉引用（任务完成真实性）** 🆕 v3.15 | 审计结论若断言某修复/任务「已完成/已修复」，须满足四层核验 L3(痕迹存在)+L4(实测数字)——本技能 ⑳(规模数字先实测)+㉑(自反身性) 即 L3/L4 工程落地；L2(状态 Done 但 partial) 由 infrastructure-audit 四层核验覆盖。四层核验唯一真相源见 `infrastructure-audit` 技能「Step 0 查任务主表（四层核验）」。 | 2026-08-13·四层核验同步·task-retrospective/对抗审计对齐 |
| ㉕ | **状态取值覆盖审计（判定逻辑盲区·元审计）** 🆕 v3.16 | 任何含「状态机判定」的代码（`if status in (完成态列表)` / `lifecycle in (...)` / `status not in (...)`）必须用真实数据的状态取值分布**反攻判定列表**——统计真实数据源的状态取值分布 → 对比代码判定的完成态列表 → 找出漏判取值。可执行：`python -c "import json,glob; from collections import Counter; print(Counter(str(json.load(open(f)).get('_meta',{}).get('lifecycle_state','')) for f in glob.glob('drq/meta_patterns/META-*.json')))"` → 对比代码完成态元组。判例：four_layer_verify meta 域 L2 只覆盖 active/REGISTERED/registered·漏 CLOSED(152)/LANDED(5)——157 个「已闭合/已落地」META 误判「未登记」(P0)。通用性：任务状态 Done/Deprecated/Blocked·META 生命周期 REGISTERED/LANDED/CLOSED·概念 status stable/proposed/deprecated 均可能漏判。 | 2026-08-13·four_layer_verify 六域对抗审计·meta L2 漏判 CLOSED/LANDED·task L2 Deprecated 语义 |
| ㉖ | **数据源存在性校验（读错文件/字段路径·反模式#47）** 🆕 v3.17 | 审计任何「读数据源」的检测器/脚本时，验证它读的「文件存在 + 字段存在」——①文件级：`grep` 脚本里 `open(...)`/`Path(...)` 的路径常量 → `ls` 确认存在 ②字段级：脚本里 `data.get("字段")`/`data["字段"]`/`stats.get("字段")` → 用真实数据 `python -c "import json; d=json.load(open(...)); print('字段' in d)"` 验证字段路径正确。判例：capability_growth_check rate_closure 读 trust_log.jsonl（事件实际在 guard_history.jsonl）+ rate_cross_space 读 stats.total_entries（字段实际在顶层 data.total_entries）——两处数据源错位致 B 渠道假沉默 B=0.6→修复后 1.0。复用 infrastructure_truth_query exists 断言。 | 2026-08-13·capability_growth_check B 渠道数据源错位·B 0.6→1.0·L5_ready true·反模式#47 |
| ㉗ | **落地三验（真跑+零污染+全步骤输出·反模式#48）** 🆕 v3.18 | 审计「落地/通电」结论时，最低标准不是「编译通过」（compile）也不是「接线通电」（wiring_map+daily_tasks 静态接线），是「用合法数据真跑一遍、零污染、全步骤输出」：①**真跑**——`python script.py --合法参数` exit=0 + 关键输出非空（compile 只是前置非验收）②**零污染**——跑前记录关键数据源 hash/行数（`md5sum`/`wc -l`）→ 跑后 diff 一致；会写数据的脚本必须 `--dry-run` 先预览或沙箱/临时目录隔离 ③**全步骤输出**——脚本每个关键步骤（登记/注册/同步/校验）都有可验证输出痕迹·无静默跳过。判例：anti_pattern_gate_router --register 编译+前置校验通过·但从未用合法数据真跑·7 bug 潜伏——版本 bump 破坏版本行（变更行插版本行内致「\|类型\|日期」追加到变更行尾）·追溯表定位正则 `^\|\s*#\d+\s*\|` 匹配 0 行（追溯行同格结构）静默缺失·META 占位符 magic number 撞车·落地清单硬编码版本。与⑩「建成未通电」同源进阶：⑩验「接线」·㉗验「真跑」。可执行载体：`scripts/landing_verify.py`（--run 真跑·--record-state/--verify-state 零污染）。🆕 T-3-1213 零污染显式化：递归闭环修复引擎侧 `recursive_closure_repair v1.2` trace.summary 新增 `zero_pollution_verified` 标记（非 dry-run 且有修复=待核验）·`closure_completeness_check.py`（closure_verification v1.47 CHECKS P1）验证「最近修复是否完成零污染核验」——零污染维度从审计建议升级为可执行检查。 | 2026-08-14·T-3-1138 --register 对抗审计·编译通过≠真跑·反模式#48 · 🆕 2026-08-17·T-3-1213/1214 |
| ㉘ | **审计断言交叉验证（审计者反身性·元审计）** 🆕 v3.19 | 审计下「X 缺失/应做 Y」断言前强制三问——①**语义完整读**：是否读了 X 的完整职责语义·而非见名字/标注就归因（#43 的 AI 审计推理变体·判例：见"递归闭环"名字猜"应闭环到固化"·recursive_closure_repair 职责=修复循环本不含固化）；②**多源交叉**：断言「X 状态=⚠️/缺失」前是否交叉验证「标注/声明」vs「真相源（代码注册表/实际文件）」·而非采信单一标注（#47 的 AI 审计推理变体·判例：采信本质定位 L549"检测源待接入"⚠️ 不交叉 L551"9/9全接入"✅·真相源 collect_defects SOURCE_PARSERS=5 个与"9/9"漂移）；③**职责边界**：区分「X 本就不该做 Y（职责边界·误归因）」vs「X 该做 Y 但没做（功能缺失）」 | 2026-08-14·两轮对抗审计自我复发 #43/#47 的 AI 推理变体·审计者缺反身性审计原子 |

| ㉙ | **RC 元教训反模式专项检测（#79-#83）** 🆕 | 对新建反模式逐条验证「检测器存在 + 已通电」双证：①#79 退出码语义——`grep -n "SEMANTIC_WRITERS\|MECHANICAL_WRITERS\|known_note" scripts/daily_tasks_validator.py` + `grep -rn "退出码语义三问" ~/.workbuddy/skills/qdr-new-script-pipeline/`；②#80 变更传播——`python scripts/move_script.py --old <脚本> --new <tmp> --dry-run`（引用扫描可运行）+ `grep -n "rename-cascade" scripts/auto_sync_framework.py`；③#81 CRLF 漂移——`python scripts/crlf_drift_check.py --scan constitution/`（exit=1=发现漂移信号）；④#82 跨宿主同步——`python ~/.workbuddy/skills/skill-sync/references/skill_sync.py --help`（路径随宿主·AGENTS.md 脚本引用规范 T2·2026-08-28）存在且可运行；⑤#83 技能位置——`python scripts/skill_placement_check.py --path <技能目录>`（v1.1 消费 cross_host_skills.json 注册表·RC-014 qdr-bridge@DSH QDR 合法落点 exit=0·伪造路径 exit=1·误报已根治）。任一反模式缺检测器或零通电→降级 ⚠️ 并触发补建。 | 2026-08-25·RC-005~RC-014 转化落地·反模式#79-#83·检测器见 scripts/move_script.py·crlf_drift_check.py·skill_placement_check.py |
| ㉛ | **跨空间记忆分发审计** 🆕 v3.22·T-3-1367 | 业务空间记忆继承完整性——核对**各业务空间之记忆继承完整性**（🅑 逐空间查：记忆文件是否在·🅑 是否为空·🅑 归属是否正确）：所有业务空间（多根·数据目录+用户工作区）MEMORY.md 铁律继承指针（L1 三件套单行引用）完整性·缺→ `--repair` 自动修复（feeder 规则层分发）+ 验证新空间自动发现（`business_space_feeder.py --list` 含 workspace 形态）·防「规则层分发断层」复发（IPC 2026-08-26 判例：业务空间未读 L1 致误判授权/新建脚本不查存量·根因=T3.3 拆分后继承指针未级联+无分发机制） | 2026-08-26·T-3-1367 跨空间记忆继承机制·feeder v2.0+检测器 |
| ㉚ | **宿主运行时约束检查** 🆕 v3.24·判例 4（2026-09-11） | hook/定时任务等宿主执行体——**三层严格递减不变式**：`启动开销 + 有界 stdin 等待 + 单次子进程超时 < 自看门狗预算 < 宿主配额`（WorkBuddy PreToolUse/UserPromptSubmit/SessionStart 均 30s），且**每个阻塞点都必须有界**（stdin 读取、子进程、网络）。验证：`python scripts/hook_runtime_guard.py --self-test`（四契约真跑）＋ `--budget-plan`（不变式自检）；回退法：grep `timeout=` × 重试次数 与配额比对。**四种违规形态**：①**重试乘积超配额**（判例 3·2026-08-25 hook v2.6 重试 30s×2=60s>30s→平台 kill→重试永不执行·v2.7 去重试根治）②**单次超时==配额**（判例 4·pre_write_hook v2.10 `timeout=30` 恰等配额 30s·再叠加解释器冷启实测 3s→宿主必先 kill→**deny JSON 丢失→fail-closed 语义静默失效**）③**无界 stdin 阻塞**（判例 4·`sys.stdin.read()` 在宿主未关闭管道时无限阻塞至 EOF·复现 `timeout 40` 强杀 EXIT=124 且**零日志**→宿主静默等满 30s 才报超时）④**看门狗缺失**（超预算前无法先输出决策）。**诊断特征（高价值）**：**脚本业务逻辑实测远小于超时值、却报超时** ＝ 有界性缺失·**不是性能问题·勿去优化性能**。修复范式：共用守卫模块（`hook_runtime_guard`：有界 stdin + `threading.Timer` 看门狗 + `safe_exit` 硬退出），超预算时**先输出拒绝决策再 `os._exit`**，保证决策在宿主 kill 前落盘。 | 2026-08-25 判例 3·pre_write_hook v2.6→v2.7·对抗审计 P0-1 ｜ 2026-09-11 判例 4·T-3-1475 四 hook 超时递归闭环·hook_runtime_guard v1.0｜8-25 → 9-11 |
| ㉜ | **计划门禁链验证（三闸痕迹·R-M1/E-12）** 🆕 v3.23·2026-08-30 | 审计「治理行动分解计划」类对象时，验证计划是否走完整三闸门禁链（防"计划声称合规但门禁未跑"）：①**制定前**——`pre_plan_check.py --plan <计划>` 有 C0-C5 门禁痕迹（GATE 通过/AGENTS 接线引用）②**产出后结构**——`constitutional_architect_gate.py --verify <计划>` exit 0（十层/7要素/任务合同）③**产出后声明真实性**——`plan_claim_validator.py --check <计划>` R1-R6 通过（数字/版本/引用/盲区/验收/路由留痕）。三闸任一未跑/未过 → 计划 claim「已合规」降级 UNKNOWN/INVALID（对齐 claim-evidence-validation 三态判定·反模式#66 connected≠usable 的计划版）。判例：RSI 计划 plan_claim_validator 抓到 R6 意图留痕缺失（P2）·补 ∎.9 执行留痕行后 PASS（2026-08-30） | 2026-08-30·R-M1/E-12 三闸流水线深挖·RSI 计划 R6 修复实证 |
| ㉝ | **技能自进化健康检查** 🆕 v3.22·2026-09-08·术语表 #345 | 审计对象**涉及技能**（改技能/审技能/技能驱动修复）时必检：跑 `python scripts/skill_self_evolution_check.py --skill <名>` 取 4 判据（盲区真实/迭代留痕/结构分层/机制词）——①治理/审计类技能 STAGNANT（0-1/4·无盲区无迭代）→ P1（自进化未建立·治理者不自进化=自身治理域累积技术债务·反模式#48 变体）②修复/改造技能后重跑验证（STATIC→EVOLVING=真进化·无提升=修订空壳）③审计结论若断言某技能「已修复」须附检测器实测（对齐 ㉔ 四层核验·防「改了但自进化痕迹缺失」假闭环·判例 qdr-preguard v1.5→v1.6 版本留痕修复 2026-09-08）。与 ㉑（检测器自反身性·查盲区声明）互补：㉑ 查「有没有盲区声明」·㉝ 查「盲区→修订→升级→验证循环是否建立」。 | 2026-09-08·用户'skill-review/adversarial-audit 有没有增加技能自进化审查'·T-3-1468 信号化联动 |
> **执行规则**：Step 1.5 必须全部必检项出实测数字后才进入 Step 2。任何一项无实测数字→停·先补基线。

---

### 🔧 Step 2 前置：校准器预查询 🆕 v3.10

> **原则**：超时不盲设——从数据学习理想超时值。校准器查询是轻量 best-effort·失败降级到静态下限·不阻塞审计主流程。对标 dam_n1_watch_runner v1.17 `_get_calibrated_timeout()` 模式。

**执行指令**（AI 启动 Step 2 Agent 前必须执行）：

```
步骤① 读取校准器缓存（最快·<1ms·纯 JSON 文件读取）
  → 路径: .workbuddy/calibrator_suggestions_cache.json
  → 查找与 Agent 认知负荷相似的脚本条目（closure_verification·self_heal·repair_dimension_sensor）
  → 取这些条目中 credibility 最高的 suggested_timeout

步骤② 如果缓存不存在或为空·运行校准器生成建议（~10-30s·best-effort）
  python scripts/timeout_calibrator.py --suggest --json
```

**超时决策逻辑**：

```
读取 calibrator_suggestions_cache.json →
  ├─ 缓存存在 + 有 trusted 条目（credibility ≥ 0.8）
  │   → 取 max(最大 suggested_timeout, 90s)   ← G3 自动信任
  ├─ 缓存存在 + 有 learning/exploring 条目（credibility < 0.8 或 cold_start）
  │   → 取 max(最大 suggested_timeout, 90s)   ← G2 可用但标注低可信度
  ├─ 缓存不存在 + calibrator 可运行
  │   → 运行 --suggest --json → 取 cold_start 建议（≥90s·1.5×估算）
  │   → cold_start 原理: 校准器用超时事件/实际耗时×1.5 估算·对标 Google SRE：任何数据优于无数据
  └─ 缓存不存在 + calibrator 不可运行
      → 降级到 90s 静态下限   ← 永不阻塞主流程
```

**门禁规则**：

| 校准器状态 | Agent 超时设定 | G级 | 说明 |
|:--|:--|:--|:--|
| credibility ≥ 0.8（trusted） | `max(建议值, 90s)` | G3 自动 | 数据可靠·可直接信任 |
| credibility < 0.8 或 cold_start | `max(建议值, 90s)` | G2 标注 | 可用但标注「待校准器成熟后复检」 |
| 查询失败/无建议 | `90s` | 静态安全网 | 不阻塞主流程·降级模式 |

> **不阻塞保证**：校准器查询总耗时 ≤ 35s（读缓存 <1ms·运行建议 ≤30s·超时截断 5s）。任何失败路径自动降级到 90s 静态下限——校准查询永远不阻止 Agent 启动。

---

### Step 2：独立对抗 Agent 🧠（🆕 v3.3——每人含宪法前提声明+决策OS路由）

> **宪法架构强制要求**：每个 Agent 启动时必须声明——①本次审计涉及的宪法概念名称 ②本次发现属于决策OS哪个层级 ③本次结论锚定哪个第一原理。

**Agent 0：语义级朕完整性审计**（v3.2·保持不变）

**Agent A：Constitution写入完整性审计**（v3.0·保持不变 + 宪法锚定）

**Agent B：命令链完整性审计**（v3.0·保持不变 + 宪法锚定）

**Agent C：基础设施覆盖与接线完整性审计**（v3.0·保持不变 + 宪法锚定）

Agent 必须独立工作·fresh eyes·基于文件系统当前状态·禁止查看其他 Agent 日志。

---

### Step 3：11 维审计 🔎

（v3.1 扩展版本·⑧维 + ⑨宪法模板完整性 + ⑩第一原理推导完整性 + ⑪名称语义准确性）

---

### Step 4：漏洞分级 📋（🆕 v3.3——强制决策OS路由）

```
T0 宪法级·人类确认    → 停止审计·等人确认 · 不得自动修复
T1 战略级·批量确认    → AI提出方案·等确认
T2 架构级·AI自主+审计 → AI修复·事后审计验证
T3 方法级·AI自主      → AI修复·记录
T4 操作级·自动化      → 脚本自动修复
```

每项发现必须标注所属决策层·未标的视为"审计不完整"。

---

### Step 5：递归修复 🔧 → Step 5.5：单维快验 ⚡ → Step 6：E2E 复验 ✅ → Step 7：元循环注册 🔄

> 🛑 **修复前置流程（🆕 2026-08-17·T-3-1216/1220 联动·审计技能自审优化）**：Step 5 涉及**新建/修改 Q博士 脚本**时，必须先走 qdr-new-script-pipeline 标准流程（查存量→回路注册→落地三验→write_guard 登记→全链路审计）·IDE 写入由 pre_write_check.check_asset_registration_wiring（新建脚本 P1 注册提醒）+ codebuddy_prewrite_hook 前置拦截承载（T-3-1216 已修复挂载）·绕过=反模式#19（建成未接线）·本技能 ㉗ 落地三验与 qdr-new-script-pipeline Step 2.6 同源

#### 🆕 v3.9 Step 5.5：单维快验门禁（强制·不可跳过）

> **来源**：2026-08-11对抗审计·30次 closure --strict 全量×6min=180min。
> closure --check <name> 模式已内置（v1.36 argparse），仅运行指定检查项（~30s）。
> 如果修复后先 --check 单维再 --strict 全量，实际仅需 ~50min。
> **性能节约：-130min（72%）**

```
修复 → closure --check <target> → 通过?
  ├─ ✅ → closure --strict（全量最终验证）
  └─ ❌ → 回 Step 5 继续修复 → 再 --check → 通过 → --strict
```

**门禁规则**：
| 修复的文件 | 先运行 | 通过后再运行 |
|:--|:--|:--|
| wiring_map 相关 | `closure --check consumer_coverage` | `closure --strict` |
| 宪法文件版本 | `closure --check dep_version_sync` | `closure --strict` |
| 表格修复 | `closure --check table_integrity` | `closure --strict` |
| META 索引 | `closure --check meta_pattern_integrity` | `closure --strict` |
| FILE_MANIFEST | `closure --check manifest_completeness` | `closure --strict` |
| 多文件修改 | 先逐个 --check 各维度 → 全部通过后 --strict |

**🛑 反模式**：修复后直接跑 `closure --strict` 跳过单维验证（本会话初次审计时发生·浪费 130min）。

---

### Step 8：递归自审 ♻️（15 盲区·🆕 v3.4：+2 记忆相关）

核心盲区（前 8 个已纳入 ·14-20 见下表与反模式 ·详见 references/recursive_self_audit.md）：

| # | 🆕 v3.4 新增 | 检查方式 | 来源 |
|:--|:--|:--|:--|
| 14 | **宪法工作不写记忆** | 宪法级变更后 · 验证流程日记/成长记录/L3日志/L2 MEMORY.md 全部写入 | 2026-08-10：v10.0+M-501+v3.3——L3日志未创建·流程日记未同步 |
| 15 | **milestone_detector 跨文件缺失** | 成长记录中新增 M-xxx · 是否自动同步到流程日记 | 2026-08-10：M-501在成长记录·流程日记无——detector无跨文件检测逻辑 |
| 16 | **Windows stdout 编码静默失败** 🆕 | 审计所有使用 `sys.stdout.reconfigure()` 的脚本·检查是否在管道环境下输出丢失 | 2026-08-11·closure_verification --strict 三次调试无输出·根因为 reconfigure 破坏缓冲 |
| 17 | **调试注入工具不自保** 🆕 | 任何修改脚本的工具必须先备份原文件到 `/tmp` 或 `.workbuddy/` 并验证行数 | 2026-08-11·closure_verification 调试→0字节·恢复耗时25min
| 20 | **检测器自反身性（盲区声明/发现/固化）** 🆕 v3.13 | 检测器/技能必须具三层自反身性：①盲区声明（header `#>**盲区**：` 或 SKILL.md「盲区与自审」段）②盲区发现（写声明时读代码暴露真实 bug·selftest 覆盖残缺输入）③盲区固化（发现→登记反模式+META+修复+更新 selftest 回归用例）。验证：`grep -c 盲区 scripts/*.py` 应≥108·技能应≥32 | 2026-08-13·md_table_validator 漏检→v1.2修复→132文件盲区声明→暴露29检测器bug→P0修复11静默失效（反模式#45·META-1475） |


