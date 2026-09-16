"""
Reference implementation of S5: template placeholder validation.
Adapt the IGNORE_KEYWORDS and IGNORE_PATTERNS lists to your stack.

Usage:
    python template_validator.py <path/to/generated.html>

Returns exit code 0 on clean, 1 on leaked placeholders.
"""
# > **版本**：v1.0 | **类型**：🧪 | **日期**：2026-07-01 | **状态**：活跃
# > **依赖**：—
# > **被依赖**：ai-drift-guard SKILL.md S5
# > **变更**：v1.0 新建
# > **用途**：AI-Drift-Guard S5 信号——模板占位符泄漏检测
import re
import sys

# JavaScript/CSS keywords that contain {} and are NOT placeholders
IGNORE_KEYWORDS = [
    'type', 'data', 'labels', 'datasets', 'scales', 'options',
    'plugins', 'legend', 'title', 'animation', 'indexAxis',
    'beginAtZero', 'display', 'position', 'usePointStyle',
    'boxWidth', 'pointRadius', 'fill', 'tension', 'borderColor',
    'backgroundColor', 'callbacks', 'tooltip', 'label', 'parsed',
    'stacked', 'grid', 'draw', 'responsive', 'maintainAspectRatio',
    'cutout', 'padding', 'borderWidth', 'fontSize', 'fontFamily',
    'barPercentage', 'categoryPercentage', 'spanGaps', 'stepped',
]

# Patterns that contain {} and are not placeholders
IGNORE_PATTERNS = [
    r'^\s*\{(\d+)\}\s*$',           # CSS: {3} = bold weight
    r'^[^:]*:\s*\{[^}]+\}$',        # CSS property: "font: {weight} {size} font"
    r'//.*$',                         # JS comments
    r'/\*.*\*/',                     # Block comments
]

def has_leaked_placeholders(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all {identifier} patterns
    pattern = re.compile(r'\{\w+\}')
    issues = []
    seen_lines = set()

    for i, line in enumerate(content.split('\n'), 1):
        matches = pattern.findall(line)
        for m in matches:
            key = m.strip('{}')

            # Skip known JS/CSS keywords
            if key in IGNORE_KEYWORDS:
                continue

            # Skip numeric values
            if key.isdigit():
                continue

            # Skip CSS-like patterns
            skip = False
            for ip in IGNORE_PATTERNS:
                if re.search(ip, line.strip()):
                    skip = True
                    break
            if skip:
                continue

            # Potential leaked placeholder
            if i not in seen_lines:
                stripped = line.strip()[:100]
                issues.append(f"Line {i}: '{m}' in: {stripped}")
                seen_lines.add(i)

    return issues


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python template_validator.py <file.html>")
        sys.exit(1)

    issues = has_leaked_placeholders(sys.argv[1])

    if issues:
        print(f"[FAIL] Found {len(issues)} leaked placeholder(s):")
        for issue in issues:
            print(f"  {issue}")
        sys.exit(1)
    else:
        print("[PASS] No leaked placeholders detected.")
        sys.exit(0)
