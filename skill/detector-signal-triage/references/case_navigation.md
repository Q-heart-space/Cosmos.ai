# detector-signal-triage 分层判例库导航

> 2026-09-10·技能结构 v2.0 分层（META-1097）——SKILL.md 保持精简可执行，扩展判例/锚点详情分层收纳。
> 本目录为**导航与速查**：判例正文仍在 SKILL.md「已知高频缺陷模式（实证判例）」表（SSOT·不复制），本文件只做分层引用与检索辅助——防第二真相源（铁律X）。

## 判例定位速查（v1.9 全量 23 行·按缺陷族分类）

| 缺陷族 | SKILL.md 判例行 | 代表判例 | META 锚点 |
|:--|:--|:--|:--|
| 匹配/扫描类盲区 | 正则后缀漏配·路径拼接·只读前 N·渐进披露漏扫 | header_parser 16 处孤立 | — |
| 注释/声明污染类 | 注释提及·检测器不自指·expected 声明质量 | render_viewb/consumer_check 假 P0 | META-1562/1563/1564 |
| 信号不可得类 | 默认 0 分·fail-closed 反向 | l5 Phase3 消失假零 | — |
| 崩溃/退出码类 | 导入期崩溃·同形退出码合法化·产出层崩溃 | constrained 子进程缺 HOME | 术语表 #310 |
| 声明/配置漂移类 | 真相源分裂·口径落后·锚点失效·退役未豁免 | preflight v1.10 vs registry v1.4 | — |
| 自反身性盲区 | 指纹无门禁·提示器恒报警·僵尸功能 | capability manifest 静默漂移 | — |

## 分诊主链路（语义方向验证→同文件自证→信号源四分→性质判定）

```
Step -1 信号源可信度四分 → Step 0 语义方向验证 → Step 0.5 同文件自证/双向验
  → Step 0.6 闭环回头自审 → 性质判定（①假红 ②假绿 ③真问题 ④提示器）
```

## 配套检索

- 术语表概念定义（SSOT）：constitution/核心概念术语表.md #309/#310/#311
- 反模式映射：governance/反模式门禁映射表.md（#63 检测器语义族）
- 误报反馈：governance/data/detector_feedback.json（detector_feedback.py --list）
- 技能自进化验证：`python scripts/skill_self_evolution_check.py --skill detector-signal-triage`
