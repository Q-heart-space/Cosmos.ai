# dsh-plugin-ai-drift-guard

把 [Q博士 / Cosmos.ai](https://github.com/Q-heart-space/Cosmos.ai) 的 `ai-drift-guard`
移植到 DeepSeek Harness，并把其中**可机械判定**的信号从提示词升级为**运行时工具门禁**。

## 强制执行的信号

| 信号 | 触发 | 行为 |
|:--|:--|:--|
| **S5** | `write`/`edit` 的 `.html`/`.htm` 内容含未替换的模板占位符（`{title}`、`{标题}`…） | dispatch 前拒绝，列出具体行号 |
| **S4** | `write`/`edit` 改动全局规则/编排文件，且本会话未记录关联扫描 | dispatch 前拒绝，给出解除命令 |

S4 覆盖的文件：`cordis.yml`、`cordis.patch.yml`、`settings.yaml`、`pnpm-workspace.yaml`、
`.npmrc`、`AGENTS.md`、`CLAUDE.md`，以及 DSH profile 目录下的 `package.json`。

解除 S4：先对该文件名执行一次 `grep` 或 `glob`。

## 未强制执行的信号

S1/S2/S3/S6/S7/S8/S9/S10 仍只是提示词，通过同名 Skill 提供给模型。
本插件不声称覆盖它们。

## 拦截日志

```
$DSH_HOME/ai-drift-guard/blocks.jsonl
```

每次拦截追加一行 JSON（`seq` / `at` / `signal` / `tool` / `target` / `reason` / `detail`）。

## 已知边界

- 只观测**工具调用**。pnpm 等直接改写文件不会经过本门禁。
- S4 按 basename 精确相等匹配，带前后缀的同名文件不拦。
- S5 沿用原作者校验器的 `//` 忽略规则：含 `//` 的行（如带 `https://` 的 `<script src>`）整行跳过。
- S5 的 `IGNORE_KEYWORDS` / `IGNORE_PATTERNS` 与 `references/template_validator.py` v1.0 一致。

## 安装 / 卸载

```bash
# 安装（profile 目录下）
dsh plugin --profile desktop add link:./plugins/ai-drift-guard

# 卸载
dsh plugin --profile desktop remove dsh-plugin-ai-drift-guard
```

安装后需重启 DSH Desktop 生效。

## 出处与许可

信号编号、S5 判定表来自 Q博士 的 `ai-drift-guard`。MIT。
