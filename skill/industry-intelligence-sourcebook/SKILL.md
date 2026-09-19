---
name: industry-intelligence-sourcebook
description: 行业情报源手册（知识型技能·无用户触发词·供自动化任务和跨项目复用）——提供经验证的竞品公司/展会/标准组织/官渠/媒体分层清单。支持IPC、海事、AI智能体等行业。
contract: "@contract:skill scripts:validate_sourcebooks.py"
circuit: ④知识
version: 1.1.1-ext
distribute_external: yes
depends: references/sourcebook.schema.json
layer: 叶·情报源
task_type: 情报源
triggers:
  - 行业情报源
  - 竞品公司清单
  - 展会清单
  - 标准组织清单
  - 情报源配置
space_scope: universal
reuse_depth: org-parameterized
scope_axis: business
trust_level: notification
deprecated: false
updated_at: 2026-08-26
---

# Industry Intelligence Sourcebook（行业情报源手册）

## 概述

本技能是一个**知识型技能**（非执行型）——不主动搜索/调用API，仅提供经过验证的行业情报源配置数据。核心价值在于将"行业知识和信源配置"从自动化 prompt 中解耦，实现跨项目、跨技能复用。

## 支持行业

| 行业 | 配置文件 | 状态 |
|:--|:--|:--|
| IPC（工业计算机·Industrial PC） | `references/ipc_sourcebook.json` | ✅ 活跃（2026-07-02） |
| 海事（Maritime·海事工控机） | `references/maritime_sourcebook.json` | ✅ 活跃（2026-07-02，提取自海事工控机研究报告） |
| AI 智能体/治理（AI Agent·🆕 2026-08-26） | `references/ai_agent_sourcebook.json` | 🔜 v1.0（初建·待验证·服务 Q博士 自身竞品/外部情报） |
| 其他行业 | — | 🔜 按需扩展 |

## 使用方式

### 场景1：自动化任务中获取信源配置

1. 加载本技能
2. 读取对应行业的 sourcebook JSON（如 `references/ipc_sourcebook.json` / `references/ai_agent_sourcebook.json`）
3. 提取所需配置块：
   - `search_whitelist` — 搜索白名单域名（国内外分轨）
   - `competitors` — 竞品清单和层级
   - `exhibition_calendar` — 展会日历
   - `query_templates` — 搜索词模板（含展会季专属模板）
   - `cross_validation` — 交叉验证规则和中英文厂商/术语映射
   - `scoring` — 6维评分规则和阈值
4. 按配置执行搜索、评分、验证流程

### 场景2：报告撰写中获取竞品对比清单

1. 加载本技能 → 读取 `competitors`
2. 获取厂商中英文名称映射、官网域名、核心参展展会、所属层级
3. 作为竞品分析的对照组数据源

### 场景3：展会季节定制搜索

1. 加载本技能 → 读取 `exhibition_calendar`
2. 判断当前月份是否有展会
3. 如有 → 从 `query_templates.expo_season` 获取该展会的专属搜索词
4. 如有重点竞品 → 从 `competitors.*.core_expos` 确认是否参展 → 激活反向扫描

### 场景4：交叉验证

1. 加载本技能 → 读取 `cross_validation`
2. 将国内源提到的厂商/事件通过 `cn_to_intl_mapping` 转换为英文关键词
3. 在国际源中搜索交叉确认
4. 反向同理

## 数据结构

所有行业配置文件均遵循 `references/sourcebook.schema.json` 定义的统一结构。主要配置块：

