# Changelog

---

All notable changes to AI-Drift-Guard will be documented in this file.

---

## [1.4.0] — 2026-09-17

平台中立化重构。驱动它的是**一次真实的跨平台移植**：把本协议接入一个基于 Cordis 的宿主
（DSH）时的实测结果。移植过程中暴露的问题，全部在此修正。

### Fixed
- **S5 的 URL 盲区**：v1.3 及以前用 `//` 直接判定 JS 注释，导致**任何含 `https://` 的行被整行跳过**——
  该行上的泄漏占位符会漏检。现在注释判定前先中和 `://`。
  `references/template_validator.py` 同步修正到 v1.1。
- **S4 无法被转义正则解除**：v1.3 的实现用字面量 `indexOf` 判断"是否做过关联扫描"，
  于是规范写法的 `cordis\.patch\.yml` 反而**不能**解除封锁，而随手写的 `cordis.patch.yml` 可以。
  现在探测串先去反斜杠。
- **CONTRIBUTING 死链**：指向已不存在的独立仓库 `Q-heart-space/ai-drift-guard`，改为 `Cosmos.ai`。
- **CHANGELOG 缺失 v1.3 条目**（SKILL.md 迭代记录里已有，此处补齐）。
- 移除对未发布文件 `CHANGELOG_vs_internal.md` 的引用。

### Changed
- **信号按可执行性分层**：Tier A（S5、S4，可被宿主强制）与 Tier B（其余，仅提示词）。
  明确写出"不要声称 Tier B 被保证"。
- **新增 Tier A 规范契约**：决策语义、会话扫描台账、判定顺序、S5 规范性算法、
  适配器接口、日志记录格式。此前没有任何规范，每个宿主只能各自猜（本次移植就是如此）。
- **去掉平台绑定**：删除 WorkBuddy 专有的安装路径与"专家 → 技能 → 导入"流程；
  改为按宿主能力分三层的通用说明。
- **效果声明改为可核对项**：删除不可证伪的"过度工程化方案：趋近零"，
  换成"造一个应交由 A.4 判定的文件，看是否 deny 且未落盘"这类可执行的核对。
- `triggers` 由空补全。

### Added
- `references/drift-guard-core.mjs` —— Tier A 参考实现。零依赖，
  可作 CLI 独立运行（`node drift-guard-core.mjs check <file.html>`），**不需要任何 AI 平台**。
- `references/adapters.md` —— 宿主适配器契约 + 实例（DSH / pre-commit / 其他宿主检查清单）+ 反例。
- `references/selftest.mjs` —— 13 项断言，覆盖上述修复与已知盲区。
- `LICENSE` —— 本技能目录此前缺少许可证，与根库要求不符。

### Removed
- **S11**：它引用 `your project's sync-validation routine`，是一个未绑定的占位符，
  对公开库的任何读者都是死文本。等价能力应实现为宿主侧的 `globalRuleMatchers` 条目。

---

## [1.3.0-ext] — 2026-07-12

（补齐：此前只存在于 SKILL.md 的迭代记录表中）

### Added
- **S9 修复**：硬截断零输出 + 新增 **S9-INPUT**（输入层停信号，AI 还没开始生成时即拦截）。
- **Limitations 节**：明确能力边界——技能运行在提示指令层，不干预模型推理层、客户端层、系统进程层。
- **Release Governance 节**：batched release + 1h 冷却门禁。
- **Export Audit**：5 项出口审计脚本化 + 元数据自洽审计。
- **S4/S6/S10 增强**（v1.2 引入）：S4 补关联扫描、S6 补同类问题清扫、S10 补最小切片。

### Changed
- 描述修正：删除不准确承诺。
- 自我审视：用技能审视自身（7/7 信号检查）。

---

## [1.2.0-ext] — 2026-07-12

### Added
- **S11 signal**: fixed/patched a system file but no closure/sync-validation check → block.
  (Response generalized for portability — references your project's asset-repair / sync-validation routine instead of a space-specific tool.) ⚠️ **已于 v1.4.0 移除**：该"泛化"留下了一个未绑定占位符。
- **MIT LICENSE** for public / multi-user distribution.
- Portable build: removed space-specific references (constitution alignment, internal project cross-references, internal PTN codes) so the skill is reusable across spaces and by multiple people.
- **S4 behavior self-containment**: "association scan" response expanded to a self-contained 7-step instruction.

### Changed
- Version marked as `-ext` to distinguish from the internal source-of-truth version.
- SKILL.md frontmatter: `version: 1.2.0-ext`; added `license: MIT`; removed space-specific routing fields (`layer`/`task_type`); kept `triggers` for portability.
- README: added "About This Project" section with Q博士 narrative + 菩提心 statement.
- Iteration history rewritten without internal PTN references.
- README: fixed broken GitHub link (`Q博士` → `Q-heart-space`); added License badge; added LICENSE to file tree.

### Note
- This release is the **portable / Distribute** build (`v1.2.0-ext`). The full-context internal version
  remains the source of truth inside the Q博士 workspace and is not published.

---

## [1.1.0] — 2026-07-01

### Added
- Bilingual description (EN/CN) in SKILL.md frontmatter
- `version` field in metadata for tracking
- CHANGELOG.md for release history
- Engineering vs. Gradualism decision table (6-row matrix)

### Changed
- SKILL.md: Full bilingual format — every section has EN/CN side by side
- Signal table: Dual-language trigger patterns and responses
- Description: Expanded from Chinese-only to EN/CN bilingual

### Fixed
- S10 signal refined with 6 cross-project over-engineering case references
- S9 upgraded from ⚠️ to ⛔ (blocking level)
- Cleaned up duplicate installed skill directory (ai-drift-guard → drift-guard)

---

## [1.0.0] — 2026-06-30

### Initial Release
- 10-drift-signal self-check protocol (S1–S10)
- `template_validator.py` reference implementation for S5
- Chinese-only SKILL.md description
- WorkBuddy marketplace packaging

> v1.0 的 "WorkBuddy marketplace packaging" 标记，是 v1.4.0 去平台绑定的对象：
> 协议本身与任何市场无关。
