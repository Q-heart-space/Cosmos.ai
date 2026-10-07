# 来源与边界 / Provenance and boundaries

## 来源 / Source

| 项 | 值 |
|:--|:--|
| **源分支** | `host-adapters` |
| **源路径** | `dsh/qdr-intent-route/` |
| **形态 / form** | `plugin` |
| **宿主** | DSH（Cordis 插件机制） |
| **入云方式** | 🅑 **逐件字节拷贝**（🅑 非重写） |

## 为什么它可以对外 / Why it qualifies

| 🎯 轴 | 🎯 判据 | 🎯 实测 |
|:--|:--|:--|
| **产物轴** | 有**与实例无关的可分发定义** | ✅ `cordis.patch.yml`（装载补丁）＋ `package.json`（`main`/`exports`） |
| **依赖轴** | 重建依赖**全为公开可得**·私有项**外置为自填** | ✅ 🅑 本机路径**仅出现在注释之判例记录**中；装载补丁用 `file:///…/plugin.js` 且以 **`<you>` 占位**明示由使用者自填 |
| **form** | `mcp` / `plugin` / `automation` | ✅ **`plugin`** |

## 它做什么 / What it does

🅑 **订阅会话的用户消息事件**，做**意图识别**并把证据写入台账 —— 🅑
即「在 DSH 上让意图路由这套机制真的跑起来」的那一层。

## 边界 / Boundaries

- 🅑 本件是**宿主接线层**，🛑 **不是能力本体**；
- 🅑 需**宿主支持 Cordis 插件**方可装载（🅑 其补丁文件即装载描述）；
- 🅑 装载前请把补丁里的 `__QDR_INTENT_ROUTE_PLUGIN_URL__` 换为你自己的 `file://` URL。
