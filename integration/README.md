# integration/ — 接进你系统的单元 / Units you can wire in

本域收录可**接进你现有系统**的单元。面向「**我要把它接进我的系统**」的使用者。

Units that can be wired into a system you already run — for people who want to plug a capability in.

## 内容 / Contents

| 目录 · Directory | 你能拿到什么 · What you get | 形态 · form |
|:--|:--|:--|
| [`ai-drift-guard/`](ai-drift-guard/) | 一个可装载的**跑偏守卫**（含其分发定义与装载补丁） | `plugin` |
| [`qdr-intent-route/`](qdr-intent-route/) | **意图路由的宿主对接层**（订阅会话消息 → 识别意图 → 写证据） | `plugin` |
| [`agents-bootstrap/`](agents-bootstrap/) ／ [`codex-bootstrap/`](codex-bootstrap/) ／ [`dsh-bootstrap/`](dsh-bootstrap/) ／ [`hermes-bootstrap/`](hermes-bootstrap/) ／ [`openclaw-bootstrap/`](openclaw-bootstrap/) ／ [`workbuddy-bootstrap/`](workbuddy-bootstrap/) | **落位清单**：逐件声明「来源 ＋ 摘要 ＋ 目标路径」⇒ 你能**按清单落位并自校验** | `plugin` |

## 收录判据 / Inclusion criteria

1. 🎯 **产物轴** —— 存在**与实例无关**的可分发定义（manifest / schema），使你能**重建等价实例**；
2. 🎯 **依赖轴** —— 重建依赖**全为公开可得**；私有项已**外置为你自填的配置**；
3. 🎯 **形态** —— 以 `form` 字段标明（`mcp` / `plugin` / `automation`）。

## 边界 / Boundaries

- 🛑 **实例运行态**（会话、凭据、机器标识）不随件发出；
- 🛑 依赖不清者不入；
- 🅑 本域只收**能独立装载**的单元，不收「在本组织内才跑得起来」的东西；
- 🅑 **落位清单不含文件本体** —— 本体随各自技能/专家包分发；🅑 其目标路径以 `${PLATFORM_CONFIG_DIR}` 占位，**落位前请替换为你自己的配置目录**。

## 怎么用 / How to use

1. 🅑 选你所在宿主的 `*-bootstrap/manifest.json`；
2. 🅑 读其 `files[]` —— 每项给 `src`（来源）、`sha256`（摘要）、`dst`（目标）；
3. 🅑 把 `dst` 里的 `${PLATFORM_CONFIG_DIR}` 换为**你自己的**配置目录；
4. 🅑 落位后**核摘要** —— 不符即文件已变。
