# memory-management 日志与沉淀参考（渐进披露·2026-08-26 外移）

> 本文件由 memory-management SKILL.md 渐进披露重构外移（2026-08-26·低频审计/沉淀流程·按需加载）
> 触发时加载：记忆访问日志记录/审计 / 提问即升级沉淀

### 🆕 15. 记忆访问日志（Phase 2A.4·2026-07-04）

> 来源：Q博士综合工作规划 Phase 2A.4 — 记忆读取时记录 timestamp + caller，支持审计。

#### 15.1 记录规则

**触发条件**：任何对以下文件的读取操作：
- `<宿主配置根>/MEMORY.md`
- 项目 `.workbuddy/memory/MEMORY.md`
- 项目 `.workbuddy/memory/YYYY-MM-DD.md`
- `../Data-全局数据仓库/.DATA_REGISTRY.md`（全局数据仓库，位于工作区父目录）

**记录内容**：

| 字段 | 示例 | 说明 |
|:--|:--|:--|
| `timestamp` | `2026-07-04T18:30:00` | ISO 8601 时间 |
| `caller` | `task-router / automation:周度复盘` | 调用者（技能名/自动化ID/用户操作） |
| `file` | `<宿主配置根>/MEMORY.md` | 被读取的文件路径 |
| `action` | `read / write / modify` | 操作类型 |
| `purpose` | `Step 0.1 全局铁律加载` | 读取目的（可选·如果能推断） |

#### 15.2 日志格式

**存储路径**：`.workbuddy/memory/access_logs/YYYY-MM-DD.jsonl`

```jsonl
{"timestamp": "2026-07-04T18:30:01", "caller": "task-router", "file": "<宿主配置根>/MEMORY.md", "action": "read", "purpose": "Step 0.1 全局铁律加载"}
{"timestamp": "2026-07-04T18:30:05", "caller": "task-retrospective", "file": "project/.workbuddy/memory/MEMORY.md", "action": "read", "purpose": "Step A0 前置审计"}
{"timestamp": "2026-07-04T18:32:00", "caller": "memory-management", "file": "<宿主配置根>/MEMORY.md", "action": "write", "purpose": "新增铁律AH"}
```

#### 15.3 日志轮转规则

| 规则 | 说明 |
|:--|:--|
| **每日轮转** | 文件名按日期（`YYYY-MM-DD.jsonl`），当日日志追加到当日文件 |
| **保留周期** | 保留 30 天 → 超过 30 天的日志归档到 `access_logs/archive/YYYY-MM/` |
| **归档策略** | 按月打包（`2026-07.jsonl.gz`），保留 12 个月 |
| **查询接口** | `grep "2026-07-04" access_logs/2026-07-04.jsonl` |

#### 15.4 实现方式

> ⚠️ 此项为**规则定义**，不强制代码实现。AI 在执行读取操作时遵守以下约定：

**约定**：
1. **自动化任务**（如周度复盘）：在 prompt 中注明"读取记忆时在回复中标注 [ACCESS] file=xxx, purpose=xxx"
2. **手动任务**：AI 在首次读取记忆后，在回复第一行下方追加访问记录
3. **查询**：`grep "caller:xxx" .workbuddy/memory/access_logs/*.jsonl` 可检索任意调用者的访问历史

**反模式**：
- ❌ 要求 AI 手动写 jsonl 文件（增加不必要的 I/O）
- ❌ 每次读取都记录（仅记录"首次加载"，同一会话内不重复记录）
- ❌ 日志文件膨胀到影响性能（30 天自动归档防止此问题）

#### 15.5 审计用途

| 场景 | 查询 | 用途 |
|:--|:--|:--|
| "为什么又忘了规则X？" | `grep "MEMORY.md" access_logs/$(date +%Y-%m-%d).jsonl` | 确认当前会话是否读取了记忆 |
| "规则X最后一次被谁修改？" | `grep "action.*write" access_logs/*.jsonl \| grep "铁律X"` | 追踪规则修改来源 |
| "本周哪些技能最常读记忆？" | `grep "read" access_logs/2026-07-0*.jsonl \| jq -r '.caller' \| sort \| uniq -c` | 统计记忆使用频率



---

### 🆕 16. 提问即升级沉淀（P1-13 · 2026-07-09 落地）

> **来源**：战略宪章 P1-13 + 本质定位③知识回路升级。每次用户提问是 Q博士 进化的显化机缘，回复完成后须自动提取知识、分级判定、沉淀到对应宪法层或 drq/ 模式库。

#### 16.1 触发

每次回复完成后（写日志前），AI 自动执行 3 步分级沉淀。

#### 16.2 Step 1：扫描本提问蕴含的知识层级

| 扫描维度 | 探测信号 | 判定等级 |
|:--|:--|:--|
| 提问改变核心认知或哲学？ | 涉及「本质」「原点」「定律」「自我」 | **P0 裂变级** 🌟 |
| 提问建立新框架/分类/纠偏？ | 创建分析文档 / 新建分类 | **P1 宪法级** 🏛️ |
| 提问暴露可复用模式或规则？ | 根因分析 / 模式提取 | **P2 规则级** ⚙️ |
| 提问产生可复制的流程？ | 生成步骤/方法/SOP | **P3 方法级** 📋 |
| 提问只是事实查询或确认？ | 状态查询 / 来源确认 | **P4 信息级** 📝 |

#### 16.3 Step 2：分级写入

| 等级 | 写入位置 | 需用户确认 |
|:--|:--|:--|
| P0 | 跨空间本体论 § / 本质定位 | ⚠️ 需确认 |
| P1 | 战略宪章 / 系统架构 | ⚠️ 需确认 |
| P2 | 铁律 / drq/ / governance/ | 可自动 + 回复末尾提示 |
| P3 | 流程日记 M-条目 / 综合规划 | 自动执行 + 回复末尾提示 |
| P4 | 每日日志 AI 压缩段 | 全自动 |

#### 16.4 Step 3：标记日志

在日志 AI 压缩段末尾追加升级标签，如 `提问升级:P0` `提问升级:P2`。

#### 16.5 可复刻模式

每次回复完成 → 3 步自检（扫描→分级→写入）→ 4 标签标记日志。
| **cross-ref 消费方** | 谁消费本技能？ | `grep -rn "memory-management" <宿主配置根>/skills/*/SKILL.md` |

