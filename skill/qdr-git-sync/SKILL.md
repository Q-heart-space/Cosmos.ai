---
name: qdr-git-sync
version: 5.0.1-ext
distribute_external: yes
layer: 枝·同步
task_type: Git 同步
triggers: 推送Q博士, 同步Q博士, 拉取Q博士, push Q博士, pull Q博士, Q博士推送, Q博士拉取, Q博士同步, 拉取Q博士能力, 同步Q博士能力, 回传给Q博士, 回传, 注入认知, 注入, 验证第三空间
depends: qdr_sync_all
description: "Q博士 多机·多宿主·多角色 完整闭环技能 v5.0.1——能力外溢四机制（技能化/注入/回传/动作化）+ 双角色（push/pull）+ 跨宿主。触发词：推送Q博士/拉取Q博士/同步Q博士/回传给Q博士/注入认知。实现=AI 跑 scripts/qdr_sync_all.py（分发·git 快）+ business_space_harvest_push（回传）+ business_space_feeder（注入）。"
space_scope: universal
reuse_depth: agnostic
scope_axis: governance
circuit: ⑤自传播
agent_created: true
deprecated: false
updated_at: 2026-09-14
---

# Q博士 完整闭环（qdr-git-sync）v5.0

> **用途**：多机多角色同步 + 能力外溢四机制接线（对齐本质定位 §1.9.3 · 五通道联动协议 v1.9）。
> **实现**：分发=qdr_sync_all.py（git 快）· 回传=business_space_harvest_push.py · 注入=business_space_feeder.py + memory_context_injector.py + meta_pull.py · 动作化=standard_bridge.py。

## 能力外溢四机制（权威框架·本质定位 §1.9.3）

| 机制 | 通道 | 存量实现（复用不重造） |
|:--|:--|:--|
| ① 技能化 | Distribute-External | skill_sync + sync_portable_build |
| ② 注入（认知供给） | Distribute-Internal | business_space_feeder.py（铁律继承指针+META锚点）+ memory_context_injector.py + meta_pull.py |
| ③ 回传（采纳证据） | Harvest-Internal | business_space_harvest_push.py（三载体分流） |
| ④ 动作化（envelope） | Distribute-External/Connector | standard_bridge.py + qdr_action_cli + qdr_mcp_server |

> 🛑 **记忆文件注入是前提**：②注入的 business_space_feeder.py「铁律继承指针」注入 L1 三件套单行引用——没有它业务空间无法加载铁律 U（IPC 铁律 U 违规根因·T-3-1367）。

## 完整闭环（五环节·多机同步视角）

```
治理者（A 机）                使用者（B 机）
  │ ① 分发 push ─────────────→  │
  │ ⑤ 消费回传 ←────────────────│
  │        ② 拉取 pull ←───────│
  │        ③ 注入（认知）→──────│
  │        ④ 回传（反馈）←──────│
  └──────── 更新能力 → 再分发（闭环）┘
```

| 环节 | 触发词 | 机制（存量·复用不重造） | 角色 |
|:--|:--|:--|:--|
| ① 分发 | 「推送 Q博士」 | qdr_sync_all.py --mode push（认领 T-4-008） | 治理者 |
| ② 拉取 | 「拉取 Q博士」 | qdr_sync_all.py --mode pull + meta_pull.py | 使用者 |
| ③ 注入 | 「注入认知」 | business_space_feeder.py（铁律继承指针+META 锚点）+ memory_context_injector.py + meta_pull.py | 使用者 |
| ④ 回传 | 「回传给 Q博士」 | business_space_harvest_push.py（三载体分流） | 使用者 |
| ⑤ 消费 | 「同步 Q博士」 | qdr_sync_all.py --mode integrate（规范名·`sync` 为兼容别名）+ harvest_consumer | 治理者 |

> 🛑 **记忆文件注入是前提**：business_space_feeder.py 的「铁律继承指针」注入 L1 三件套单行引用（BZ.1）——没有它，业务空间无法加载铁律 U，无法执行写操作（IPC 铁律 U 违规根因·T-3-1367）。

## 触发词与角色

