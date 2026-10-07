# `intent-route-shared` —— 字段说明（schema v2）

> **域**：`data/`（接收方问题＝「**我要这份可共享的数据**」）
> **来源支**：`dataset` ｜ **路径**：`intent_route_shared/`
> **规模（源支）**：**1791 件**（2026-09：1408 ／ 2026-10：383）·🅑 每件约 300 B
> **脱敏标记**：🅑 每件自带 **`scope: "shared_deidentified"`** ⇒ **本就为共享而生**

## 一、这是什么

🎯 **意图路由的跨宿主事件流** —— 每条记录**一次意图路由判定**的元数据（🛑 **不含用户内容**）。

## 二、字段（🅑 逐字段·取自实件）

| 字段 | 类型 | 含义 |
|:--|:--|:--|
| `schema_version` | int | 本 schema 之版本（现为 **2**） |
| `event_id` | str | 事件唯一标识（形态 `<宿主>-<hex>`） |
| `timestamp` | str | ISO 8601 UTC（含微秒） |
| `scope` | str | 🎯 **共享范围** —— `shared_deidentified` ⇒ **已脱敏·可共享** |
| `host` | str | 判定发生之**宿主**（如 `dsh`／`workbuddy`／`codex`） |
| `quadrant` | str | 路由之**四象限**归类（如 `Q2`） |
| `channel` | str | 命中通道（如 `fallback` ⇒ 未命中专用路由） |
| `delta_type` | str | 增量类型（如 `add`） |
| `confidence` | int | 置信度（**0** ⇒ 未判/低信） |
| `degrade_reason` | str | 降级原因（空串 ⇒ 无降级） |
| `covered` | bool | 是否已被既有规则覆盖 |

## 三、一件之实（🅑 原始）

```json
{ "schema_version": 2, "event_id": "dsh-<hex>",
  "timestamp": "2026-10-01T07:35:59+00:00",
  "scope": "shared_deidentified", "host": "dsh", "quadrant": "Q2",
  "channel": "fallback", "delta_type": "add",
  "confidence": 0, "degrade_reason": "", "covered": false }
```

## 四、🛑 已知边界（🅑 诚实标注）

- 🎯 **本目录给的是**样本 ＋ 字段说明**（🅑 样本用于看清一条记录长什么样）——
  🅑 完整时间序列**不在本目录**；🅑 你若需要**统计口径**，按下方字段自行聚合即可。
- 🅑 **本目录只含样本与字段说明** —— 🅑 其余内容**不在本目录**。
- 🛑 **本目录不收**他人主体的业务数据**（🅑 无论是否脱敏）**。
