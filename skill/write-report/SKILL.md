---
name: write-report
description: |
  研究报告撰写方法论。覆盖结构设计→研究→大纲→分章撰写→数据核查→终稿全流程。
  触发词：写报告、撰写报告、研究、调研、大纲设计、调整结构、优化章节、重组内容、数据核查。
  ⚠️ 内容定稿后 → @apq-content-coherence（内容校对·13项）→ @apq-format-verify（格式校验·30项）
space_scope: universal
reuse_depth: org-parameterized
scope_axis: business
layer: 叶·写作
trust_level: notification
version: 1.0.0-ext
distribute_external: yes
depends: apq-content-coherence, apq-format-verify, task-router,
  report-iteration-steward, references/check-dimensions.md
triggers:
  - 写报告
  - 撰写报告
  - 研究
  - 调研
  - 大纲设计
  - 调整结构
  - 优化章节
  - 重组内容
  - 数据核查
circuit: ⑦自审
deprecated: false
updated_at: 2026-08-10
---


# 研究报告撰写方法论

> 通用框架。领域示例见 `references/examples-maritime.md`

## 使用场景

| 你说的话 | 模式 | 流程 |
|:--|:--|:--|
| "调整结构"、"重组章节" | **结构调整** | Phase 0 → coherence → verify |
| "快速研究"、"写一章" | **快速** | P1→P2→P3逐章(跳过审稿)→P4 |
| "完整研究"、"深度报告" | **完整** | P0(如需)→P1→P2→P3(含L1/L2)→P4 |
| "子报告"、"专项报告" | **子报告** | 模板A/B引用母报告→独立章模式 |

### 子报告规则
- 前置章用模板引用母报告，禁止全文压缩（~2,500积分黑洞）
- 独立章照常走完整流程

## 结构调整（Phase 0）

| 步骤 | 内容 |
|:--|:--|
| 0.1 | 确定主线逻辑链 → 每节点对应一章 |
| 0.2 | 旧→新映射表：逐节列出，零遗漏零重复 |
| 🆕 0.3 | **新增内容放置评估**（V5.3 固化）：按三段式分类（分析/洞察/行动）确定新内容归属位置，**禁止默认追加到章节末尾**。验证放置后上下游逻辑链完整 |
| 0.4 | 新增内容归属：合并已有 or 新建。新建时必须同时确定准确插入位置 |
| 0.5 | 映射验证：全量逐节比对 |

结构调整后必须：coherence → verify → deliver

## 研究流程

```
P1: 初始化 → { taskId, chapters, sourcePool }
P2: 规划大纲 → P3: 逐章循环 → P4: 组装

P3 逐章循环（每章独立）:
  3.1 调研 → 读上下文 → 搜索 → 草稿
  3.2 L1快审（来源≥5？事实有支撑？覆盖完整？）
  3.3 不通过 → L2深度审 → Patch修订 → 回3.2
  硬上限: 2轮，第2轮强制PASS，问题列"遗留改进"
```

## 五维校核

> 撰写阶段自检提示，不替代 coherence。详见 `references/check-dimensions.md`

| 维度 | 时机 |
|:--|:--|
| 前后一致性 | 每章完成时 |
| 趋势逻辑 | 全章完成后 |
| 结论可追溯 | L2深度审 |
| 竞品完整性 | P2大纲规划时 |
| 盲区检测 | P2+P4 |

## 核心规则

1. **参数卡文件化**：禁止 prompt 粘贴参数卡，Agent 读 `research_context.json`
2. **Patch修订模式**：修订员只输出 Patch（位置+原文+改为+原因）
3. **单次直出审稿**：审稿员一次读完→一次输出 PASS 或 REVISE
4. **来源分级**：A=官网/年报 | B=行业报告 | C=媒体 | D=推测

## 禁止行为

| ❌ | ✅ |
|:--|:--|
| prompt粘贴参数卡 | Agent 读文件 |
| 修订员输出完整草稿 | 只输出 Patch 块 |
| 审稿员多轮循环 | 单次直出 PASS/REVISE |
| 跳过公开数据验证 | P1前强制执行 |
| 全部写完再校核 | 逐章校核 |

## 资源索引

| 文件 | 用途 |
|:--|:--|
| `references/examples-maritime.md` | 海事工控机领域示例 |
| `references/domain-adaptation.md` | 新领域适配流程 |
| `references/check-dimensions.md` | 五维校核详细说明 |

---

## 完成后下游建议

本技能执行完成后，按 **[task-router]** 当前任务类型为 **报告撰写**，建议下一步：**[@report-iteration-steward]**（若已有具体数据）或 **[@apq-report-iteration-steward]**（渠道管理项目）。是否继续？
## 🛑 自同步约束（修改本技能后强制执行）
本技能为 Q博士 技能生态资产，修改后须运行 `python scripts/sync_skill_registry.py` 同步注册表/路由/FILE_MANIFEST。