| 用户说 | 模式 | 角色 | 做什么 |
|:--|:--|:--|:--|
| **「推送 Q博士」** | `push` | 治理者 | 本地改动 → 远端（需要写权限 PAT） |
| **「拉取 Q博士」** | `pull` | 使用者 | 远端能力 → 本地（reset --hard 覆盖本地改动） |
| **「同步 Q博士」** | `integrate`（别名 `sync`） | 双角色 | **双向收敛（唯一出路）**：备份 → commit → merge（**不重写 SHA**）→ push；冲突 **fail-closed** |
| **「回传给 Q博士」** | harvest | 使用者 | 反馈/发现 → harvest_state.json（三载体分流） |
| **「注入认知」** | inject | 使用者 | META/记忆 → 会话（qdr.knowledge.pull） |

**核心洞察（🆕 2026-09-16 补「宿主级角色」维度）**：

角色可以**按机器分配**，也可以**按宿主分配**（同一台机器上，两个宿主扮演不同角色）：

| 粒度 | 示例 | PAT 要求 |
|:--|:--|:--|
| **机器级** | A 机（治理者+双角色）· B 机（只使用） | 按机器配一把钥匙 |
| **宿主级** ⭐ | B 机：**DSH=治理者**（写）· **WorkBuddy=使用者**（只读） | **同机两把钥匙**（权限隔离·WorkBuddy 误操作改不坏云端） |

**三种典型配置**：
- **A 机（治理者+双角色）**：需要完整 PAT（repo 权限），既推又拉
- **B 机（宿主级分工·推荐）**：DSH 持写 PAT（治理者）· WorkBuddy 持只读 PAT（使用者）
- **B 机（只使用）**：只读 PAT（public_repo）即可，「拉取 Q博士」就能用最新能力

> 📖 **B 机首次安装完整手册**（人类向·权威）：
> `deliverables/[操作手册]B机业务使用者首次安装与拉取_20260914.md`
> 🛑 **业务使用者 ≠ 治理者 B 机**——业务使用者走「公开渠道便携版」（无需 PAT）；治理者 B 机才用 `bootstrap_install.py` + PAT + 拉取私库。

## 四空间定位（🆕 2026-09-16 治本）

> **本质**：单仓库承载四个**语义空间**——不是「同一内容的多版本分支」，而是「不同内容的容器」。
> **治本规则**：各空间**只含本空间特有内容**——治理核心（constitution/governance/drq/scripts）**只在 main**，
> 其他空间**禁止含其副本**（2026-09-16 前四支各继承一份核心·已实证漂移：`concept_registry.json` main `802c4ca0` vs 其余 `50b48009`）。
> **配置源（唯一真相源）**：`governance/data/space_location_map.json`。宪法锚点：`constitution/系统架构.md` §4.5a。

| 空间 | 分支 | 本地物理位置 | 本质 | 内容 |
|:--|:--|:--|:--|:--|
| **main** | `main` | `$QDR_ROOT`（`D:/Workbuddy/Q博士`） | 治理本体（平台中立） | 宪法/脚本/治理/drq |
| **capabilities** | `capabilities` | `~/.workbuddy/skills`（宿主物理约束） | 能力载体 | 技能（跨空间方法论） |
| **dataset** | `dataset` | `Data-全局数据仓库` | 数据资产 | 数据/脚本/注册表 |
| **host-adapters** | `host-adapters` | `.codex` + `.dsh`（宿主物理约束） | 宿主接入产物 | 各平台特有产物（`AGENTS.md`·宿主桥·MCP 配置） |
| **外部公开面（Cosmos.ai）** | `-`（独立公开仓库 `Q-heart-space/Cosmos.ai`） | `github.com/Q-heart-space/Cosmos.ai` | 对外公开库·与四空间正交 | **Distribute-External 出口**：脱敏派生知识·按**对外能力六域**分类（`skill/`·`expert/`·`methodology/`·`whitepaper/`·`case/`·`resource/`）·技能归入 `skill/<技能名>/` |

## 跨宿主环境变量（适配不同 AI 平台目录）

| 环境变量 | 作用 | 默认值（兼容当前 A 机） |
|:--|:--|:--|
| `QDR_PAT` | 写权限 PAT 路径 | `~/.workbuddy/qdoctor_pat` |
| `QDR_PAT_RO` | 只读 PAT（pull 模式用） | （无·默认用 QDR_PAT） |
| `QDR_GIT_PROXY` | 代理 | `http://127.0.0.1:7897` |
| `QDR_SKILLS_DIR` | 技能目录 | `~/.workbuddy/skills` |
| `QDR_DATA_DIR` | 数据仓库目录 | **必需**（无默认） |

