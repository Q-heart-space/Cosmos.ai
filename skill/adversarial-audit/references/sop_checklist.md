> 🆕 孤儿文件标注（2026-09-16 技能审阅）：本文件未被 SKILL.md 或 references 引用·可能为历史遗留/已废弃·保留待清理。

# 7步对抗式审查 SOP 参考手册

> 补充到 `adversarial-audit` 技能的详细检查清单和实战案例。
> 🆕 v1.4 新增：清单启发记�� + 经验库完整版

## 清单启发记录（来自核心设计原则落地检查清单）

### 六条启发

| # | 清单元素 | 对抗审计对应 | 落地 |
|:--|:--|:--|:--|
| 1 | 10×4 矩阵 | 11维×4层 = 32 交叉点 | Step 3 矩阵化 |
| 2 | "通电≠PASS" | 架构验证层 vs 内容验证层 | 维③(通电) + 维⑧(PASS) |
| 3 | 经验库（§四） | 技能经验库 | 5条经验+升级机制 |
| 4 | 陀螺仪定位 | "不替代closure，验证方向" | 技能定位声明 |
| 5 | 日治自动化 | 关键检查 schedule daily_tasks | Step 1 基线注释 |
| 6 | 静态快照+动态 | 基线+增量审计 | Step 1 经验基线加载 |

### 第一原理推导

```
清单原则⑥「自指涉验证」→ 对抗审计 Step 8「审计者审计自己的审计过程」
清单原则⑦「递归闭环」→ 对抗审计「Step 3→Step 8→回到Step 3」
清单经验#11「声明滞后于实跑」→ 对抗审计维⑧「prevention工程化？solution通电？」
清单原则①「建成必通电」→ 对抗审计维③「daily_tasks调度≠空」
```

## 🆕 14 元概念映射

| 元概念 | 对抗审计对应 | 关键程度 |
|:--|:--|:--|
| 元通道 | Step 2 独立Agent通道 | 中 |
| **元闭环** | **Step 8→回到Step 3 递归自审循环** | **★ 核心** |
| 元审定 | 技能核心目的：审计被审计者 | 高 |
| 元决策 | Step 5 决策OS T0-T5 路由 | 高 |
| 元认知 | Step 8 盲区自审 + 经验库 | 高 |
| **元进化** | **经验库驱动检查项渐进升级** | **★ 核心** |
| 元动态 | 技能版本 D0-D3 (v1.0→v1.4) | 中 |
| 元复用 | Step 3 基础设施查询(BR.1) | 中 |
| 元结构 | Step 3 11维×4层矩阵 | 高 |
| 元级联 | Step 5 递归修复→复跑验证 | 高 |
| 元场景 | 触发条件: ≥3Agent·≥5文件 | 中 |
| 元产品 | 技能打包(.zip)·可分发 | 中 |
| 元对齐 | 宪法前置法Q1-Q6映射 | 高 |
| 元合规 | 质量门禁·P0/P1/P2 | 高 |

### "问题→技能" 管道

本技能从创建到 v1.4 的完整进化链：

```
问题观察("哲学性而非工程性")
  → 宪法前置法 Q1-Q6 推导(战略宪章 §九-A 入宪)
  → 基础设施查询(25 META脚本·6层管线)
  → 15任务四Phase分解计划
  → 4Agent并行执行(fixer/builder/registrar)
  → 对抗审计(11检查·4漏洞)
  → 递归闭环修复(task_state_machine阻断→修复→复验)
  → 五模式复盘(元模式提取)
  → META-1095注册(L4→注册→分类→桥接→规划)
  → 技能创建(从META-1095标准化7步SOP)
  → 技能自我审计(Step 8·6盲区)
  → 技能迭代升级(v1.0→v1.1⑧维→v1.2决策OS→v1.3递归自审→v1.4清单启发)
```

**这不是一次性的——这是 Q博士 自进化引擎的"问题→技能"管道的活体证明。** 每次重复这个管道，自进化能力就增强一次。

## 实战案例：2026-08-09 META 深度治理

### 第一次审计（14:17）

| Agent | 任务 | 文件产出 |
|:--|:--|:--|
| fixer | Phase1: L5判定修复+L0排除+重分级 | register_meta.py v1.5·audit_l5_downgrade.py |
| builder | Phase2: L2→L3管线+L2审计+bridge+closure | meta_l2_to_l3_pipeline.py v1.0·bridge v3.13·closure v1.43 |
| registrar | Phase3+4: 注册+术语表+自测+MANIFEST+宪法 | META-1086·concept_registry·self_test·战略宪章 |

