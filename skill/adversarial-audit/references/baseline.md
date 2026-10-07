# 跨会话基线

## baseline.json 格式

```json
{
  "last_audit": "2026-08-09T18:51",
  "last_dimensions": 8,
  "last_blindspots": ["维③daily_tasks盲区", "七维计数不一致"],
  "last_l5_count": 2,
  "last_conversion_rate": 19.5,
  "recurrence_tracker": {
    "task_state_machine_block": {"count": 2, "upgraded_to": "P0"},
    "false_l5": {"count": 1, "severity": "P0"}
  }
}
```

## 自适应频率规则

| 复发次数 | 审计频率 | 处理 |
|:--|:--|:--|
| 第1次 | 标准触发（≥3Agent·≥5文件） | 记录 |
| 第2次 | 降低阈值（≥3文件） | P1→P0 |
| 第3次 | 每次文件修改后自动审计 | 阻断级 |

## 继承规则

- 上次 blindspots → 本次 Step 3 增量检查项
- recurrence_tracker count ≥2 → 自动升级 P0 阻断
- 上次L5 vs 本次L5 → 如减少 → 经验#3「打补丁修复无D5+」额外触发
