> 🆕 孤儿文件标注（2026-09-16 技能审阅）：本文件未被 SKILL.md 或 references 引用·可能为历史遗留/已废弃·保留待清理。

# Agent 必检项模板 v1.0

> **来源**：2026-08-09 四轮对抗审计复盘——Agent 因缺少强制性原子检查项而遗漏 6 个 bypass 脚本、5 个 D0_FILES 缺陷、3 个 daily_tasks 命令错配

---

## Agent A：Constitution 写入完整性审计

### 必检原子扫描（5 条·不可跳过）

```bash
# 1. 扫描所有 constitution/ 裸写
cd <本库根>
grep -rn "constitution/" scripts/*.py | grep -E "write_text|open.*'w'" | grep -v "secure_write\|read_text\|#"

# 2. 对比 D0_FILES vs 实际文件
python -c "
from pathlib import Path
import os
d0 = ['constitution/跨空间本体论.md','constitution/本质定位.md','constitution/战略宪章.md','constitution/系统架构.md','constitution/元层总纲.md','constitution/九维审定规范.md','constitution/决策OS规范.md','constitution/综合工作规划.md','constitution/FILE_MANIFEST.md','constitution/人机对齐协议.md','constitution/核心概念术语表.md','constitution/成长记录.md','constitution/流程日记.md','constitution/Stable_Core_清单.md']
actual = [f'constitution/{f}' for f in os.listdir('constitution') if f.endswith('.md') and not f.startswith('.')]
missing_in_d0 = [f for f in actual if f not in d0]
extra_in_d0 = [f for f in d0 if f not in actual]
print(f'Missing from D0_FILES: {missing_in_d0}')
print(f'Extra in D0_FILES: {extra_in_d0}')
"

# 3. 列出所有 secure_write 调用点（正面对比）
grep -rn "secure_write.*constitution" scripts/*.py | wc -l

# 4. 验证 G3B 白名单覆盖
grep -rn "secure_write.*constitution" scripts/*.py | sed 's/.*reason=.//' | sort -u

# 5. 检查 write_guard 信任梯度默认值
grep -A5 "_load_ruleset_rule" scripts/write_guard.py
```

### 自由研究方向

- write_guard 是否存在其他绕过路径（如 subprocess 调用、临时文件替换）
- 并发写入 constitution 同一文件的竞争条件
- G3B 白名单的维护机制是否自举

---

## Agent B：命令链完整性审计

### 必检原子扫描（5 条·不可跳过）

```bash
# 1. argparse 跨文件命令验证
python scripts/argparse_signature_auditor.py --validate-daily-tasks --json

# 2. 逐个脚本 --help 验证（排除已知假阳性）
for cmd in $(grep "python scripts/" governance/data/daily_tasks.json | sed 's/.*python scripts\///' | sed 's/ .*//' | sort -u); do
  echo -n "$cmd: "
  timeout 3 python "scripts/$cmd" --help >/dev/null 2>&1 && echo "OK" || echo "HELP_FAILED"
done

# 3. 超时 vs 实际执行时间对比（并行冗余检查）
# 提取 daily_tasks.json 中所有 timeout，对比实际 p95 执行时间

# 4. known_exit_codes 完整性检查
grep -A2 '"cmd"' governance/data/daily_tasks.json | grep -c "known_exit_codes"

# 5. 命令中脚本文件存在性检查
grep "python scripts/" governance/data/daily_tasks.json | sed 's/.*python scripts\///' | sed 's/ .*//' | while read f; do [ -f "scripts/$f" ] || echo "MISSING: $f"; done
```

### 自由研究方向

- concurrency_governor 的资源池公平性
- daily_tasks.json vs sunday_tasks.json 的调度去重
- 超时预算与实际执行时间的趋势分析

---

## Agent C：基础设施覆盖与接线完整性审计

### 必检原子扫描（5 条·不可跳过）

```bash
# 1. consumer_check 全接线
python scripts/consumer_check.py --full-wiring --json

# 2. circuit_power 僵尸资产
python scripts/circuit_power_check.py --json

# 3. 新增脚本接线检查（对比 git diff 或最近修改时间）
find scripts/ -name "*.py" -mtime -1 | while read f; do
  grep -q "$(basename $f)" governance/data/daily_tasks.json || echo "NOT_IN_DAILY: $f"
done

# 4. 核心设计原则落地检查清单 vs 实际日治调度
python scripts/doc_script_version_aligner.py --check --json

# 5. 注册表-接线图-日治调度三者一致性
python scripts/registry_integrity_guard.py --check
```

### 自由研究方向

- 寻找"已接未通"脚本（wiring_map 有但 daily_tasks 无）
- 新增基础设施的 consumer 覆盖完整性
- 14元概念的实际通电率
