# 批量修复脚本模板与验证协议

> ⚠️ **V19.0 教训**：H3 重编号脚本失败 4 次（v2-v4），表格去重脚本失败 4 次（v2-v5），根因均为未先在小样本上验证。总浪费约 120k tokens。

## 铁律：先验证匹配，再写完整脚本

```bash
# ✅ 正确做法：先写 5 行 snippet 验证匹配逻辑
python -c "
import re
with open('报告文件.md', 'r', encoding='utf-8') as f:
    content = f.read()
matches = list(re.finditer(r'### 19\.\d+', content))
print(f'Found {len(matches)} matches')
for m in matches[:3]:
    print(repr(content[m.start():m.start()+50]))
"
# 确认匹配数量和内容正确后 → 再写完整修复脚本

# ❌ 错误做法：直接写完整脚本 → 运行 → 失败 → 重写
```

## 脚本操作防级联冲突

**问题**：全局 `content.replace()` 会修改首次出现的目标，造成级联冲突。

| ❌ 错误 | ✅ 正确 |
|:--|:--|
| `content.replace('**表 3-29**', '**表 3-30**')` — 全局替换 | 行级别去重替换 — 只修重复行 |
| `re.sub(r'### 19\.(\d+)', repl, content)` — 全文字符串替换 | 行级别标志位法 — 定位区间内逐行替换 |

```python
# ✅ 正确：行级别去重替换（表格编号）
seen = {}
for i, line in enumerate(lines):
    m = re.match(r'(\*\*表 )(\d+-\d+[a-z]?)(\s*数据表\*\*.*)', line.rstrip('\n'))
    if m:
        num = m.group(2)
        if num in seen:
            new_num = f'{ch}-{next_serial}'
            new_lines.append(f'{m.group(1)}{new_num}{m.group(3)}\n')
        else:
            seen[num] = i
            new_lines.append(line)
```

## 通用修复模板

| 修复场景 | 推荐方案 | 验证来源 |
|:--|:--|:--:|
| H3 编号重排 | 行级别标志位法 | V19.0 |
| 表格编号消重 | 行级别去重替换 | V19.0 |
| 锚点补全 | 定位 H2 行，在上一行插入 `<a id="ch-N"></a>` | V19.0 |
| 全局文本替换 | 仅在目标字符串全文唯一时使用 | — |
| ⚠️ 禁用 | 全局正则替换操作编号/锚点 | V19.0 教训 |

## 品牌色一致性自动检查

```python
import json, pathlib, re

def check_brand_color_consistency(css_text):
    brand = json.loads(
        pathlib.Path(__file__).parent / "references" / "brand_colors.json"
    )
    for name, expected in brand["colors"].items():
        var_name = f"--{name.replace('_', '-')}"
        match = re.search(rf'{var_name}\s*:\s*([#\w]+)', css_text)
        actual = match.group(1) if match else None
        if actual and actual != expected:
            print(f"⚠️ 品牌色不一致: {name} 应为 {expected}, 实际 {actual}")
```
