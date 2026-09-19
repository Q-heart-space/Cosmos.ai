# spec-cache/ — 竞品规格快照缓存

> **用途**：解 A11「无结果复用机制」——避免每次都从零重查同一竞品。
> 版本：v1.5.0 | 2026-09-15
> **加载时机**：Step -1 先扫本目录，命中即走差量更新（非全量重查）。

## 一、180 天复用协议

```
Step -1 扫 cache：
  ├─ 命中且 ≤180 天 → 直接复用 + 仅验证关键参数是否变更
  ├─ 命中且 >180 天 → 降级为「参考」+ 全量重查
  └─ 未命中 → 全量查询 → 查完后写入本目录
```

## 二、快照命名与格式

**命名**：`<厂商>_<型号>.yaml`（如 `Advantech_MIC-733-AO.yaml`）

**格式**：

```yaml
vendor: Advantech
model: MIC-733-AO
snapshot_at: "2026-09-15"
verified: true                 # 是否经多源交叉验证
sources:
  - url: "https://..."
    fetched_at: "2026-09-15"
    tier: 1                    # 信源分级 1-4
specs:
  cpu: "..."
  compute:
    int8_sparse_tops: 275      # ⚠️ 量纲标注（rule-6）
    note: "系列营销值·32G SKU 实为 200"
  memory: "..."
  tdp: "..."
  network: "..."
  serial: "..."
  certifications: [...]
  temp_range: "..."
lifecycle:
  status: "在售"               # 在售/EOL/LTB
  penalty: 1.0
confidence: "高"
```

## 三、当前缓存索引

| 厂商 | 型号 | 快照日 | 时效 | verified |
|:--|:--|:--|:--|:--:|
| AAEON | BOXER-8741AI | 2026-09-15 | 新鲜 | — |
| Advantech | MIC-733-AO | 2026-09-15 | 新鲜 | true |
| Advantech | UNO-258 | 2026-09-15 | 新鲜 | — |
| Vecow | EAC-5000 | 2026-09-15 | 新鲜 | — |
| Neousys | NRU-230V-AWP | 2026-09-15 | 新鲜 | — |
| JWIPC | JEA-E608S/E618S | 2026-09-15 | 新鲜 | — |

## 四、写入契约

1. 竞品查询完成后，**必须**写快照到本目录（否则下次仍从零查）
2. `snapshot_at` 为写入日期，作为时效判定基准
3. `verified: true` 仅当经 ≥2 独立源交叉验证
4. 量纲字段（算力）**必须**标注口径（rule-6 精神）
5. 索引表同步更新

## 五、与 SKILL.md 的关系

- SKILL.md Step -1 引用本目录作为「复用入口」
- 本目录文件**不进入**主上下文（按需加载·避免 token 浪费）
- 与 `fallback_sourcebook.yaml` 互补：sourcebook 是「厂商清单」，spec-cache 是「已查快照」
