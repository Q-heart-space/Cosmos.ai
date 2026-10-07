# 常见陷阱 + 输出物

## 常见陷阱

- **直接 Edit/Write 后未补 write_guard**：会导致 `write_guard --audit` 报 bypass。必须补登记。
- 🆕 **旁路 secure_write 单一写入入口（反模式#74/#75·2026-08-19）**：新建/修改脚本严禁自建并行备份模块（旧 `_backup_helper` 已并入 `secure_write` 并删除）或 `path.with_suffix('.bak_*')` 就地写源真相目录（constitution/governance/scripts）。写前快照一律调 `secure_write.secure_snapshot()`（唯一 sanctioned API）；关键文件写入一律经 `secure_write(operation="auto", reason="...")`。`asset_health_check` 已通电 `find_source_dir_pollution()`（残留扫描）+ `find_unsecured_write_calls()`（前馈旁路代码扫描）两道门禁回归防护——违反即 P0 上报。
- **register_asset 并发冲突**：多个脚本同时注册可能导致 `reconcile_asset_wiring.py` 失败。失败后单独运行一次 `reconcile_asset_wiring.py` 即可。
- **综合工作规划写入被阻断**：施工标记 `active=false` 时写入宪法文件会被 `pre_write_check` 阻断。更新 `.workbuddy/.under_construction` 为 `active=true` 后再写入。
- **审计报告头部缺失**：新建审计报告必须包含完整头部字段（尤其 **变更** 行），否则 `asset_health_check` 报 HEADER_VERSION_DRIFT / INCOMPLETE_HEADER。
- 🆕 **接线≠通电**（2026-08-09·经验#14）：新建检测器脚本后 wiring_map 自动接线，但 daily_tasks.json 不会自动更新。须手动执行 Step 2.5，否则脚本将建成但永不运行。
- 🛑 **别用 `contains` 判断「功能已存在」（2026-09-07·RC-068 实证·与 RC-058 同族）**：
  补丁脚本写 `if "--self-test" not in code:` 判定「未实现自检」——而**变更日志文本里也含 `--self-test` 字样**
  ⇒ 误判为已存在而**静默跳过注入**。正确判据是**语义锚点**（如 `def self_test(` 是否定义），不是字面子串。
- 🛑 **自检不得只查符号存在（反模式 #309 假通电）**：`self_test()` 必须**真实调用**被测逻辑。
  判例：`bootstrap_install` 自检真实调用 `check_environment()` 验证返回 dict 且含 status/overall——
  因其历史缺陷（v1.2→v1.3）正是 `--check` 崩溃；只查 `hasattr` 永远绿，抓不到。
- 🆕 **exit 语义最容易「搞反」（2026-09-10·ptn_ledger_check 实证）**：Step 2.5 三问给出了判定方法，但**约定方向仍常被写反**——
  正确方向是 **`exit=1` = 仅 P1（软·预期退出·可标 `known_exit_codes`）**、**`exit=2` = 存在 P0（硬·不标 kec·触发 M8 闭环）**。
  实测新脚本写成 `1=P0 / 2=P1`（方向相反）+ daily_tasks `known_exit_codes=[1,2]` → **P0 被静默豁免**（最危险的假绿）。
  自检必须锁死该语义：`if (_exit([],[]), _exit([],["x"]), _exit(["x"],[])) != (0,1,2): fail`。
- 🆕 **自检夹具的「合成编号」会被静态扫描器误判（2026-09-10 实证·反模式 #63 假红同族）**：
  夹具按设计需要「一个必然无定义的编号」（如测试「漏登检出」）→ 静态字面量会被 `cascade_reference_checker` 扫到 →
  报「陈旧引用：该编号被引用但无定义」（实测 1 项假红）。**修法=动态拼接构造**（`_MISSING = "PTN-" + "99"`·连注释里都不能留字面量）。
  同类风险：夹具里的路径/ID/文件名常量——**任何检测器脚本自己的夹具都在自己的扫描范围内**。
- 🆕 **自检夹具必须与断言语义隔离（2026-09-10 实证）**：同一夹具若同时承载两个被测点（如「重号检出」用含重号的台账），
  会被另一断言误用 → `parse` 的 last-wins 使行归属漂移 → 派生「一致项误报」的假红。**一个断言一个夹具**；
  且被测函数若存在「已报 P0 就不应再派生 P1」的抑制逻辑，须配**独立回归用例**（T3b）锁死该行为。
- 🛑 **改名 vs 改类型声明（2026-09-07·RC-066-A）**：N1 命名（`_test`/`_once`）是**硬判**，
  补头部 `生命周期：production` 只会**新增** `TYPE-CONFLICT` + `NAME-DECL-CONFLICT`（3 红 > 2 红）。
  命名与落位冲突时**改名字**，不是改声明。改名后须同步全部引用（先全量扫描定影响面·再批量替换）。
- 🆕 **类型默认不是 production（2026-09-07·Step 1.1）**：`scripts/` 下新建脚本若**无调度源引用、无一次性/测试词元**，三轴判定落到 **tool（不接线）**——「长期回路成员」必须被证成，禁止默认进 wiring_map。想进常驻回路：先接 `daily_tasks.json` 等调度源，再用引用轴证成 production。**禁止拿 wiring_map 自己反证自己**（自证源禁用·循环论证·实测 91.4% 假分布）。
- 🆕 **落位错了命名再对也白搭（2026-09-07·Step 1.1 落位硬约束）**：①**一次性脚本必须带 `_once` 后缀且落 `staging/`**（或 `scripts/_archive/`）——落在 `scripts/` 根不带 `_once`，会被判成 tool 并可能进 wiring_map 常驻，制造无效接线；②**测试脚本必须落 `tests/`**，命名用 `test_*`/`*_test`——落在 `scripts/` 下会触发 `TEST_MISPLACED` P1（`new_script_compliance_check.py` v1.5 门禁 07）。③目录轴 > 命名轴：**目录判定优先于命名**，头部 `# > **生命周期**` 声明只作一致性校验，冲突时以目录+命名推导为准并报 `TYPE_CONFLICT` P1。

## 输出物

- 新脚本文件（`scripts/<script>.py`）
- 回路注册更新（`circuit_wiring_map.json` + `self_test_registry.json`）
- 规划状态更新（`constitution/综合工作规划.md`）
- 可选：终态审计报告（`audits/YYYY-MM/[审计]..._终态_YYYY-MM-DD.md`）
- 记忆同步（`MEMORY.md` + 今日日志）