#### 发现

| # | 级别 | 维 | 漏洞 | 修复 |
|:--|:--|:--|:--|:--|
| 1 | 🔴 | ⑥ | E2E Windows sandbox 脏状态 | ✅ test cleanup修复 |
| 2 | 🟡 | ② | reclassify 正则过宽 | ✅ 对齐 classify_maturity |
| 3 | 🟡 | ⑥ | Bridge 2 未处理模式 | ✅ 预期行为·低影响 |
| 4 | 🟡 | ⑤ | META 未入规划 | ✅ 手动追加 |

### 第二次审计（18:27）——任务完整性审查 → 发现 task_state_machine 阻断

### 第三次审计（18:34）——META-1093 第一原理审计

**致命缺口发现**：
- daily_tasks.json 中 **零 META 条目**——"转化率日治"未落地
- pre_write_check.py 中 **零 META consumers**——"宪法前置法 Q1-Q6 门禁"未工程化
- META-1093 artifacts 缺 4 个关键文件

**根因**：对抗式审查的维③（接线通电）只检查 wiring_map 是否有 consumers，**未检查 daily_tasks 是否实际调度** 和 **pre_write 是否有门禁落地**。

### 决策OS 标注

| 修复 | 决策层 | 维修深度 |
|:--|:--|:--|
| META-1093 L5→L4 降级 | T2 架构 | D1 |
| artifacts 3→7 | T4 数据 | D1 |
| daily_tasks +2 | T3 工具 | D3 |
| 技能七维→八维 | **T0-Meta** | **D9** |
| 技能 Step 5 嵌入决策OS | **T0-Meta** | **D9** |

> **关键洞察**：前三项修复(D1/D3)是症状修复——修了具体问题但同类模式下次仍会漏。后两项(D9)才是根因修复——升级了技能框架和方法论本身。**对抗式审计的真正价值在 D5+ 修复，不是 D1-D3 打补丁。**

**修复**：
1. META-1093 L5→L4 降级（L5 须 daily_tasks+pre_write 集成）
2. artifacts: 3→7（补全缺失文件）
3. daily_tasks: +2 META 命令
4. 技能升级：七维→八维（新增⑧落地通电·检查 prevention 工程化 + solution 通电）

审计 T-3-1097/1098/1099 (META-1093/1094/1095)

#### 发现

| # | 级别 | 维 | 漏洞 | 根因 | 修复 |
|:--|:--|:--|:--|:--|:--|
| 1 | 🟡 P1 | ⑥ | 3 个 META 已竣工(L4/L5)但任务标 Next | bridge 默认 Next | ✅ Next→Done |
| 2 | 🟢 P2 | ⑦ | meta_task_closure_check 自动闭合被 task_state_machine 阻断 | Next→Done 在 TRANSITIONS 中不存在 | ✅ 添加合法跃迁 |

**事故教训**：第一次审计时 P2 被记录追踪但未修复根因（task_state_machine TRANSITIONS），导致第二次审计时同样的问题再次出现。**对抗式审查必须修复所有发现的漏洞，不分 P 级。**

| Agent | 任务 | 文件产出 |
|:--|:--|:--|
| fixer | Phase1: L5判定修复+L0排除+重分级 | register_meta.py v1.5·audit_l5_downgrade.py |
| builder | Phase2: L2→L3管线+L2审计+bridge+closure | meta_l2_to_l3_pipeline.py v1.0·bridge v3.13·closure v1.43 |
| registrar | Phase3+4: 注册+术语表+自测+MANIFEST+宪法 | META-1086·concept_registry·self_test·战略宪章 |

### 对抗审计发现

| # | 级别 | 维 | 漏洞 | 位置 |
|:--|:--|:--|:--|:--|
| 1 | 🔴 | ⑥管线 | E2E 测试 Windows sandbox 脏状态 | test_meta_pipeline.py |
| 2 | 🟡 | ②数据 | reclassify L3→L4 正则过宽 | meta_task_closure_check.py:367 |
| 3 | 🟡 | ⑥管线 | Bridge 报告 2 个未处理模式 | pattern_to_task_bridge.py |
| 4 | 🟡 | ⑤宪法 | META-1085 未入综合规划 | 综合工作规划.md |

