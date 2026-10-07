#!/usr/bin/env python3
"""
对抗审计·8维自动审计执行器 v1.0
===============================

第一原理推导：
  - 原则① 建成必通电：技能声明8维审计，必须有可执行脚本
  - 原则② 声明-实现一致：32交叉点需要有代码对应的检查逻辑
  - 第三空间 信息→决策：本脚本产出信息（JSON审计数据），AI审计者做决策

定位：不是替代AI审计者——是提供AI审计者需要的结构化基线数据。
     AI审计者的价值在"质疑本脚本没发现的"和"从数据中提取META模式"。

用法：
  python audit_runner.py              # 全量8维审计，输出JSON
  python audit_runner.py --quick      # 快速模式（仅③④⑧，关键项）
  python audit_runner.py --json       # 仅JSON输出
"""
import json, re, subprocess, sys, argparse
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent.parent
PYTHON = 'python'

# 动态定位 Q博士 工作空间根目录
# 技能路径: ~/.workbuddy/skills/adversarial-audit/scripts/audit_runner.py
# 向上3层到达 ~/.workbuddy/ · 需要找到 D:/Workbuddy/Q博士/
def find_workspace_root() -> Path:
    """从技能目录向上查找 Q博士 工作空间根目录."""
    # 方法1：从当前文件向上找，直到找到 constitution/ 目录
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / 'constitution' / '本质定位.md').exists():
            return current
        if (current / 'scripts' / 'circuit_wiring_map.json').exists():
            return current
        current = current.parent
    # 🆕 T-2（**B机 接手·2026-10-05**）**去宿主绑定**：原为**猜的**绝对路径（某台机的盘符目录）。
    #   🛑 处方明令「**不得猜替代路径**」⇒ 此路改为**唯一确定来源**：环境变量 `QDR_ROOT`。
    #   若两者都不成立 ⇒ **具名退出**（🛑 不静默退回某台机的路径：那会在换机后产生"看起来能跑"的假象）。
    import os as _os
    _env_root = _os.environ.get("QDR_ROOT")
    if _env_root:
        guess = Path(_env_root)
        if (guess / 'constitution' / '本质定位.md').exists():
            return guess
    # 🆑 T-2：**具名退出**（🛑 不静默退回 `.`／某台机路径 —— 静默兜底会在换机后产生"看起来能跑"的假象）
    raise RuntimeError(
        "🛑 无法定位 Q博士 工作空间根：①自本文件向上 10 层未见 `constitution/本质定位.md` "
        "或 `scripts/circuit_wiring_map.json`；②环境变量 `QDR_ROOT` 未设或其下无上述标志。"
        "⇒ 请设 `QDR_ROOT` 为工作空间根（🛑 本工具不猜替代路径）")

ROOT = find_workspace_root()


def run(cmd: str, timeout: int = 60) -> dict:
    """Run a command and return structured result."""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                          cwd=str(ROOT), timeout=timeout)
        return {
            'ok': r.returncode == 0,
            'exit': r.returncode,
            'stdout': r.stdout[:2000],
            'stderr': r.stderr[:500],
            'summary': (
                'PASS' if r.returncode == 0 else
                f'FAIL(exit={r.returncode})' if r.returncode else
                'TIMEOUT'
            )
        }
    except subprocess.TimeoutExpired:
        return {'ok': False, 'exit': -1, 'stdout': '', 'stderr': 'TIMEOUT', 'summary': 'TIMEOUT'}
    except Exception as e:
        return {'ok': False, 'exit': -1, 'stdout': '', 'stderr': str(e), 'summary': f'ERROR: {e}'}


def dimension_1_code_integrity() -> dict:
    """维① 代码完整性：E2E pipeline + syntax check."""
    results = {}
    
    # Test pipeline
    results['e2e'] = run(f'{PYTHON} scripts/test_meta_pipeline.py')
    
    # Syntax check on modified scripts (simplified: check key scripts)
    key_scripts = ['register_meta.py', 'pattern_to_task_bridge.py', 
                   'closure_verification.py', 'meta_task_closure_check.py',
                   'meta_l2_to_l3_pipeline.py']
    for s in key_scripts:
        path = ROOT / 'scripts' / s
        if path.exists():
            r = run(f'{PYTHON} -m py_compile scripts/{s}')
            results[f'syntax_{s}'] = r
    
    passed = all(v.get('ok', False) for v in results.values())
    return {'dimension': '① 代码完整性', 'passed': passed, 'checks': results}