| 配置块 | 说明 | 示例 |
|:--|:--|:--|
| `source_pyramid` | 4层信源金字塔（L1-L4），每层含厂商/标准组织/展会/媒体 | 每条含 `domains`（全区域域名）+ `social_media`（微信/B站/抖音/知乎）+ P0字段（`verification`/`parent_entity`/`content_type`/`aliases`/`ttl`/`compliance`） |
| `source_pyramid.L2_quasi_official` | 准官方（协会/展会/技术联盟） | embedded world、PICMG |
| `source_pyramid.L3_trusted_secondary` | 可信二手源（行业垂直媒体） | automationworld.com |
| `source_pyramid.L4_supplementary` | 补充参考（泛科技/门户） | xinhuanet.com、prnewswire.com |
| `competitors` | 竞品分层清单+参展追踪配置 | primary/secondary/watch |
| `exhibition_calendar` | 年度展会日历+竞品参展关联 | 3月embedded world → 研华/诺达佳/智微 |
| `search_whitelist` | 搜索白名单（国内/国际/竞品分轨） | 业界共识的高信号域名 |
| `query_templates` | 搜索词模板（泛化+展会季+竞品专项） | 含动态占位符 {year}/{month} |
| `cross_validation` | 交叉验证规则+中英文映射 | ≥2个独立源确认 |
| `scoring` | 6维评分卡+阈值+交叉验证加成 | 满分94，阈值45 |
| `verification` (P0) | 信源资质：最近验证日期/方式/状态/资质证明 | `status`: active/suspicious/deprecated |
| `parent_entity` (P0) | 实际控制实体，用于独立性判定（防止同集团多域名误判为独立源） | 如 EE Times China + EETimes → AspenCore |
| `content_type` (P0) | 信源内容类型，驱动噪音过滤（新闻稿/独立报道/标准文件/政策文件等） | 11种枚举：official_announcement/independent_reporting 等 |
| `ttl` (P0) | 信源有效期与采集频率（daily/weekly/monthly/event_driven）·🆕 2026-08-24 实践指南：**按变化频率定 ttl**（IPC 回传 META 落位）——快变量（价格/新闻/库存）→ daily·中变量（产品规格/渠道政策）→ weekly·慢变量（认证/产品定位·首发确定数月才变）→ monthly 或 event_driven（信号触发深挖/复用·不硬抓）·判例：竞品认证每天硬抓 spec sheet·抓取频率远大于变化频率·纯增成本阻塞 | L1→daily, L2→weekly, exhibition→event_driven |
| `compliance` (P0) | 采集合规：允许抓取/API可用/rate limit/数据保留/管辖权 | 基于域名TLD自动推导 jurisdiction |

## 技能维护

- **发现新信源**（厂商/展会/标准组织/媒体）→ 更新对应行业的 sourcebook JSON，填写 P0 字段（verification/content_type/ttl/compliance），更新 `last_updated`
- **新增行业** → 创建 `references/{industry}_sourcebook.json`，遵循 `sourcebook.schema.json` 校验，更新上方行业表格
- **信源质量评估** → 调整 L1-L4 层级，更新 `verification.status`
- **搜索词失效** → 更新 `query_templates`
- **发现新展会-竞品关联** → 更新 `exhibition_calendar` + `competitors.*.core_expos`
- **Schema 校验** → 每次修改后运行 `validate_sourcebooks.py` 确保结构完整性

## 引用者

- `ipc-daily-report` 自动化任务（`automation-1780585028550`）
- `write-report` 技能（行业配置参数注入）
- `channel-analysis` 技能（竞品对标配置）
- `customer-po-analysis` 技能（供应商来源验证）
- `cross-space-realtime-feedback` 技能（AI 智能体域情报源·🆕 2026-08-26）
- 未来的海事报告、产品研究等跨项目技能

## 扩展新行业

1. 复制 `references/sourcebook.schema.json` 中的模板结构
2. 创建新的 JSON 文件，如 `references/maritime_sourcebook.json`
3. 填充 L1-L4 信源、竞品、展会、搜索白名单
4. 更新本文件上方"支持行业"表格
5. 引用的技能/自动化加载时指定新的 industry 参数
## 盲区与自审
- 本技能的已知盲区：知识型技能，仅提供 IPC、海事、AI 智能体三个行业的信源配置（AI 域 v1.0 初建·待多轮验证），其他行业未覆盖（需按需扩展）；信源清单是静态配置，URL 变更、公司易主/倒闭、层级调整后不会自动更新，可能引导查询到失效入口；只提供"在哪查"的配置，不执行任何查询或抓取。
- 自审方式：竞品查询发现 URL 失效、新竞品/新展会未收录、或 `validate_sourcebooks.py` 校验失败时，检查 sourcebook JSON 是否过时，需更新 P0 字段（verification/ttl）后再复用。

## 🛑 自同步约束（修改本技能后强制执行）
本技能为 Q博士 技能生态资产，修改后须运行 `python scripts/sync_skill_registry.py` 同步注册表/路由/FILE_MANIFEST。
