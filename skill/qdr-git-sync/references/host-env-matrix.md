# 跨宿主环境变量与目录矩阵

> **用途**：`qdr-git-sync` 在非 WorkBuddy 宿主（DSH / Codex / 其他 AI 平台）上运行时的**环境适配参考**。
> **性质**：参考文档（reference）——SKILL.md 保有操作流程，本文件承载**宿主差异矩阵**与**故障处置**。

## 一、环境变量全表

| 变量 | 作用 | 默认值（WorkBuddy 宿主） | 其他宿主需设置 |
|:--|:--|:--|:--|
| `QDR_QDR_ROOT` | Q博士 根目录 | `__file__` 上溯两级 | ✅ 若目录结构不同 |
| `QDR_SKILLS_DIR` | 技能目录 | `~/.workbuddy/skills` | ✅ **必需**（`~/.dsh/skills` / `~/.codex/skills`） |
| `QDR_DATA_DIR` | 数据仓库 | `$QDR_ROOT/../Data-全局数据仓库` | ✅ **必需**（无默认） |
| `QDR_PAT_FILE` | 写权限 PAT 路径 | `~/.workbuddy/qdoctor_pat` | ✅ 若凭据位置不同 |
| `QDR_PAT_RO` | 只读 PAT（pull 用） | 无（回落到 `QDR_PAT`） | 使用者机器建议设置 |
| `QDR_GIT_PROXY` | git 代理 | `http://127.0.0.1:7897` | ✅ 空值 = 直连 |
| `QDR_GIT` | git 可执行文件 | `shutil.which('git')` | 一般无需 |
| `QDR_COSMOS_CLONE` | 云端公开库工作副本 | `$QDR_ROOT/../Cosmos.ai` | ✅ 位置不同时 |
| `QDR_SKILLS_DIR` | 同上 | — | — |

## 二、宿主目录映射（脚本内 `_HOST_MAP`）

| 宿主 | 判定依据 | 技能目录 |
|:--|:--|:--|
| `workbuddy` | 默认 | `~/.workbuddy/skills` |
| `dsh_global` | 宿主检测 | `~/.dsh/skills` |
| `codex` | 宿主检测 | `~/.codex/skills` |

> 判定由 `_detect_host()` 完成；`host_paths.py` 可用时优先其 `host_config_dir()`，否则回落 `~/.workbuddy`。

## 三、三通道（TARGETS）语义

| 通道 | 类型 | 目录 | 内容 | add_paths |
|:--|:--|:--|:--|:--|
| `main` | git | `$QDR_ROOT` | 治理核心（宪法/治理/脚本/drq） | 精确列举（constitution/governance/scripts/drq/reuse_core 等） |
| `capabilities` | git | `$QDR_SKILLS_DIR` | 技能 | `None`（`git add -A`） |
| `dataset` | git | `$QDR_DATA_DIR` | 数据资产 | `None` |

## 四、模式与保护语义

| 模式 | 角色 | 前置保护 | 失败时 |
|:--|:--|:--|:--|
| `push` | 治理者 | `behind>0` ⇒ **拒推** | 报 `conflict`·提示先 pull |
| `pull` | 使用者 | `ahead>0`/本地未提交 ⇒ 拒 `reset --hard` | 报错·不覆盖本地 |
| `integrate` | 双角色 | 备份分支 → commit → `merge <远端真实 sha>` → push | `merge --abort` **fail-closed** |
| `--list` | 诊断 | 无（只读） | — |

**真相源纪律**：分歧判定一律走 `git ls-remote`（**不依赖本地跟踪引用**——本仓库实证 `refs/remotes` 写入不可靠）。

## 五、故障处置表

| 症状 | 根因 | 处置 |
|:--|:--|:--|
| `[remote_unknown] 无法判定远端状态` | `ls-remote` 失败（**多为网络/代理抖动**） | **fail-closed 保护正确** ⇒ 检查代理后**重试**（非缺陷） |
| `[commit_failed]` 但 `reason` 为空 | 工作区无变更可提交（`nothing to commit` 也返回 exit=1）⇒ **假失败** | 用 `git log` 核对是否已同步（**T-60·判据待修**） |
| `[blocked_downgrade]` | **版本回退保护生效**（云端版本更高） | 核对版本；确需覆盖加 `--allow-downgrade` |
| `fatal: could not read Username` | 裸 `git` 无凭据（未走标准通道） | 🛑 **不要用裸 git**——走本脚本（内置 PAT/代理） |
| `fatal: unable to auto-detect email address` | 仓库 local `user.email` 未配置 | `git config --local user.email` 补齐 |
