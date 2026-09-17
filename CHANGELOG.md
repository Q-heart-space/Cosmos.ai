# Changelog

本文件记录 **Cosmos.ai 公开库结构**的变更。各技能的版本历史见 `skill/<skill-name>/CHANGELOG.md`。

## 2026-09-17 — 域集收敛五域 + 修复死链

- 顶层收敛为**五域**：`decision/` · `skill/` · `expert/` · `methodology/` · `whitepaper/`
- 删除 `resource/`（无宪法依据）· `case/` 归入 `methodology/case/`
- 新增 `decision/` **决策资产**域（五元组 + 五项不变量 + 行业维度：`common/` 共性 + `<行业>/` 专属）
- 根 README 改为**中英文双名映射**导航
- 修复 `skill/ai-drift-guard/SKILL.md` 安装段**死链**：原指向不存在的 `[Releases]` → 改指本目录 `ai-drift-guard.zip`

## 2026-09-16 — 结构重组

- 新增按**对外能力**分类的顶层目录：`skill/` · `expert/` · `methodology/` · `whitepaper/` · `case/` · `resource/`
- 技能统一归入 `skill/<技能名>/`（首个技能：`skill/ai-drift-guard/`）
- 根目录改为**库索引**（README）；移除散落于根目录的技能文件
- 明确**回传通道**：走 Issues / Pull Requests / Discussions，不设回传目录
