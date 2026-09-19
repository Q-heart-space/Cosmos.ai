# Get笔记 API 路由表

> Base URL: `https://openapi.biji.com`
> 构造请求时必须使用下表中的完整路径。如果收到 404，说明路径不对。

---

## 笔记

| 方法 | 路径 | 说明 | 详细文档 |
|------|------|------|----------|
| POST | `/open/api/v1/resource/note/save` | 新建笔记（文本/链接/图片） | [save.md](save.md) |
| POST | `/open/api/v1/resource/note/task/progress` | 查询异步任务进度 | [save.md](save.md) |
| GET  | `/open/api/v1/resource/note/list` | 笔记列表（分页） | [list.md](list.md) |
| GET  | `/open/api/v1/resource/note/detail` | 笔记详情 | [list.md](list.md) |
| POST | `/open/api/v1/resource/note/update` | 更新笔记 | [list.md](list.md) |
| POST | `/open/api/v1/resource/note/delete` | 删除笔记 | [list.md](list.md) |
| POST | `/open/api/v1/resource/note/sharing` | 创建笔记分享链接 | [list.md](list.md) |
| POST | `/open/api/v1/resource/note/tags/add` | 添加标签 | [tags.md](tags.md) |
| POST | `/open/api/v1/resource/note/tags/delete` | 删除标签 | [tags.md](tags.md) |
| GET  | `/open/api/v1/resource/image/upload_token` | 获取图片上传凭证 | [save.md](save.md) |

## 搜索

| 方法 | 路径 | 说明 | 详细文档 |
|------|------|------|----------|
| POST | `/open/api/v1/resource/recall` | 全局语义搜索 | [search.md](search.md) |
| POST | `/open/api/v1/resource/recall/knowledge` | 知识库语义搜索 | [search.md](search.md) |

## 知识库

| 方法 | 路径 | 说明 | 详细文档 |
|------|------|------|----------|
| GET  | `/open/api/v1/resource/knowledge/list` | 我的知识库列表 | [knowledge.md](knowledge.md) |
| GET  | `/open/api/v1/resource/knowledge/subscribe/list` | 订阅知识库列表 | [knowledge.md](knowledge.md) |
| POST | `/open/api/v1/resource/knowledge/create` | 创建知识库 | [knowledge.md](knowledge.md) |
| GET  | `/open/api/v1/resource/knowledge/notes` | 知识库笔记列表 | [knowledge.md](knowledge.md) |
| POST | `/open/api/v1/resource/knowledge/note/batch-add` | 添加笔记到知识库 | [knowledge.md](knowledge.md) |
| POST | `/open/api/v1/resource/knowledge/note/remove` | 从知识库移除笔记 | [knowledge.md](knowledge.md) |
| GET  | `/open/api/v1/resource/knowledge/bloggers` | 知识库博主列表 | [knowledge.md](knowledge.md) |
| GET  | `/open/api/v1/resource/knowledge/blogger/contents` | 博主内容列表 | [knowledge.md](knowledge.md) |
| GET  | `/open/api/v1/resource/knowledge/blogger/content/detail` | 博主内容详情 | [knowledge.md](knowledge.md) |
| GET  | `/open/api/v1/resource/knowledge/lives` | 知识库直播列表 | [knowledge.md](knowledge.md) |
| GET  | `/open/api/v1/resource/knowledge/live/detail` | 直播详情 | [knowledge.md](knowledge.md) |
| POST | `/open/api/v1/resource/knowledge/live/follow` | 关注直播 | [knowledge.md](knowledge.md) |
