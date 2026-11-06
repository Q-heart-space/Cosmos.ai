# DSH 专家**预设**载体（适配面·一份模板 · 零本体复制）

> **落位**：`host-adapters` 分支 ｜ **适用宿主**：DSH（`kind: governor-host`·`transport: plugin`）
> **本目录只有一件载体**：`_template/agent_preset_row.yml`（**平台组合模板·新方言**）。

## 一、它解决什么

Q博士 专家在**各平台**都要有「**可召唤的原生对象**」。WorkBuddy 侧＝原生专家包（`.codebuddy-plugin` ＋ agents ＋ avatars·已装）；**DSH 侧的原生对象＝ agent preset**。
🛑 在补本条之前，DSH 侧**只有注册表第二源**（`experts/expert_lib.json`）而**无平台原生对象** ⇒ 「路由可达 ≠ 平台可召唤」——即 `qdr_router_intents.json` 规则 `note` 里逐字自陈的那条诚实边界。

## 二、机制（部署器三步·**persona 在部署时从核读取**）

1. **枚举**：读第二源 `experts/expert_lib.json`（`id → skill_source`·该文件自陈「从核派生·禁手抄」）。
2. **取本体**：按 `skill_source` 读**技能核** `${QDR_HOST_SKILLS_DIR}/<skill>/SKILL.md`（`description` ＋ `能力边界`）与 `agents/<skill>.md`（persona 正文）。
3. **渲染落位**：以本模板为底，把**唯一占位符行**整行替换为该专家 persona，整体缩进挂到
   `- insert:` → `- id: preset-<id>` / `name: '@deepseek-ai/dsh-agent-preset'` / `config.{id,name,description,order,plugins}`
   之下，**按行 id no-clobber 合并**进 `${PLATFORM_CONFIG_DIR}/profiles/desktop/cordis.patch.yml`。

🛑 **本载体不含任何本体正文**（判据：模板内 0 处 `能力边界`／专家名／核语料）⇒ **本体一份（capabilities）· 适配一份（本文件）**，**零漂移**：核改一次，下次部署自动生效，无需改本件。

## 三、为什么是「声明行」而不是 `.agent-presets/` 目录（2026-09-27 一手取证）

DSH **`dsh≥0.1.7` 起不再读** `$DSH_HOME/.agent-presets/<id>/`：

| 证据 | 读数 |
|:--|:--|
| 随包技能 `dsh-agent-preset/skills/editing-cordis-compositions/SKILL.md`（迁移段） | 逐字「Before declaration rows, a user preset was a directory `$DSH_HOME/.agent-presets/<id>/` … **Nothing reads that directory any more.**」 |
| 安装体代码搜索 | `resources/app/lib`、`build` 全量搜 `.agent-presets` ⇒ **0 命中**（唯一 `agent-presets` 命中是客户端设置面板 section id，同名无关） |
| 注册表服务契约 | `agentPresets` ＝ *"Registry of **YAML-declared** presets"*；`list()` ＝ *"every **declared** preset"*；包 README 逐字「注册表不扫描目录，也不接受 preset 路径」 |
| 后果（本机实测） | `~/.dsh/.agent-presets/` 10 专家/团 ×2 文件**齐备**，而预设选择器**只见内置 4 个**（`standard`/`minimal`/`ptc`/`cordis`）⇒ 旧通道＝**有产物无投递通道**，且旧判据（目录内文件齐备＋persona 探针）**恒绿而漏** |

🔑 通则（本条已写进本面判据）：**判据域必须＝宿主真读的那个文件**。旧判据判的是「我们写了没」，不是「宿主读不读」——所以它能一直绿而对象一个都召唤不出来。

## 四、取证（2026-09-27 · A机）

| 项 | 读数 |
|:--|:--|
| 模板来源 | 平台随包 `standard` 组合（`node_modules/@deepseek-ai/dsh-web-app/presets/standard.patch.yml`）·**仅替换 `persona.prefix` 一行** |
| 载体规模 | **151 行**·占位符 **1** 处·**绝对路径 0 行**·**本体语料 0 处** |
| 包名可解析 | 模板引用 **27** 个 `@deepseek-ai/*` 包·**逐个在本机 DSH 安装中可解析**（旧载体死于 `@deepseek-ai/dsh-workflow-worker-thread`：该包在新版已不存在，逐字搬 ⇒ **激活期失败** ⇒ 选择器里显示 broken） |
| 生效面 | profile 补丁层声明 `patchReload: live` ⇒ 写入后刷新即生效（🛑 与「插件只在宿主启动时加载」不同轴，勿混） |

