# integration/ — 接进你系统的单元 / Units you can wire in

本域收录可**接进你现有系统**的单元。面向「**我要把它接进我的系统**」的使用者。

Units that can be wired into a system you already run — for people who want to plug a capability in.

## 内容 / Contents

| 目录 · Directory | 你能拿到什么 · What you get |
|:--|:--|
| [`ai-drift-guard/`](ai-drift-guard/) | 一个可装载的**跑偏守卫**（含其分发定义与装载补丁） |

## 收录判据 / Inclusion criteria

1. 🎯 **产物轴** —— 存在**与实例无关**的可分发定义（manifest / schema），使你能**重建等价实例**；
2. 🎯 **依赖轴** —— 重建依赖**全为公开可得**；私有项已**外置为你自填的配置**；
3. 🎯 **形态** —— 以 `form` 字段标明（`mcp` / `plugin` / `automation`）。

## 边界 / Boundaries

- 🛑 **实例运行态**（会话、凭据、机器标识）不随件发出；
- 🛑 依赖不清者不入；
- 🅑 本域只收**能独立装载**的单元，不收「在本组织内才跑得起来」的东西。
