#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告校验核心 — Shared Core 试点模块
========================================
从 report-verify/_report_validator.py 提取的通用校验函数，
可被任意报告构建/校验技能引用。

提取依据（治理规则X）：两个组件共享检测逻辑 → 必须提取到独立文件。

用法:
    import sys
    sys.path.insert(0, '<本技能>/scripts')  # 同目录
    from verify_core import ReportValidator, find_brand_colors, validate_table_columns

引用者:
    - report-verify/_report_validator.py（首批试点）
    - build-dashboard/dashboard/__init__.py（未来接入）
"""

import re
import json
import os
from pathlib import Path
from typing import Optional


# ============================================================
# 品牌色加载（单一事实来源）
# ============================================================

# 🆕 2026-11-09 组织参数化（原为宿主硬名 + 已迁走的技能级文件）：
#   ① 组织级唯一品牌资产 `business:<域>/<组织>/brand/brand_colors.json`
#   ② 本体中性模板 `references/brand_colors.template.json`（兜底·无组织品牌色）
#   🛑 不再写死任何宿主目录（`.workbuddy` / `.dsh`），运行期由环境/声明解析。
def _org_brand_paths():
    """按三级解析求组织级品牌色候选：env > <config_dir>/qdr_env.json。"""
    import os as _os, json as _json
    here = _os.path.dirname(_os.path.abspath(__file__))
    decl = {}
    cur = here
    for _ in range(5):
        cur = _os.path.dirname(cur)
        if not cur or cur == _os.path.dirname(cur):
            break
        cand = _os.path.join(cur, "qdr_env.json")
        if _os.path.isfile(cand):
            try:
                with open(cand, encoding="utf-8-sig") as fh:
                    decl = _json.load(fh) or {}
            except Exception:
                decl = {}
            break
    root = (_os.environ.get("QDR_BUSINESS_ROOT") or "").strip() or str(decl.get("QDR_BUSINESS_ROOT") or "").strip()
    dom = (_os.environ.get("QDR_BUSINESS_DOMAIN") or "").strip() or str(decl.get("QDR_BUSINESS_DOMAIN") or "ipc").strip()
    cli = (_os.environ.get("QDR_BUSINESS_CLIENT") or "").strip() or str(decl.get("QDR_BUSINESS_CLIENT") or "").strip()
    out = []
    if root and cli:
        out.append(Path(root) / dom / cli / "brand" / "brand_colors.json")            # 组织级唯一
        out.append(Path(root) / dom / cli / "skills" / "report-verify" / "brand_colors.json")  # 旧形态兼容
        out.append(Path(root) / dom / cli / "report-verify" / "brand_colors.json")             # 更旧兼容
    return out


_BRAND_COLORS_PATHS = _org_brand_paths() + [
    Path(__file__).resolve().parent.parent / "references" / "brand_colors.template.json",  # 中性兜底
]

_BRAND_COLORS_CACHE: Optional[dict] = None


def find_brand_colors() -> dict:
    """加载品牌色值：**组织级配置优先**，本体中性模板兜底。结果缓存。

    🛑 无任何配置 ⇒ 返回 `{}`（调用方按中性默认处理，**不猜任何组织品牌色**）。
    """
    global _BRAND_COLORS_CACHE
    if _BRAND_COLORS_CACHE is not None:
        return _BRAND_COLORS_CACHE

    for p in _BRAND_COLORS_PATHS:
        if p.exists():
            with open(p, 'r', encoding='utf-8') as f:
                data = json.load(f)
                _BRAND_COLORS_CACHE = data.get('colors', data)
                return _BRAND_COLORS_CACHE

    _BRAND_COLORS_CACHE = {}
    return _BRAND_COLORS_CACHE


# ============================================================
# 表格列数对齐校验（全局通用）
# ============================================================

def validate_table_columns(lines: list[str]) -> list[dict]:
    """校验 Markdown 表格的列数对齐。
    
    返回问题列表，每项含: level, id, msg, line
    """
    issues = []
    in_table = False
    header_cols = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith('|') or '|' not in stripped[1:]:
            if in_table:
                in_table = False
                header_cols = 0
            continue

        cells = [c.strip() for c in stripped.split('|')[1:-1]]

        # 分隔行: |---|---|
        if all(re.match(r'^[\s:|-]+$', c) for c in cells):
            if header_cols != len(cells):
                issues.append({
                    'level': 'ERROR',
                    'id': 4,
                    'msg': f'表格列数不匹配: 表头{header_cols}列, 分隔行{len(cells)}列',
                    'line': i + 1,
                })
            continue

        if not in_table:
            in_table = True
            header_cols = len(cells)

    return issues


# ============================================================
# ReportValidator 类（可扩展）
# ============================================================

class ReportValidator:
    """报告校验基类。封装 issues 收集和输出格式化。
    
    子类/调用方用法:
        validator = ReportValidator(report_type='strategy')
        validator.check_version_consistency(content, basename)
        validator.check_table_alignment(lines)
        ok = validator.report(basename)
    """

    def __init__(self, report_type: str = 'strategy'):
        self.report_type = report_type
        self.issues: list[dict] = []

    def warn(self, level: str, check_id: int, msg: str, line: Optional[int] = None):
        """记录一条校验问题。"""
        entry = {'level': level, 'id': check_id, 'msg': msg}
        if line is not None:
            entry['line'] = line
        self.issues.append(entry)

    # --- 通用校验方法 ---

    def check_version_consistency(self, content: str, basename: str):
        """校验版本号三处一致性（元数据块/文件名/版本记录表）。"""
        ver_meta = re.findall(r'\*\*版本\*\*[：:]\s*v?([\d.]+)', content)
        ver_fname = re.findall(r'v(\d+\.\d+)', basename)
        ver_table = re.findall(r'\|\s*\*\*v(\d+\.\d+)\*\*\s*\|', content)

        if len(set(ver_meta)) > 1:
            self.warn('ERROR', 1, f'元数据块版本号不唯一: {ver_meta}')
        if ver_meta and ver_fname and ver_meta[0] != ver_fname[0]:
            self.warn('ERROR', 1,
                f'元数据版本({ver_meta[0]}) ≠ 文件名版本({ver_fname[0]})')

    def check_title_duplication(self, content: str):
        """校验 H2/H3 标题不重复。"""
        h2s = re.findall(r'^## (.+)', content, re.MULTILINE)
        h3s = re.findall(r'^### (.+)', content, re.MULTILINE)

        seen_h2, seen_h3 = {}, {}
        for h in h2s:
            hk = h.strip()[:30]
            seen_h2[hk] = seen_h2.get(hk, 0) + 1
        for h in h3s:
            hk = h.strip()[:30]
            seen_h3[hk] = seen_h3.get(hk, 0) + 1

        for k, v in seen_h2.items():
            if v > 1:
                self.warn('ERROR', 3, f'H2标题重复({v}次): {k}')
        for k, v in seen_h3.items():
            if v > 1:
                self.warn('WARNING', 3, f'H3标题重复({v}次): {k}')

    def check_table_alignment(self, lines: list[str]):
        """校验表格对齐行格式（非法字符、太短）。"""
        for i, line in enumerate(lines):
            if not re.match(r'^\|[\s:|-]+\|$', line.strip()):
                continue
            cells = [c.strip() for c in line.strip().split('|')[1:-1]]
            for c in cells:
                if c and len(c.replace(':', '').replace('-', '').strip()) > 0:
                    self.warn('WARNING', 7,
                        f'表格分隔行含非法字符: "{c}"', i + 1)
                if c.startswith(':') and c.endswith(':') and len(c) < 3:
                    self.warn('WARNING', 7,
                        f'对齐标记太短(可能渲染异常): "{c}"', i + 1)

    def check_brand_colors_html(self, html_path: str, forbidden_colors: list[str] = None):
        """校验 HTML 中是否含硬编码的非品牌色。"""
        if forbidden_colors is None:
            forbidden_colors = ['#1E40AF', '#2563EB', '#3B82F6']

        if not os.path.exists(html_path):
            return

        with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()

        for color in forbidden_colors:
            if color in html:
                self.warn('ERROR', 6,
                    f'HTML含硬编码非品牌色{color}，应使用品牌主色（角色 primary）')

    # --- 输出 ---

    def report(self, basename: str) -> bool:
        """打印校验结果，返回是否通过（无 ERROR）。"""
        errors = [i for i in self.issues if i['level'] == 'ERROR']
        warnings = [i for i in self.issues if i['level'] == 'WARNING']

        print(f"\n{'='*60}")
        print(f"报告校验: {basename}")
        print(f"报告类型: {self.report_type}")
        print(f"ERROR: {len(errors)} | WARNING: {len(warnings)}")
        print(f"{'='*60}")

        for i in errors + warnings:
            tag = '❌' if i['level'] == 'ERROR' else '⚠️'
            line_info = f" (行{i['line']})" if i.get('line') else ''
            print(f"  {tag} #{i['id']}: {i['msg']}{line_info}")

        if errors:
            print(f"\n🛑 {len(errors)}个ERROR，禁止发布！")
            return False
        elif warnings:
            print(f"\n✅ 通过（{len(warnings)}个WARNING可忽略）")
        else:
            print(f"\n✅ 全部通过")
        return True
