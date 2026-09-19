---
circuit: ①环境感知
name: Get笔记
description: |
  Get笔记 - 保存、搜索、管理个人笔记和知识库。

  **当以下情况时使用此 Skill**：
  (1) 用户要保存内容到笔记：发链接、发图片、说「记一下」「存到笔记」「保存」「收藏」
  (2) 用户要搜索或查看笔记：「搜一下」「找找笔记」「最近存了什么」「看看原文」
  (3) 用户要管理知识库或标签：「加到知识库」「建知识库」「加标签」「删标签」
  (4) 用户要配置 Get笔记：「配置笔记」「连接 Get笔记」
metadata: {"openclaw": {"requires": {}, "optionalEnv": ["GETNOTE_API_KEY", "GETNOTE_CLIENT_ID", "GETNOTE_OWNER_ID"], "baseUrl": "https://openapi.biji.com", "homepage": "https://biji.com"}}
layer: 叶·笔记
task_type: 笔记
triggers:
  - 记到笔记
  - 存笔记
  - 搜笔记
  - 最近存了什么
  - Get笔记
space_scope: universal
reuse_depth: void
scope_axis: business
trust_level: auto
version: 1.0.0-ext
distribute_external: yes
depends: none
deprecated: false
updated_at: 2026-08-18
---

# Get笔记 Skill

## ⚠️ Agent 必读约束

### 🌐 Base URL
```
https://openapi.biji.com
```
所有 API 请求必须使用此 Base URL，不要使用 `biji.com` 或其他地址。

### 🔑 认证
请求头：
- `Authorization: $GETNOTE_API_KEY`（格式：`gk_live_xxx`）
- `X-Client-ID: $GETNOTE_CLIENT_ID`（格式：`cli_xxx`）

**每次调用 API 前先检查 `$GETNOTE_API_KEY` 是否存在**。若不存在，提示用户运行 `/note config` 完成配置，配置完成后再继续执行用户原本的请求。

