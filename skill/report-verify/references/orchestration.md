# 8 阶段编排工作流

> 日常校验只跑 Phase 1-6。正式发版请使用 `@skill:apq-report-release`。

## 编排流程

```
Phase 0: 备份原始 MD 文件（.bak）
    ↓
Phase 1: 24 项自动校验（门禁）← 日常必跑
    · 运行 _report_validator.py
    · 24 项必须全部通过
    · 任何一项不通过 → STOP → 修复 → 重跑 Phase 1
    ↓ 全部通过
Phase 2: 编号重排（如有章节增删）← 日常可选
    · 运行 renumber_report.py
    · 更新正文 §X.Y 交叉引用
    ↓
Phase 3: 锚点重建 ← 日常可选
    · 运行 insert_anchors.py
    ↓
Phase 4: 图表编号校验（如已启用）← 日常可选
    · 运行 _figure_table_numbering.py --check
    ↓
Phase 5: 摘要一致性校验（WARNING 级别）← 日常可选
    · 运行 check_19_summary_sync()
    ↓
Phase 6: 逻辑衔接预检（WARNING 级别，AI 辅助）← 日常可选
    · 运行 check_20_context_continuity()
    ↓ 全部通过
Phase 7: PDF 构建 ← ⚠️ 仅正式发版时执行
    · 由 @skill:apq-report-release 或 @skill:apq-report-build 触发
    ↓
Phase 8: 目视检查清单 ← ⚠️ 仅正式发版时执行
    · 逐页翻看 PDF，确认无跨页空白、表格完整、图片正常
```

## 质量门禁规则

| 阶段 | 日常修改 | 正式发版 |
|------|----------|----------|
| Phase 1 (30项校验) | ✅ 必跑，不通过停止 | ✅ 必跑，不通过停止 |
| Phase 2-6 (可选阶段) | 按需跑 | ✅ 全跑 |
| Phase 7 (PDF构建) | ⚠️ 跳过 | ✅ 跑 |
| Phase 8 (目视检查) | ⚠️ 跳过 | ✅ 跑 |

## 执行命令模板

```bash
# ========== 日常修改：只跑校验，不生成 PDF ==========
cd "D:\Workbuddy\海事工控机研究报告"
cp "报告文件.md" "报告文件.md.bak"

# Phase 1: 24 项校验（日常必跑）
python _report_validator.py --md "报告文件.md"

# Phase 2-6: 按需执行
python renumber_report.py "报告文件.md"   # 仅章节增删后
python insert_anchors.py "报告文件.md"    # 仅锚点变动后
python _figure_table_numbering.py "报告文件.md" --check

# ========== 需要 PDF 时，单独执行 ==========
# @skill:apq-report-build（推荐）或 @skill:apq-report-release（正式发版）
```
