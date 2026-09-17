# Host adapters / 宿主适配器

本协议**不绑定任何 AI 平台**。`SKILL.md` 的 Tier A 只规定"宿主必须提供什么"，
不规定宿主叫什么、目录在哪、钩子如何命名。本文件说明如何为一个具体宿主写适配器。

## 适配器契约 / The contract

任何适配器只需做三件事：

| # | 提供 | 说明 |
|:--|:--|:--|
| 1 | `globalRuleMatchers` | **该宿主自己的**"全局规则/编排文件"清单。协议本体不含任何平台路径。 |
| 2 | 拦截点 | 在"工具调用/写入动作发生之前"拿到 `{ tool, arguments }` 并返回 `allow` / `deny` / `ask`。 |
| 3 | `logSink` | `deny` 时落一行 JSONL（`SKILL.md` A.6）。没有落点也要显式回报"日志不可用"，不要静默。 |

判定逻辑本身在 [`drift-guard-core.mjs`](drift-guard-core.mjs) 里——**不要在你的适配器里重写它**。
重写就会产生平台间的判定漂移，这恰恰是本协议要避免的。

```js
import { createLedger, evaluate } from './drift-guard-core.mjs'

const ledger = createLedger()
const config = {
  globalRuleMatchers: [ /* 宿主自定 */ ],
  searchTools: [ /* 宿主自定 */ ],
  writeTools: [ /* 宿主自定 */ ],
}
const decision = evaluate({ name, arguments: args }, ledger, config)
```

---

## 实例 A：DSH（Cordis 内核）

> 这只是**一个实例**。它的存在不意味着本协议面向 DSH。

DSH 的每个能力都是 Cordis 插件行；工具派发有一个 waterfall 事件可作为拦截点。

- 拦截点：`tools/pre-execute`（waterfall，返回 `{kind:'deny', reason}` 即阻断）
- 搜索类工具：`grep`、`glob`
- 写入类工具：`write`、`edit`
- `logSink`：`$DSH_HOME/ai-drift-guard/blocks.jsonl`
- `globalRuleMatchers`：

```js
[
  { basename: 'cordis.yml' },
  { basename: 'cordis.patch.yml' },
  { basename: 'settings.yaml' },
  { basename: 'pnpm-workspace.yaml' },
  { basename: 'AGENTS.md' },
  { basename: 'CLAUDE.md' },
  { basename: '.npmrc' },
  // package.json 只在宿主自己的 profile 目录下才算"全局"——
  // 这个路径片段是 DSH 专有的，所以它属于适配器，不属于协议。
  { basename: 'package.json', pathIncludes: '/profiles/' },
]
```

宿主侧的注册片段：

```js
ctx.on('tools/pre-execute', async (exec, next) => {
  const decision = evaluate(exec, ledger, config)
  if (decision.kind === 'allow') return next()
  const logError = persist(makeLogRecord(decision, exec, ++seq))
  const suffix = logError === null ? '' : '\n[log unavailable: ' + logError + ']'
  return { kind: 'deny', reason: decision.reason + suffix }
})
```

**实测记录**（2026-09-17，DSH Desktop 上的真实运行结果，非声明）：

| 用例 | 结果 |
|:--|:--|
| 写含 `{page_title}` / `{heading}` 的 `.html` | 拒绝，并报出 line 5 / line 8 |
| 写含 `{data}` / `{type}` 的 `.html` | 放行（命中 `IGNORE_KEYWORDS`，无误报） |
| 写 `settings.yaml`（未扫描） | 拒绝 |
| 先搜索该 basename，再写同一文件 | 放行（ledger 生效） |
| 被拒文件是否落盘 | **未落盘**——拦截发生在 dispatch 前 |

---

## 实例 B：pre-commit / CI（完全不涉及 AI 平台）

这是**最中立**的强制方式：约束的是产物，不是模型。

`.git/hooks/pre-commit`：

```sh
#!/bin/sh
files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.html?$' || true)
[ -z "$files" ] && exit 0
node skill/ai-drift-guard/references/drift-guard-core.mjs check $files
```

CI（任何厂商）等价于：

```yaml
- run: node skill/ai-drift-guard/references/drift-guard-core.mjs check $(git ls-files '*.html' '*.htm')
```

优点：无需宿主提供钩子；S5 在这个层面是**真正不可绕过**的（除 `--no-verify`）。
缺点：只在提交时拦截，不在生成时拦截——反馈来得晚。

**两者建议同时启用**：适配器给出即时反馈，pre-commit 兜底。

---

## 实例 C：其他宿主 / Other hosts

对任何"能拿到工具调用、并能拒绝它"的宿主，写适配器的检查清单：

1. 有没有 dispatch **之前**的钩子？只有"事后通知"的宿主**无法**实现 Tier A——如实说明，不要假装。
2. 把 `grep/glob/read/search` 里**真正的搜索类**工具列进 `searchTools`。把 `read` 列进去会让 S4 形同虚设
   （读文件本身不是"关联扫描"）。
3. `globalRuleMatchers` 只收**该宿主语境下改了会影响别处**的文件。宁可少，不可滥——
   一条会拦住正常工作的规则，第二天就会被关掉。
4. `writeTools` 的**第一个**元素被当作"全量写入"（读 `arguments.content`），
   其余按"局部替换"处理（读 `arguments.new_string`）。顺序有意义。
5. 落点不可写时，必须在 `deny` 的 reason 里回报，否则你会得到一个"看起来在工作"的守卫。

---

## 反例：不要做的事 / Anti-patterns

| 反例 | 为什么错 |
|:--|:--|
| 在适配器里重新实现 S5 检测 | 平台间判定漂移，协议失去意义 |
| 把某个平台的路径 (`~/.foo/skills`) 写进 `SKILL.md` | 平台绑定——本协议 v1.4 移除的正是这类内容 |
| 声称 Tier B 信号"已被保证" | 提示词没有强制力，这是自欺 |
| 用"文件已投递"冒充"已被采纳" | 同理：写了规则 ≠ 规则生效；必须有实测记录 |