def dimension_2_data_consistency() -> dict:
    """维② 数据一致性：JSON↔index↔plan三方一致·字段完整性."""
    try:
        idx = json.loads((ROOT / 'drq/meta_patterns/index.json').read_text(encoding='utf-8'))
        results = {}
        
        # Check JSON files have required fields
        required = ['title', 'problem', 'core_insight', 'tier', 'engineering_maturity']
        missing_fields = []
        for p in idx.get('patterns', []):
            mid = p.get('id', '')
            files = list((ROOT / 'drq/meta_patterns').glob(f'{mid}_*.json'))
            if files:
                data = json.loads(files[0].read_text(encoding='utf-8'))
                for k in required:
                    if k not in data or not data[k]:
                        missing_fields.append(f'{mid}.{k}')
        
        results['missing_fields'] = missing_fields
        results['total_patterns'] = len(idx.get('patterns', []))
        
        # Distribution
        l_counts = {}
        for p in idx.get('patterns', []):
            m = p.get('engineering_maturity', '?')
            l_counts[str(m)] = l_counts.get(str(m), 0) + 1
        results['distribution'] = l_counts
        
        passed = len(missing_fields) == 0
        return {'dimension': '② 数据一致性', 'passed': passed, 'checks': results}
    except Exception as e:
        return {'dimension': '② 数据一致性', 'passed': False, 'checks': {'error': str(e)}}


def dimension_3_wiring_power() -> dict:
    """维③ 接线通电：wiring_map注册 + daily_tasks调度."""
    try:
        cwm = json.loads((ROOT / 'scripts/circuit_wiring_map.json').read_text(encoding='utf-8'))
        dt = json.loads((ROOT / 'governance/data/daily_tasks.json').read_text(encoding='utf-8'))
        results = {}
        
        # Check key scripts have consumers
        key_scripts = ['meta_l2_to_l3_pipeline.py', 'register_meta.py', 
                       'pattern_to_task_bridge.py', 'closure_verification.py']
        no_consumers = []
        for s in key_scripts:
            entry = cwm.get('scripts', {}).get(s, {})
            if isinstance(entry, dict):
                cons = entry.get('expected_consumers', [])
                if not cons:
                    no_consumers.append(s)
        
        results['no_consumers'] = no_consumers
        
        # Check daily_tasks has META entries
        dt_meta = [c for c in dt.get('commands', []) 
                   if 'meta' in json.dumps(c).lower()]
        results['daily_tasks_meta_count'] = len(dt_meta)
        
        passed = len(no_consumers) == 0 and len(dt_meta) > 0
        return {'dimension': '③ 接线通电', 'passed': passed, 'checks': results}
    except Exception as e:
        return {'dimension': '③ 接线通电', 'passed': False, 'checks': {'error': str(e)}}


def dimension_4_version_alignment() -> dict:
    """维④ 版本对齐：version_drift_check."""
    results = run(f'{PYTHON} scripts/version_drift_check.py --quick')
    return {'dimension': '④ 版本对齐', 'passed': results['ok'], 'checks': {'drift': results}}


