# 贡献指南 / Contributing

感谢你参与 **Cosmos.ai** —— Q博士 的对外公开库。欢迎以三种方式回传（外部 → Q博士）：

## 1. 提出问题或建议

用 [Issues](../../issues) 反馈。请说明三段：**你做了什么 → 期望什么 → 实际什么**。

## 2. 贡献技能 / 资质

用 Pull Request 提交。要求：

- **技能** → 放 `skill/<skill-name>/`，须含 `SKILL.md` + `README.md` + `references/`（如有）+ `LICENSE`
- **自闭环**：`SKILL.md` + `references` + 脚本 + 许可证齐备（缺脚本 = 技能失效）
- **自检可跑**：脚本不能只是躺在 `references/` 里。凡声明"已生效"的行为，
  必须附一条**任何人可复现**的自检命令（例如 `node references/selftest.mjs`），
  并在 PR 里贴出输出。没有可复现验证的"修复"，按未修复处理。
- **平台中立**：协议本体不得写入任何具体 AI 平台的目录结构、钩子名或 SDK。
  平台差异写进适配器文件。
- 无密钥泄漏、无内部私有引用

## 3. 参与讨论

用 [Discussions](../../discussions)。

## 评审与合并

所有 PR 经评审后并入对应能力域。被采纳的贡献将列入 [CONTRIBUTORS.md](CONTRIBUTORS.md)。

## 边界

本库只接受**可公开的派生知识**。请勿提交内部宪法、治理原文、凭证或任何私有数据。
