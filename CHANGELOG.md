# Changelog

本文件记录 **Cosmos.ai 公开库结构**的变更。各技能的版本历史见 `skill/<skill-name>/CHANGELOG.md`。

## 2026-09-16 — 结构重组

- 新增按**对外能力**分类的顶层目录：`skill/` · `expert/` · `methodology/` · `whitepaper/` · `case/` · `resource/`
- 技能统一归入 `skill/<技能名>/`（首个技能：`skill/ai-drift-guard/`）
- 根目录改为**库索引**（README）；移除散落于根目录的技能文件
- 明确**回传通道**：走 Issues / Pull Requests / Discussions，不设回传目录