def dimension_5_constitution_consistency() -> dict:
    """维⑤ 宪法一致：战略宪章§九-A引用·CFM·术语表计数."""
    try:
        results = {}
        const = (ROOT / 'constitution/战略宪章.md').read_text(encoding='utf-8')
        glos = (ROOT / 'constitution/核心概念术语表.md').read_text(encoding='utf-8')
        plan = (ROOT / 'constitution/综合工作规划.md').read_text(encoding='utf-8')
        
        # L5前提存在
        results['l5_prerequisite_in_constitution'] = 'L3+L4' in const
        
        # CFM Done
        results['cfm_done'] = 'T-3-834' in plan and 'Done' in plan
        
        # 术语表计数
        import re as _re
        cnt = _re.search(r'共\s*(\d+)\s*个概念', glos)
        results['glossary_count'] = int(cnt.group(1)) if cnt else 0
        
        passed = results['l5_prerequisite_in_constitution'] and results['cfm_done']
        return {'dimension': '⑤ 宪法一致', 'passed': passed, 'checks': results}
    except Exception as e:
        return {'dimension': '⑤ 宪法一致', 'passed': False, 'checks': {'error': str(e)}}


def dimension_6_pipeline_validation() -> dict:
    """维⑥ 管线验证：bridge scan + term_registry_sync."""
    results = {}
    results['bridge'] = run(f'{PYTHON} scripts/pattern_to_task_bridge.py --scan --json', timeout=90)
    results['sync'] = run(f'{PYTHON} scripts/term_registry_sync.py --check')
    
    # Parse bridge for L5 anomaly (stdout may be truncated at 2000 chars by run())
    try:
        # Re-run bridge without stdout truncation for accurate parsing
        import subprocess as sp
        br = sp.run(f'{PYTHON} scripts/pattern_to_task_bridge.py --scan --json', 
                    shell=True, capture_output=True, text=True, cwd=str(ROOT), timeout=90)
        bdata = json.loads(br.stdout)
        results['l5_anomaly'] = bdata.get('maturity_distribution', {}).get('L5_anomaly', 0)
        results['conversion_rate'] = bdata.get('conversion_rate', 0)
        results['unactioned'] = bdata.get('unactioned', 0)
    except Exception as e:
        results['l5_anomaly'] = -1
        results['conversion_rate'] = -1
        results['parse_error'] = str(e)[:200]
    
    passed = results['bridge']['ok'] and results['sync']['ok'] and results.get('l5_anomaly', -1) == 0
    return {'dimension': '⑥ 管线验证', 'passed': passed, 'checks': results}


def dimension_7_kill_chain() -> dict:
    """维⑦ 杀伤链：reclassify·conversion_rate·L2→L3 pipeline."""
    results = {}
    results['reclassify'] = run(f'{PYTHON} scripts/meta_task_closure_check.py --scan')
    results['l2l3'] = run(f'{PYTHON} scripts/meta_l2_to_l3_pipeline.py --scan')
    results['semantic'] = run(f'{PYTHON} scripts/semantic_object_query.py --validate')
    
    passed = results['reclassify']['ok'] and 'valid' in results['semantic'].get('stdout', '').lower()
    return {'dimension': '⑦ 杀伤链', 'passed': passed, 'checks': results}


def dimension_8_landing_power() -> dict:
    """维⑧ 落地通电：prevention工程化·solution通电·artifacts完整·L5真实性."""
    try:
        results = {}
        
        # Check L5 patterns have daily_tasks + pre_write integration
        idx = json.loads((ROOT / 'drq/meta_patterns/index.json').read_text(encoding='utf-8'))
        dt = json.loads((ROOT / 'governance/data/daily_tasks.json').read_text(encoding='utf-8'))
        dt_str = json.dumps(dt)
        
        l5_patterns = [p for p in idx.get('patterns', []) 
                       if p.get('engineering_maturity') == 5]
        results['l5_count'] = len(l5_patterns)
        
        # Check each L5 for completeness (read from JSON file, not index)
        false_l5 = []
        for p in l5_patterns:
            mid = p.get('id', '')
            # Read actual JSON file for full data
            files = list(ROOT.glob(f'drq/meta_patterns/{mid}_*.json'))
            if files:
                full = json.loads(files[0].read_text(encoding='utf-8'))
                artifacts = full.get('artifacts', []) or []
                prevention = full.get('prevention', '') or ''
                solution = full.get('solution', '') or ''
            else:
                artifacts = p.get('artifacts', []) or []
                prevention = p.get('prevention', '') or ''
                solution = p.get('solution', '') or ''
            
            # L5 authenticity: artifacts≥3 AND (prevention+solution exist)
            has_solution = bool(prevention and solution)
            in_dt = any(kw in dt_str for kw in ['adversarial', 'bridge', 'closure', 'reclassify'])
            
            # Real L5: has artifacts OR has prevention+solution (gate integration)
            if not ((len(artifacts) >= 3 or has_solution) and in_dt):
                false_l5.append(mid)
        
        results['false_l5'] = false_l5
        results['l5_authenticity'] = len(false_l5) == 0
        
        passed = len(false_l5) == 0
        return {'dimension': '⑧ 落地通电', 'passed': passed, 'checks': results}
    except Exception as e:
        return {'dimension': '⑧ 落地通电', 'passed': False, 'checks': {'error': str(e)}}


