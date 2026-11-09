#!/usr/bin/env python3
"""全系报告通用MD校验脚本。
用法: python _report_validator.py --md 报告.md [--type strategy|maritime|data|client]

v2.0: 核心校验逻辑已提取至 Shared-脚本/verify_core.py（治理规则X 共享逻辑提取试点）
"""
import sys, re, os

# --- 共享核心导入（治理规则X）---
# 🆕 2026-11-09：原为仓外相对路径 `../Data-全局数据仓库/Shared-脚本`（且含宿主硬路径兜底）
#   ⇒ 改为**同技能目录** scripts/（verify_core.py 已纳入本体·可随技能分发）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
from verify_core import (
    ReportValidator,
    find_brand_colors,
    validate_table_columns,
)


def check_md(md_path, report_type='strategy'):
    """主校验入口 —— 使用 ReportValidator 基类。"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')

    v = ReportValidator(report_type=report_type)

    # 1. 版本号三处一致性（共享核内方法）
    v.check_version_consistency(content, os.path.basename(md_path))

    # 2. 版本修订记录连续性
    ver_meta = re.findall(r'\*\*版本\*\*[：:]\s*v?([\d.]+)', content)
    versions = [m.group(1) for m in re.finditer(r'\*\*v(\d+\.\d+)\*\*\s*\|', content)]
    if versions and ver_meta and versions[0] != ver_meta[0]:
        v.warn('ERROR', 2,
            f'版本表第一行({versions[0]}) ≠ 元数据版本({ver_meta[0]})')

    # 3. H2/H3标题不重复（共享核内方法）
    v.check_title_duplication(content)

    # 4. 表格结构完整性（共享核函数）
    table_issues = validate_table_columns(lines)
    for issue in table_issues:
        v.warn(issue['level'], issue['id'], issue['msg'], issue.get('line'))

    # 5. 交叉引用有效性
    refs = re.findall(r'第(\d+)章|第(\d+\.\d+)节', content)
    chapter_pattern = re.findall(r'^## 第(\d+)章', content, re.MULTILINE)
    max_chapter = 0
    if chapter_pattern:
        max_chapter = max(int(c) for c in chapter_pattern)
    for ref_num_str, _ in refs:
        try:
            ref_num = int(ref_num_str)
            if ref_num > max_chapter and max_chapter > 0:
                v.warn('WARNING', 5,
                    f'引用不存在的第{ref_num}章 (最大章节为第{max_chapter}章)')
        except:
            pass

    # 6. 品牌色检查（共享核内方法）
    html_path = md_path.replace('.md', '.html')
    v.check_brand_colors_html(html_path)

    # 7. 表格对齐行格式（共享核内方法）
    v.check_table_alignment(lines)

    return v.report(os.path.basename(md_path))


if __name__ == '__main__':
    md_path = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == '--md' else None
    report_type = 'strategy'
    if len(sys.argv) > 4 and sys.argv[3] == '--type':
        report_type = sys.argv[4]

    if md_path:
        check_md(md_path, report_type)
    else:
        print("用法: python _report_validator.py --md 报告.md [--type strategy]")
