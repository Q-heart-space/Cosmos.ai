---
name: qdr-external-publish
version: 1.0.0-ext
distribute_external: yes
space_scope: universal
reuse_depth: agnostic
scope_axis: distribute
layer: 枝·分发
usage_class: 治理类
task_type: 对外发布
circuit: ⑤自传播
triggers: 对外发布, 发布到公开库, 推送公开库, 公开库发布, 发布技能, publish external, 发到 Cosmos, 对外能力发布, 公开库合规检查, 发布回执, Q博士对外发布, Q博士发布
depends: publish_external
description: "Q博士 对外公开库发布技能——把 Q博士 内部技能/资产按标准流程发布到对外公开库（github.com/Q-heart-space/Cosmos.ai）。一条命令完成「切面门禁 -> 本地库 -> 云端库 -> 发布回执」全链路（零人工）。触发词：对外发布/发布到公开库/推送公开库/公开库发布/发布技能/公开库合规检查/发布回执。实现=AI 跑 scripts/publish_external.py（全自动发布器）。"
agent_created: true
deprecated: false
updated_at: 2026-09-19
---

# qdr-external-publish — Q博士 对外公开库发布技能

> **定位**：Distribute-External 出口的**自然语言入口**——把上面这条链路从「要记命令」变成「一句话触发」。
> **实现**：薄编排层，底层唯一执行体 = `scripts/publish_external.py`（v2.0）。本技能**不重造**任何逻辑。
> **规范**：`governance/对外公开库规范.md` §十一（标准发布流程）+ §十二（日志归档纪律）。

## 触发 → 动作路由

| 用户说 | 动作 | 命令 |
|:--|:--|:--|
| 「有哪些技能可以对外发」 | 列资格（分级） | `python scripts/publish_external.py --list` |
| 「XX 能发吗 / 差什么」 | 切面诊断（不写入） | `python scripts/publish_external.py --plan XX` |
| **「对外发布 XX」** | **全自动发布（本地库 + 云端库 + 回执）** | `python scripts/publish_external.py --execute XX --confirm` |
| 「只落本地库不推云端」 | 仅 S2 | 加 `--no-push` |
| 「公开库合规检查」 | 全量切面复验 + 回执覆盖核对 | 见下方「合规自检」 |

## 标准流程（四步·🛑 零人工）

```
S1 切面门禁   六切面全 pass（B3/B4/B5/B6/B7/B9）——不过即拒发
S2 本地库     源技能 -> products/公开库/skill/<name>/   （私有库内权威副本）
S3 云端库     同步 $(ROOT.parent)/Cosmos.ai -> commit -> push origin master
S4 回执       governance/data/transfer_events/TE-<ts>_<name>.json
```

**层位纪律**（规范 §11.4）：①源技能 → ②本地库（**权威**）→ ③云端工作副本（**只读派生·禁止直接编辑**）→ ④云端公开库

## 切面判据（`--plan` 判可执行性）

| 切面 | 判据 | 补法 |
|:--|:--|:--|
| B3 语义与适用域 | `space_scope != governance-core` | L0 技能天然满足 |
| B4 数据与证据 | `references/` **非空** | 补真实参考文档（🛑 不要放空占位） |
| B5 制度与信任 | `LICENSE` 存在 | 照云端 MIT：`Copyright (c) 2026 Q博士 (Q-heart-space)` |
| B6 技术执行 | 四件：`SKILL.md`+`references`+`scripts`+`role.json` | `role.json` = `{"role": "business"}`·空目录加 `.gitkeep` |
| B7 时间与版本 | `version` 带 `-ext` 后缀 | `X.Y.Z-ext`（2 段补零为 3 段） |
| B9 经济与激励 | `distribute_external: yes` | frontmatter 增字段 |
| **B8 依赖自闭环** | 依赖**本机脚本/内部技能/平台技能** ⇒ 硬阻断 | 内联 / 显式化 / 剥离 |
| **B10 归属与许可** | `_skillhub_meta.json`⇒平台技能🛑<br>upstream+AGPL/GPL⇒🛑许可冲突<br>upstream+宽松许可⇒⚠️须 NOTICE | 依 §十三（法律前置） |

🔑 `--list` 判**资格**（tier）· `--plan` 判**可执行性**（切面）⇒ **「可发」≠「能发」**。

## 🛑 两道内建保护（不可绕过）

1. **版本回退保护**：云端版本 > 源技能版本 ⇒ **拒发**（`blocked_downgrade`）。判据：**发布语义是推进，不是回退**。确需覆盖加 `--allow-downgrade`。
2. **切面硬门禁**：`eligible_for_publish=False` ⇒ **拒绝发布**。🛑 **不得"带病发布"**（判例：`qdr-git-sync` 曾因 `references/` 空而 B4 不过，仍被发布 ⇒ 2026-09-19 已修复重发）。

## 🛑 四道内建保护（不可绕过）

1. **版本回退保护**：云端版本 > 源 ⇒ **拒发**（`blocked_downgrade`）·判据=**发布语义是推进非回退**
2. **切面硬门禁**：`eligible_for_publish=False` ⇒ **拒绝发布**（不"带病发布"）
3. **B8 依赖自闭环**：依赖对外不可得对象 ⇒ **拒发**（`--ignore-deps` 可显式绕过）
4. **B10 归属与许可**：平台技能 / AGPL 衍生 ⇒ **拒发**（🛑 法律前置·**无绕过参数**）

## 域支持（🆕 v2.3）

`--domain {skill,decision,expert,methodology,whitepaper}`（默认 `skill`）。
🟡 **当前仅 `skill` 域已实现**（`status=implemented`）；其余 4 域为**契约预留**（规范 §五 域集）⇒ 无发布源与判据 ⇒ **fail-closed**。

## 合规自检（一条命令覆盖）

```bash
python scripts/publish_external.py --list                    # 全量资格与分级
python scripts/publish_external.py --plan <name>             # 单技能切面
ls governance/data/transfer_events/                          # 回执覆盖（每个已发布技能应有回执）
```

**合规判据（三条同时满足）**：
1. 切面 **6/6** 全 pass
2. 目录名 = 技能 `name`（**无 `-release` 等后缀**）
3. `transfer_events/` 存在该技能的**发布回执**（🛑 无回执 = 违反「没有迁移事件就没有可审计的跨」）

## 禁止行为

| ❌ | ✅ |
|:--|:--|
| 绕过 `publish_external.py` 手工 `cp` + `git push` | 走标准入口（回执与门禁才有保障） |
| 直接编辑 `$(ROOT.parent)/Cosmos.ai` 内的技能 | 改 ② 本地库后重发布（③ 是只读派生） |
| 切面不过仍发布 | 先补切面（`--plan` 看缺项） |
| 以 `git push 成功` 冒充「已发布」 | 云端直查实证（GitHub MCP / `ls-remote`） |

## 盲区与自审

- **盲区**：①本技能只编排，切面逻辑在 `publish_external.py`——脚本自身判据缺陷本层无法兜底（如 T-60 假失败）②`capabilities` 通道的子模块态（如 `guizang-ppt-skill`）不在本链覆盖范围 ③批量发布目前需逐个调用（无 `--execute-all`）。
- **自审**：发布后必须核对回执 + 云端可见性；两者缺一不得声明 Done。
