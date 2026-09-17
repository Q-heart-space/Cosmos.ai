# Changelog

本文件记录 **Cosmos.ai 公开库结构**的变更。各技能的版本历史见 `skill/<skill-name>/CHANGELOG.md`。

## 2026-09-17（第二次提交）— ai-drift-guard v1.4：平台中立化重构 + 陈旧引用修复

驱动这次重构的是一次**真实的跨平台移植**（把本协议接入一个基于 Cordis 的宿主）。移植中暴露的问题全部在此修正，逐条见 `skill/ai-drift-guard/CHANGELOG.md`。

- **去平台绑定**：`SKILL.md` 删除 WorkBuddy 专有的安装路径与导入流程；协议本体不再含任何平台的目录、钩子名或 SDK。平台差异移入新增的 `references/adapters.md`
- **信号按可执行性分层**：Tier A（S5、S4，可由宿主真拦截）与 Tier B（其余，仅提示词）。明确禁止声称 Tier B "已被保证"
- **新增 Tier A 规范契约**：决策语义 / 会话扫描台账 / 判定顺序 / S5 规范性算法 / 适配器接口 / 记录格式。此前无规范，各宿主只能各自猜
- **修复 S5 盲区**：注释判定前中和 `://`。此前任何含 `https://` 的行被整行跳过，其上的泄漏占位符会漏检。Python 校验器同步修到 v1.1
- **修复 S4 缺陷**：转义正则（`cordis\.patch\.yml`）此前无法解除封锁，而随手写的字面量可以。改为探测串先去反斜杠
- **移除 S11**：它引用未绑定的 `your project's sync-validation routine`，对公开库读者是死文本
- **效果声明改为可核对项**：删除不可证伪的"过度工程化方案：趋近零"
- 新增 `references/drift-guard-core.mjs`（零依赖参考实现，可脱离 AI 平台作 pre-commit / CI 用）与 `references/selftest.mjs`（13 项断言）
- 补齐 `skill/ai-drift-guard/LICENSE`（本库自己的贡献规则要求技能目录含许可证，此前缺失）
- **修复死链**：`skill/ai-drift-guard/CONTRIBUTING.md` 原指向已不存在的独立仓库 `Q-heart-space/ai-drift-guard`
- **修复陈旧引用**：根 `CONTRIBUTING.md` 仍在说已删除的 `resource/` 目录
- **修复 CHANGELOG 缺口**：技能 CHANGELOG 停在 1.2.0-ext，缺 v1.3 条目，并引用了未发布文件 `CHANGELOG_vs_internal.md`
- **修复陈旧发行包**：`ai-drift-guard.zip` 内的 SKILL.md 为 5.6 KB，而仓库中是 9.6 KB —— 按本库安装说明下载 zip 的人拿到的是旧协议。已重新生成
- 根 `CONTRIBUTING.md` 增补：**"凡声明已生效的行为，必须附任何人可复现的自检命令"**

## 2026-09-17 — 域集收敛五域 + 修复死链

- 顶层收敛为**五域**：`decision/` · `skill/` · `expert/` · `methodology/` · `whitepaper/`
- 删除 `resource/`（无宪法依据）· `case/` 归入 `methodology/case/`
- 新增 `decision/` **决策资产**域（五元组 + 五项不变量 + 行业维度：`common/` 共性 + `<行业>/` 专属）
- 根 README 改为中英文双名映射导航
- 修复 `skill/ai-drift-guard/SKILL.md` 安装段**死链**：原指向不存在的 `[Releases]` → 改指本目录 `ai-drift-guard.zip`

## 2026-09-16 — 结构重组

- 新增按**对外能力**分类的顶层目录：`skill/` · `expert/` · `methodology/` · `whitepaper/` · `case/` · `resource/`
- 技能统一归入 `skill/<技能名>/`（首个技能：`skill/ai-drift-guard/`）
- 根目录改为**库索引**（README）；移除散落于根目录的技能文件
- 明确**回传通道**：走 Issues / Pull Requests / Discussions，不设回传目录
