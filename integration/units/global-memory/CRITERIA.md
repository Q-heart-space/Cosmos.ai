# L1 接入判据（`l1/CRITERIA.md`·**各宿主通用**）

> **本件是 `README.md` §二判据的机读展开** —— **只列判据与命令·不含身份件全文**。

## 判据表

```yaml
criteria:
  - id: C1
    name: 宿主配置根可解析
    cmd: python scripts/host_paths.py --self-test
    pass: rc == 0
  - id: C2
    name: 三件套声明齐全
    cmd: python -c "import host_paths as h;print(len(h.PLATFORM_LAYOUTS['workbuddy']['global_identity']))"
    pass: 输出 == 3
  - id: C3
    name: L1 三件套实存
    cmd: 逐件 os.path.isfile(host_config_dir()/name)
    pass: 3/3
  - id: C4
    name: 角色分型与验真
    cmd: python scripts/business_space_memory_check.py
    pass: rc == 0
  - id: C5
    name: 异机可达（关键·防虚指）
    cmd: 消费机跑 business_space_memory_check
    pass: rc == 0 AND role in {canonical, consumer, portable-consumer} 且 status == ok
    note: 🛑 指向「本机本地路径」的实现⇒对异机即虚指⇒本项必红
  - id: C6
    name: 身份三件纳管（缺口 B·待裁）
    cmd: 检查 global_identity 是否含 IDENTITY.md/SOUL.md/USER.md
    pass: 待 决策专家（决策单元治理形态）——把「重大决策」从口头判断变成**可复算的决策资产**：按宪法自陈的三元组（决策依据＋替代方案评估＋验收标准）× 证据链 × 带宽匹配 × 授权链 × 收据链产出六件套，用**决策六问 ＋ A/B 回归**判合格、用**回测通道**扫存量裁决件、用决策OS三维矩阵定层级（T0–T5）。触发词：决策专家、决策单元、决策资产、决策OS、裁决、该不该上、定不定、替代方案评估、六件套、决策六问、回滚与失效条件、用Q博士决策、从第一原理推导、决策回测。触发词主通道=按真实输入自动路由（`qdr_router` 的 `skill_rules`），名称仅作内部标识与对外品牌。（能力边界：只做「决策的产出与合格性判定 ＋ 存量回测」·不代替 `adversarial-audit` 做对抗式审计·不代替 `task-retrospective` 做复盘·不代替 `constitution-steward` 改宪法·不代替 `meta-library-steward` 管库） 裁决后填
```

## 三级闭环判据（**`META-1638` 族**）

| 级 | 内容 | 本轮状态 |
|--:|:--|:--|
| ① | **声明**（`global_memory_artifact_dir` / `global_identity`） | ✅ 已声明 |
| ② | **货落盘**（制品实体） | ✅ 已落（**但仅 A机 本地**） |
| ③ | **导入器/消费入口存在** | ✅ 已建（`scripts/global_memory_install.py`） |
| ④ | **端到端正控真跑（含缺件场景）** | ✅ 已通（`missing → ok`） |
| ⑤ | 🆕 **异机可达**（**可跨机携带**） | 🔴 **未达** —— **制品不在任何分支 ⇒ B机 拿不到** |