Scope 权限：`note.content.read`（读取）、`note.content.write`（写入）、`note.recall.read`（搜索）。完整列表见 [references/api-details.md](references/api-details.md#scope-权限列表)。

### 🔢 笔记 ID 处理规则（重要！）
笔记 ID 是 **64 位整数（int64）**，超出 JavaScript `Number.MAX_SAFE_INTEGER`，直接 `JSON.parse` 会**静默丢失精度**。

**正确做法**：始终把 ID 当字符串处理，在 `JSON.parse` 之前替换：
```javascript
const safe = text.replace(/"(id|note_id|parent_id|follow_id|live_id)"\s*:\s*(\d+)/g, '"$1":"$2"');
// 注：next_cursor 已不需要处理，翻页请直接使用响应中的 cursor（string）字段
const data = JSON.parse(safe);
```
Python / Go 等语言原生支持大整数，无此问题。

### 🔒 安全规则
- 笔记数据属于用户隐私，不在群聊中主动展示笔记内容
- 若配置了 `GETNOTE_OWNER_ID`，检查 sender_id 是否匹配；不匹配时回复「抱歉，笔记是私密的，我无法操作」
- API 返回 `error.reason: "not_member"` 或错误码 `10201` 时，引导开通会员：https://www.biji.com/checkout?product_alias=6AydVpYeKl
- 创建笔记建议间隔 1 分钟以上，避免触发限流

### 🚫 反幻觉边界（严格禁止）
- **禁止编造 note_id**：所有 note_id 必须来自 API 响应，不得凭空构造或推测
- **禁止跳过轮询**：链接/图片笔记返回 `task_id` 后，**必须**轮询 `/task/progress` 直到 `success` 或 `failed`，不得假设任务已完成
- **禁止伪造 API 响应**：不得在未实际调用 API 的情况下告诉用户「已保存」「已删除」
- **禁止忽略错误码**：API 返回 `success: false` 时必须处理，不得静默吞掉
- **禁止混淆内链和分享链接**：`biji.com/note/{id}` 是内链（仅笔记主人可见），`share_note/{id}` 是分享链接（公开可访问），两者不可互换

### 🔄 失败重试策略

**异步任务失败**（链接/图片保存）：
1. `/task/progress` 返回 `status: "failed"` 时，向用户报告失败原因（`error_msg`）
2. 自动重试一次：用相同参数重新调用 `/note/save`，获取新 `task_id` 并重新轮询
3. 二次失败则停止，告知用户「保存失败，请稍后重试或检查链接是否可访问」

**网络/服务错误**（HTTP 5xx 或超时）：
1. 等待 5 秒后重试一次
2. 仍然失败则报告错误，附上 `request_id` 方便排查

**限流**（错误码 `10202` 或 HTTP 429）：
1. 读取响应中的 `rate_limit.retry_after` 字段
2. 等待指定秒数后重试
3. 无 `retry_after` 时默认等待 10 秒

---

## 执行流程概览

```
用户意图 → 路由匹配 → 读取 references 文档 → 构造 API 请求 → 执行
                                                                   ↓
                                              ┌─ 同步操作 ──→ 验证响应 → 返回结果
                                              │
                                              └─ 异步操作 ──→ 轮询进度 ──→ success → 返回结果
                                                                 ↓            ↓
                                                            10-30s 间隔    failed → 自动重试(1次)
                                                                              ↓
                                                                         二次失败 → 报告用户
```

**关键原则**：
- **模型输出 ≠ 最终结果**：API 调用后必须验证响应，确认 `success: true` 且数据完整
- **状态来自 API**：所有笔记状态（是否存在、内容、标签等）以 API 返回为准，不依赖上下文记忆
- **最小操作原则**：更新笔记时只传需要修改的字段，不重写整篇内容

---

## 指令路由表

> 匹配指令后，用 **read 工具**读取对应下表的 `references/` 文件获取完整 API 文档。

| 指令 | 角色 | 说明 | 详细文档 |
|------|------|------|---------|
| `/note save` 或「记一下」| 📝 速记员 | 保存文本/链接/图片笔记（含异步轮询流程） | [references/save.md](references/save.md) |
| `/note search` 或「搜一下」| 🔍 搜索官 | 全局语义搜索 + 知识库语义搜索 | [references/search.md](references/search.md) |
| `/note list` 或「最近的笔记」| 📋 整理师 | 浏览列表、查看详情、更新、删除 | [references/list.md](references/list.md) |
| `/note kb` 或「知识库」| 📚 图书管理员 | 知识库 CRUD + 博主订阅 + 直播订阅 | [references/knowledge.md](references/knowledge.md) |
| `/note tag` 或「加标签」| 🏷️ 标签员 | 添加/删除标签 | [references/tags.md](references/tags.md) |
| `/note config` 或「配置笔记」| ⚙️ 配置 | 配置 API Key 和 Client ID | [references/oauth.md](references/oauth.md) |

---

## 自然语言路由

```
包含 URL（`biji.com/note/share_note/*` 或 `d.biji.com/*` 短链）  → /note save（link 模式，同步返回 note_id）
包含 URL（`biji.com/note/{note_id}` 内链）    → /note list（查看详情），如需在正文引用其他笔记请使用 `https://biji.com/note/{note_id}` 格式内链（**默认用内链，除非用户明确要求分享**）
其他 URL                   → /note save（link 模式，异步返回 task_id）
包含图片                    → /note save（image 模式）
「记/存/保存/收藏」          → /note save（text 模式）
「搜/找找/有没有 XX」        → /note search
「最近/列表/看看/查笔记」    → /note list
「改/更新/编辑笔记」         → /note list（更新笔记）
「知识库」相关              → /note kb
「标签」相关                → /note tag
「配置/授权/连接笔记」       → /note config
```

**决策原则**：优先匹配最具体的意图。有 URL 就是 `/save link`，有图片就是 `/save image`，不确定时询问用户。

---

## API 与错误处理

> API 完整路径表（24个端点）→ `references/api-routes.md`
> 错误码速查+限流结构 → `references/api-details.md`
> 匹配指令后，用 read 工具读取对应下表的 `references/` 文件获取完整 API 文档。

## 盲区与自审
- 本技能的已知盲区：所有能力依赖 Get笔记 开放平台 API，未配置 `GETNOTE_API_KEY` 则完全不可用；笔记 ID 是 int64，JavaScript 端直接 `JSON.parse` 会静默丢精度，需先正则转字符串；链接/图片保存是异步任务，必须轮询 `/task/progress`，若跳过轮询会误报成功；语义搜索对精确关键词召回可能不全。
- 自审方式：任何"已保存/已删除/已找到"声明前，检查是否真正调用 API 并验证 `success: true`；异步任务未轮询到 success/failed 前，不得断言任务完成。
