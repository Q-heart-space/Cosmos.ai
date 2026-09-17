"""
Reference implementation of S5: template placeholder validation.
Adapt the IGNORE_KEYWORDS and IGNORE_PATTERNS lists to your stack.

Usage:
    python template_validator.py <path/to/generated.html>

Returns exit code 0 on clean, 1 on leaked placeholders.

Keep this file in sync with references/drift-guard-core.mjs (the portable reference
implementation). Divergence between the two is a bug.
"""
# > **版本**：v1.1 | **类型**：🧪 | **日期**：2026-09-17 | **状态**：活跃
# > **依赖**：—
# > **被依赖**：ai-drift-guard SKILL.md A.4 (S5)
# > **变更**：v1.1 修复 URL 盲区——注释判定前先中和 `://`，否则任何含 https:// 的行被整行跳过
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
]

# Comment markers, applied AFTER neutralizing URL schemes.
COMMENT_PATTERNS = [
    r'//',                            # JS line comment
    r'/\*.*\*/',                      # Block comment
]

# Control characters standing in for the `//` of a URL scheme separator.
URL_SCHEME_GUARD = ':\x01\x01'

# Unicode-aware placeholder pattern. `\w` in Python is already Unicode-aware,
# which is required so that `{标题}` is detected.
PLACEHOLDER_PATTERN = re.compile(r'\{\w+\}')


def neutralize_url_schemes(line):
    """Replace `://` so a URL is never mistaken for the start of a JS comment.

    v1.0 matched r'//.*$' directly, which meant every line containing `https://`
    was skipped entirely — including lines that also carried a leaked placeholder.
    """
    return line.replace('://', URL_SCHEME_GUARD)


def is_ignorable_line(trimmed):
    for pattern in IGNORE_PATTERNS:
        if re.search(pattern, trimmed):
            return True
    neutral = neutralize_url_schemes(trimmed)
    for pattern in COMMENT_PATTERNS:
        if re.search(pattern, neutral):
            return True
    return False


def has_leaked_placeholders(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []
    seen_lines = set()

    for i, line in enumerate(content.split('\n'), 1):
        trimmed = line.strip()
        if is_ignorable_line(trimmed):
            continue

        for m in PLACEHOLDER_PATTERN.findall(line):
            key = m.strip('{}')

            # Skip known JS/CSS keywords
            if key in IGNORE_KEYWORDS:
                continue

            # Skip numeric values
            if key.isdigit():
                continue

            # Potential leaked placeholder — report at most one per line
            if i not in seen_lines:
                issues.append(f"Line {i}: '{m}' in: {trimmed[:100]}")
                seen_lines.add(i)

    return issues


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python template_validator.py <file.html>")
        sys.exit(1)

    failed = False
    for path in sys.argv[1:]:
        issues = has_leaked_placeholders(path)
        if issues:
            failed = True
            print(f"[FAIL] {path} — {len(issues)} leaked placeholder(s):")
            for issue in issues:
                print(f"  {issue}")
        else:
            print(f"[PASS] {path}")

    sys.exit(1 if failed else 0)
