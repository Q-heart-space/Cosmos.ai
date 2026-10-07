# my-experts 市场（Q博士 自建专家）——适配产物

> 🛑 本目录是**适配层**（分支 `host-adapters`）：机器与平台只是**安装点**，差别只在**获取通道**。
> 包体在 `../experts/<id>/`；落位映射见下表。

## 🛑 写者归属（2026-09-26 时序取证后定案·第 107 轮）

- **包（`plugins/<id>/`）＝我方产出**：由 `workbuddy/experts/<id>/` 派生落位 ⇒ **我方负责**（已装 5 个）。
- **市场清单（`.codebuddy-plugin/marketplace.json`）＝平台管辖**：
  - 本机实测：我方写入（3,360 B·5 键）后 **30 秒内被还原成原内容**（sha 与改前**逐字节相同**·**mtime 保持**）；而**改名 25 秒无人补** ⇒ 是**事件触发型还原者**（非持续镜像同步）。
  - 🛑 **结论**：本目录携带的 `marketplace.json` **仅作「参考形态」**（记录平台实际落盘的 3 键形态：`{name,source,description}`），**不是我方落位件**；我方**只产包**，清单交给平台/平台注册器。
  - 依据：A机 E154 一手取证——平台按 **`readPluginManifestFromDir(path.join(pluginsDir, entry.name))`＝扫描 `plugins/` 目录**枚举专家；`marketplace.json` 是**市场级清单**。

## 落位映射（占位符·🛑 禁机器绝对路径）

| 分支（源） | 宿主（目标） | 写者 |
|:--|:--|:--|
| `workbuddy/experts/<id>/`（5 包：plugin.json ＋ agents/<id>.md ＋ avatars/） | `${PLATFORM_CONFIG_DIR}/plugins/marketplaces/my-experts/plugins/<id>/` | **我方**（deployer `expert_packages` 面） |
| `workbuddy/marketplaces/my-experts/.codebuddy-plugin/marketplace.json` | `${PLATFORM_CONFIG_DIR}/plugins/marketplaces/my-experts/.codebuddy-plugin/marketplace.json` | **平台**（🛑 我方仅留**参考形态**·不落位） |

## 验收（有运行时的机器）

1. 结构：`plugins/` 下 **5 个目录**，每个含 `.codebuddy-plugin/plugin.json` ＋ `agents/<id>.md`。
2. 界面：重启平台后**专家区应列出 5 位专家**（决策专家／跨空间实时反哺专家／治理深审专家／行业情报分析师／修复专家）。
3. 🛑 「配置根存在 ≠ 运行时已装」——运行时取证见描述符 `runtime_probe`（`workbuddy=unverified`）。