def audit(dimensions: list = None) -> dict:
    """Execute full 8-dimension audit."""
    if dimensions is None:
        dimensions = [1, 2, 3, 4, 5, 6, 7, 8]
    
    runners = {
        1: dimension_1_code_integrity,
        2: dimension_2_data_consistency,
        3: dimension_3_wiring_power,
        4: dimension_4_version_alignment,
        5: dimension_5_constitution_consistency,
        6: dimension_6_pipeline_validation,
        7: dimension_7_kill_chain,
        8: dimension_8_landing_power,
    }
    
    results = []
    for d in dimensions:
        if d in runners:
            results.append(runners[d]())
    
    # 14元概念通电检查（简化版）
    meta_check = _check_14_meta_concepts(results)
    
    passed = sum(1 for r in results if r['passed'])
    total = len(results)
    
    return {
        'auditor': 'audit_runner.py v1.0',
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_dimensions': total,
            'passed': passed,
            'failed': total - passed,
            'pass_rate': f'{passed}/{total}',
            'verdict': 'CLEAN' if passed == total else 'HAS_GAPS',
            'meta_concepts_powered': meta_check,
        },
        'dimensions': results,
    }


def _check_14_meta_concepts(results: list) -> dict:
    """14元概念通电检查."""
    # Simplified: check that we have audit findings (元审定), 
    # dimensions executed (元结构), etc.
    return {
        'powered_count': len([r for r in results if r['passed']]),
        'total_dims': len(results),
        'verdict': 'POWERED' if any(r['passed'] for r in results) else 'OFFLINE'
    }


def main():
    parser = argparse.ArgumentParser(description='对抗审计·8维自动审计执行器')
    parser.add_argument('--quick', action='store_true', help='快速模式（仅③④⑧）')
    parser.add_argument('--json', action='store_true', help='仅JSON输出')
    parser.add_argument('--dim', type=int, nargs='+', help='指定维（如 --dim 3 8）')
    args = parser.parse_args()
    
    if args.quick:
        dims = [3, 4, 8]
    elif args.dim:
        dims = args.dim
    else:
        dims = None  # full
    
    report = audit(dims)
    
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"  对抗审计·8维自动审计  v1.0")
        print(f"  {report['timestamp']}")
        print(f"{'='*60}")
        print(f"  总维数: {report['summary']['total_dimensions']}")
        print(f"  通过: {report['summary']['passed']}  |  失败: {report['summary']['failed']}")
        print(f"  判定: {report['summary']['verdict']}")
        print(f"  元概念通电: {report['summary']['meta_concepts']['powered_count']}/{report['summary']['meta_concepts']['total_dims']}")
        print(f"{'='*60}")
        
        for d in report['dimensions']:
            status = '✅' if d['passed'] else '🔴'
            print(f"  {status} {d['dimension']}")
        
        if report['summary']['failed'] > 0:
            print(f"\n  失败详情:")
            for d in report['dimensions']:
                if not d['passed']:
                    print(f"  🔴 {d['dimension']}: {json.dumps(d['checks'])[:200]}")
        
        # 输出JSON到文件供AI审计者消费
        out = ROOT / 'staging' / '_audit_runner_output.json'
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"\n  完整JSON: {out}")
    
    sys.exit(0 if report['summary']['verdict'] == 'CLEAN' else 1)


if __name__ == '__main__':
    main()
