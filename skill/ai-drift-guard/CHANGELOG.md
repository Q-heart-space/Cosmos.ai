# Changelog

---

All notable changes to AI-Drift-Guard will be documented in this file.

---

## [1.2.0-ext] — 2026-07-12

### Added
- **S11 signal**: fixed/patched a system file but no closure/sync-validation check → block. (Response generalized for portability — references your project's asset-repair / sync-validation routine instead of a space-specific tool.)
- **MIT LICENSE** for public / multi-user distribution.
- Portable build: removed space-specific references (constitution alignment, internal project cross-references, internal PTN codes) so the skill is reusable across spaces and by multiple people.
- **S4 behavior self-containment**: "association scan" response expanded to a self-contained 7-step instruction (no longer depends on Q博士-specific "关联扫描" context).

### Changed
- Version marked as `-ext` to distinguish from the internal source-of-truth version (prevents 铁律AO version collision).
- SKILL.md frontmatter: `version: 1.2.0-ext`; added `license: MIT`; removed space-specific routing fields (`layer`/`task_type`); kept `triggers` for portability.
- README: added "About This Project" section with Q博士 narrative + 菩提心 statement.
- Iteration history rewritten without internal PTN references.
- README: fixed broken GitHub link (`Q博士` → `Q-heart-space`); added License badge; added LICENSE to file tree.

### Note
- This release is the **portable / Distribute** build (`v1.2.0-ext`). The full-context internal version (`v1.2.0` with constitution-alignment and project cross-references) remains the source of truth inside the Q博士 workspace and is not published. See `CHANGELOG_vs_internal.md` for version comparison.

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