**B 机（只装 DSH）配置示例**：
```cmd
set QDR_SKILLS_DIR=C:\Users\you\.dsh\skills
set QDR_DATA_DIR=D:\Workbuddy\Data-全局数据仓库
set QDR_GIT_PROXY=        REM 空=直连
python scripts/qdr_sync_all.py --mode pull   REM 使用者拉
```

## 跨 AI 平台（MCP）

能力以 **MCP server** 形式暴露（`qdr_mcp_server`），**任何支持 MCP 的 AI 平台**（Claude/Cursor/OpenAI Agent SDK/未来平台）都能连接 Q博士 的能力，不依赖特定平台的 skills 目录格式。

## 执行方式（AI 在对话里收到触发词后）

```bash
cd /d "D:\Workbuddy\Q博士"
python scripts/qdr_sync_all.py --list                          # dry-run
python scripts/qdr_sync_all.py --mode push                    # 治理者推
python scripts/qdr_sync_all.py --mode pull                    # 使用者拉
python scripts/qdr_sync_all.py --mode integrate               # 治理者+使用者：双向收敛（唯一出路）
python scripts/qdr_sync_all.py --mode sync                    # 同上（兼容别名·历史文档写法）
python scripts/qdr_sync_all.py --mode push --target capabilities   # 只推能力
```

> 🛑 **双向分叉必须用 `integrate`（第一原理）**：`push` 因 `behind>0` 拒绝（要求先 pull）·`pull` 因 `ahead>0` 拒绝（要求先 push）——**两侧互为对方前置条件 ⇒ 无出路**（T-33 实证：main 曾静默积压 27 提交跨一天）。`integrate` 是唯一同时满足两侧前置的动作：**备份 → commit → merge（不重写 SHA）→ push**，冲突则 `merge --abort` 回到合入前并报 `merge_conflict`（fail-closed·不自动解冲突）。
> 🛑 **未知 `--mode` fail-closed**：v2.8 起模式未校验即报错退出（exit=1），**不再静默降级为 push**。

## 安全门禁

- PAT 存 `~/.workbuddy/qdoctor_pat`（已被 .gitignore 排除）
- 脚本内置忽略凭证：`.enc`/`.key`/`.master.key`/`.credentials.*.json`/`token`/`mcp.json`/`API-Credentials.md`
- 忽略大目录：`Backups`/`versions`/`staging`/`workspace`
- pull 模式用 `reset --hard`（强制同步·本地改动丢失·只用于「使用者拉」场景）
- `integrate` 模式**不重写历史**（用 `merge` 非 `rebase/force`）· 合入前自动建 `backup/integrate-<target>-<ts>` 分支可一键回退 · 冲突 **fail-closed**（`merge --abort` 后报错·不自动解冲突）
- B 机（只使用）应用 `QDR_PAT_RO`（只读 PAT），无写权限→安全

## 边界

- ✅ 四空间（main/capabilities/dataset/host-adapters）·各空间**只含本空间特有内容**
- ✅ 治理核心只在 main·其他空间**禁止含副本**（治本规则 2026-09-16·防「一份内容四份副本」漂移）
- ✅ 三模式：push（治理者推）/ pull（使用者拉·`reset --hard`）/ integrate（双角色·**双向收敛唯一出路**·不重写 SHA·冲突 fail-closed）
- ✅ 跨宿主：环境变量适配任何 AI 平台目录
- ✅ 跨 AI 平台：MCP server 暴露
- ❌ 不做定时自动化（那是 automation 职责）
- ❌ `git add -A` 不会加临时文件（_*.py/_*.txt/*.write_guard_tmp 等已忽略）

## 产品化场景

| 机器 | 角色 | 触发 | 模式 | PAT |
|:--|:--|:--|:--|:--|
| A 机（开发·治理者） | 治理者+使用者 | 「推送 Q博士」 | push | repo 写 |
| B 机（开发·治理者分身） | 治理者+使用者 | 「推送 Q博士」 | push | repo 写 |
| B 机（生产·使用者） | 使用者 | 「拉取 Q博士」 | pull | public_repo 读 |