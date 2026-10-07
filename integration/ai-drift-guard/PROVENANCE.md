# 来源与边界（`HO-081` G2 入云）

- **来源**：本机部署态 `%DSH_HOME%/profiles/desktop/plugins/ai-drift-guard/**`（🛑 机器本地·非受控载体）。
- **入云方式**：**逐件字节拷贝**（sha16 逐件对拍一致·见台账 §1719）——🛑 **非重写**。
- **关系**：本插件＝**技能核的宿主适配**：`lib/core.mjs` 是 `ai-drift-guard` 技能
  `references/drift-guard-core.mjs` 的**逐行副本**（🛑 **行尾按各面规范**：技能侧 CRLF／插件侧 LF
  ⇒ 「逐字节副本」的说法**不实**，已在 `lib/index.js` 头部就地订正）；`lib/index.js` 只做 DSH 接线。
- **判据**：`scripts/skill_plugin_parity_check.py`（逐行相同 ∧ 版本单源 ∧ 在本载体在册）。
- **🛑 未入云项**：`node_modules`（第三方）与其宿主运行时状态不在本目录。
