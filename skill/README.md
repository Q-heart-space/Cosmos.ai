# skill/ — 可安装使用的技能

Q博士 对外发布的**技能便携版**（portable build）。每个技能占**一个子目录**，互不混叠。

## 已发布技能

| 技能 | 一句话 | 版本 |
|:--|:--|:--|
| [`ai-drift-guard/`](ai-drift-guard/) | AI 跑偏守卫：动手前 10 项自检协议 | 1.3.0-ext |

## 用法

1. 选一个技能子目录
2. 按其 `README.md` 安装（复制到 `~/.workbuddy/skills/<技能名>/`，或用 Import 导入）
3. 用自然语言触发词使用（如「AI跑偏守卫」）

## 结构约定

```
skill/<skill-name>/
├── SKILL.md          # 技能定义（触发词 + 协议）
├── references/       # 参考实现 / 清单
├── README.md         # 安装与使用
├── CHANGELOG.md      # 版本历史
├── CONTRIBUTING.md   # 该技能的贡献说明
└── LICENSE
```