### 修复后验证

| 检查 | 修复前 | 修复后 |
|:--|:--|:--|
| E2E test_meta_pipeline | FAIL (sandbox) | 6/6 PASS |
| classify_maturity L5 | max(levels) | 3 in levels and 4 in levels |
| 虚假 L5 数量 | 26 | 2 |
| L2→L3 转化率 | 8.7% | 19.5% |

## 十一维审计详细检查清单（①-⑧ + ⑨宪法模板完整性 ⑩第一原理推导完整性 ⑪名称语义准确性）

### ① 代码完整性
- [ ] classify_maturity L5 用 subset 而非 max
- [ ] test_meta_pipeline.py 6/6 PASS
- [ ] 无 UnboundLocalError / NameError
- [ ] 新脚本 python 语法通过
- [ ] 修改的脚本 import 路径正确

### ② 数据一致性
- [ ] engineering_maturity 写入 JSON 文件
- [ ] lifecycle_state 已填充（非 unknown）
- [ ] source 字段已填充
- [ ] index.json 与 JSON 文件双向同步
- [ ] META 去重（无重复 ID）

### ③ 接线通电
- [ ] 新脚本在 circuit_wiring_map.json 中
- [ ] expected_consumers > 0
- [ ] 新脚本在 FILE_MANIFEST 中
- [ ] 新脚本在 self_test_registry 中
- [ ] meta_l2_to_l3_pipeline 在 daily_tasks（如需要）

### ④ 版本对齐
- [ ] 脚本头版本号与实际变更一致
- [ ] FILE_MANIFEST 版本号与脚本头一致
- [ ] version_drift_check 返回 0
- [ ] 术语表版本号与 registry 一致

### ⑤ 宪法一致
- [ ] 战略宪章 §九-A 引用最新版本
- [ ] CFM T-3-834 = Done
- [ ] 术语表概念总数与 PART A 一致
- [ ] 新概念已入术语表+concept_registry
- [ ] 成长记录已更新

### ⑥ 管线验证
- [ ] test_meta_pipeline.py 6/6
- [ ] pattern_to_task_bridge --scan --json 0 L5_anomaly
- [ ] meta_task_closure_check --scan 分布正确
- [ ] closure pileup P0=0
- [ ] term_registry_sync --check aligned

### ⑦ 杀伤链
- [ ] --reclassify 正确升级（不降级）
- [ ] _check_meta_conversion_rate 正确计算
- [ ] meta_l2_to_l3_pipeline --scan 有输出
- [ ] concept_dependency_inferrer 通电
- [ ] semantic_object_query --validate valid

### ⑧ 落地通电（🆕 v1.1·2026-08-09 事故驱动）
- [ ] **prevention 工程化检查**：声称的 prevention 是否在 pre_write_check 中有对应门禁？
- [ ] **solution 通电检查**：声称的 solution（如"转化率日治"）是否在 daily_tasks.json 中有对应调度？
- [ ] **artifacts 完整性**：META.artifacts 是否列出了所有相关文件？（宪法·脚本·治理·清单）
- [ ] **L5 真实性**：L5 标记是否真实——必须有 daily_tasks 调度 + pre_write 门禁二者同时存在

## 🆕 Step 8：递归自审退化清单

### 五次自审盲区

| 盲区 | 触发信号 | 处置 |
|:--|:--|:--|
| 1 维度遗漏 | 十一维审计中有维未触发但应触发 | 升级技能维度（如七维→八维） |
| 2 深度不足 | 所有修复 ≤ D3 无 D5+ | 追加 T0-Meta 框架级修复 |
| 3 假闭合 | 状态标 Done/L5 但实际未通电 | 降级+补 daily_tasks/pre_write |
| 4 级联遗漏 | 修复引入新 drift/wiring gap | 复跑 Step 3 十一维审计 |
| 5 元循环断裂 | META 未通过全链路注册 | 补 register+classify+bridge |

### 停止条件五联检查
- [ ] ⬜ Step 3 十一维审计零 P0 + 零 P1 + P2 已全部修复
- [ ] ⬜ Step 6 E2E 全绿
- [ ] ⬜ Step 8 盲区清单全部「✅ 已处置」
- [ ] ⬜ 深度学习 L4 到达（全部"做不到"→规划任务）
- [ ] ⬜ 最少 1 个新 META 已通过 register→classify→bridge 全链路
