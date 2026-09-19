# 对外发布技能标准（External Release Standard）v1.0

> **定标日期**：2026-09-15 | **定标依据**：WorkBuddy 官方 skill-creator 规范 + ai-drift-guard-release 实践样本
> **适用**：标注 `distribute_external: yes` 或拟发布公开市场（GitHub / 技能市场）的技能
> **本文件由 skill-review Step 3 引用**（G7 对外发布维）

## 一、为什么需要本标准

**背景**：2026-09-15 B 机实测暴露——打包分发的技能缺参考文件（references 空）+ 缺公开市场要素，导致接收方无法真运行。

**判定**：ai-drift-guard-release 是首个达标样本（含 .git + .github 周一自动化 + README/CHANGELOG/CONTRIBUTING/LICENSE），其余产物未达标。

## 二、发布要素（三大类 · 14 项）

### A. 结构六件（目录级）

| # | 要素 | 必需性 | 说明 |
|:--|:--|:--:|:--|
| A1 | `README.md` | 必须 | 项目说明（是什么/怎么用/安装） |
| A2 | `CHANGELOG.md` | 必须 | 变更日志（版本演进） |
| A3 | `LICENSE` | 必须 | 许可证（MIT 等） |
| A4 | `CONTRIBUTING.md` | 推荐 | 贡献指南 |
| A5 | `.gitignore` | 必须 | Git 忽略规则 |
| A6 | `.github/` | 条件 | 含 CI/自动化时必须（如 ai-drift-guard 的周一自动化） |

### B. frontmatter 四项

| # | 字段 | 值 | 说明 |
|:--|:--|:--|:--|
| B1 | `distribute_external` | `yes` | 对外分发标记（未标记的不按本标准审） |
| B2 | `license` | `MIT` 等 | 与 LICENSE 文件一致 |
| B3 | `description` | 中英双语 | 对外的 description 须双语（受众国际化） |
| B4 | 能力边界声明 | 必须 | description 或正文含「不做什么」（防误用） |

### C. 自闭环四项（真运行）

| # | 项 | 判定 |
|:--|:--|:--|
| C1 | references 非空 | 若 SKILL.md 引用了 references → 必须非空 |
| C2 | scripts 可运行 | 若含 scripts/ → 无本机路径依赖、无缺失依赖 |
| C3 | 无 TODO 遗留 | 正文/文件无「待补/TODO/占位符」 |
| C4 | 无本机信息泄露 | 无本机绝对路径 / 内部术语 / 凭证 |

## 三、与官方 skill-creator 的对应

| skill-creator 规范 | 本标准 |
|:--|:--|
| SKILL.md required + frontmatter | B 类 |
| scripts/ / references/ / assets/ | C1/C2 + A 类 |
| Progressive Disclosure 三级 | SKILL.md <5k 词 · 详细内容外置 references |
| 第三人称 description | B3/B4 |
| agent_created: true | 保留（skill_manage 需要） |
| package_skill.py 验证 | 对齐 C 类自闭环 |

## 四、打包侧要求（sync_portable_build）

| 要求 | 实现 |
|:--|:--|
| references 一起打包 | ✅ rglob 递归（已实现） |
| scripts 一起打包 | ✅ 2026-09-15 补（自闭环要求） |
| role.json 注入 | ✅ business 角色 |
| 自闭环四件校验 | ✅ SKILL.md + references + scripts + role.json |
| **待补**：README/CHANGELOG/CONTRIBUTING/.gitignore 生成 | ⏳ 打包器需补（对外发布时） |
| **待补**：TODO 遗留检测 | ⏳ 打包器需补 |
| **待补**：本机信息泄露检测 | ✅ 已有 NoInternalRefs（部分） |

## 五、审阅清单（skill-review Step 3 用）

```
□ A1 README.md 存在
□ A2 CHANGELOG.md 存在
□ A3 LICENSE 存在
□ A4 CONTRIBUTING.md 存在（推荐）
□ A5 .gitignore 存在
□ A6 .github/ 存在（若含自动化）
□ B1 distribute_external: yes
□ B2 license 字段与 LICENSE 一致
□ B3 description 中英双语
□ B4 能力边界声明存在
□ C1 references 非空（若引用）
□ C2 scripts 可运行（若含）
□ C3 无 TODO 遗留
□ C4 无本机信息泄露
```

## 六、达标判据

- **全部 A（6）+ 全部 B（4）+ 全部 C（4）** → ✅ 对外发布就绪
- A4（CONTRIBUTING）缺失 → 可接受（推荐级）
- C1/C3/C4 任一缺失 → 🛑 **阻断**（真运行/泄露风险）
- 参考达标样本：`products/技能市场/releases/ai-drift-guard-release/`
