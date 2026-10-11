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
    pass: 待 decision-expert 裁决后填
```

## 三级闭环判据（**`META-1638` 族**）

| 级 | 内容 | 本轮状态 |
|--:|:--|:--|
| ① | **声明**（`global_memory_artifact_dir` / `global_identity`） | ✅ 已声明 |
| ② | **货落盘**（制品实体） | ✅ 已落（**但仅 A机 本地**） |
| ③ | **导入器/消费入口存在** | ✅ 已建（`scripts/global_memory_install.py`） |
| ④ | **端到端正控真跑（含缺件场景）** | ✅ 已通（`missing → ok`） |
| ⑤ | 🆕 **异机可达**（**可跨机携带**） | 🔴 **未达** —— **制品不在任何分支 ⇒ B机 拿不到** |