## 五、维护债（如实登记）

① 模板是**平台版本的快照**：平台升级若改动 `standard` 组合（新增/移除行或**改包名**），本件须**重新派生并复跑验收**（判据＝`--verify --host dsh` 全绿 ＋ 真机选择器可见）；
② DSH 无 MCP 暴露面 ⇒ 另一条通道（Cordis 插件 `dsh/qdr-intent-route`）与**本面互不替代**：插件管「意图感知」，本面管「专家对象可召唤」；两者写**同一个** profile 补丁文件，靠**行 id 不同**（`qdr-intent-route` vs `preset-<id>`）no-clobber 共存；
③ 各机目标根由**运行期解析**（平台配置根），🛑 本件不得写死任何机器路径；
④ 旧载体 `_template/agent.cordis.yml` **已删除**（旧方言·包名已重置 ⇒ 留着就是第二真相源兼静默失效源）；同名旧产物 `~/.dsh/.agent-presets/` 由部署器输出**逐条具名提示**待人工清理（本工具不擅自删宿主侧文件）。

## 六、🆕 **版本矩阵**（市场化口径：平台原生对象 = **版本绑定**的载体）

> **一手判例（2026-09-26/27 两机读数冲突）**：同一渲染逻辑 —— **B机（旧版 DSH）**：5 个预设逐个过 roster
> `standingKeyFor()` ⇒ **`MOUNT_OK` ×5**、`agentPresets.list()` 确认 `trust=user`；**A机（`dsh 0.1.7-rc.1`／
> Desktop 2.0.14）**：`~/.dsh/.agent-presets/` 10 目录/20 文件**齐备**而**预设选择器一个都不出现**。
> ⇒ 冲突的唯一解释＝**宿主版本差**；描述符 `platforms.dsh.expert_presets` 由单通道升级为**通道矩阵**（数据）。

| 宿主版本 | 通道 id | 载体（本目录） | 落点 | 判据 |
|:--|:--|:--|:--|:--|
| `dsh ≥ 0.1.7` | `declaration-row` | `agent_preset_row.yml`（新方言·插件条目表） | profile 补丁层 `${DSH_HOME}/profiles/desktop/cordis.patch.yml` 的 `- insert:` → `id: preset-<id>` / `name: '@deepseek-ai/dsh-agent-preset'` / `config.{id,name,description,order,plugins}` | 行在位 ∧ 解析后 `config.name/description` 非空 ∧ `plugins` 非空 ∧ persona 折叠归一逐字一致 |
| `dsh ≤ 0.1.6` | `legacy-dir` | `agent_dir/agent.cordis.yml`（旧方言·逐字保留旧包名） | `${DSH_HOME}/.agent-presets/<id>/{agent.cordis.yml,preset.yml}` | 两文件齐备 ∧ `preset.yml` 解析后非空 ∧ persona 探针在位 |

**通道选择判据（部署器 `_dsh_channel_probe`）**：①CLI `dsh --version`（区间 `cli_min`／`cli_max`）
②安装体内 preset **包名**（`dsh-agent-preset`＝新 ／ `dsh-agent-presets`＝旧；有界 glob·环境派生安装根·**零绝对路径**）。

🛑 **红线（fail-visible）**：**探测不可用 或 两方言同时命中 ⇒ 拒绝落位**——既**不默认**、也**不写双通道**。
理由（同为已证事实）：写错通道在**旧宿主**上＝未解析的 preset 模块行 ⇒ **整个 profile boot 失败（exit 1）**；
在**新宿主**上＝**静默死件**（写完没有任何消费者）。这条正是本次缺口的镜像（旧载体写了、没人读）。

🔑 **市场化含义**：①新增平台/新版本＝**改描述符矩阵一行**（零代码）；②「平台原生对象」这一层**必须逐版本取证**，
🛑 **不得用单机读数外推**（本判例：B机的 `MOUNT_OK` 在 A机**不成立**）；③凡「有产物」的适配面，其判据必须判
**宿主真读的那个载体**——只判「我们写了没」而不判「宿主读不读」，就会长期绿而对象一个都召唤不出来。
