/**
 * AI-Drift-Guard — DSH 适配器
 *
 * 本文件**只做 DSH 特有的接线**，判定逻辑一行都不在这里：
 *   1. 提供 globalRuleMatchers（DSH 语境下"改了会影响别处"的文件清单）
 *   2. 把核心接到 tools/pre-execute（缝3：派发前拒绝）
 *   3. 把 S9 接到 agent/pre-step（缝2：模型开始生成前拒绝该步）
 *   4. 提供 logSink，并注册同名 Skill
 *
 * 判定逻辑来自 ./core.mjs —— Cosmos.ai 公开库 references/drift-guard-core.mjs
 * 的**逐行副本**（🛑 **行尾按各面规范**：技能侧 CRLF／插件侧 LF ⇒ **不是**逐字节副本；
 *  🆕 r1545·`HO-081` G1 就地订正——原「逐字节副本」说法与实测不符），由 references/selftest.mjs 的 13 项断言覆盖。
 * 不要在这里重写它：重写就会产生平台间的判定漂移。
 *
 * 协议出处：https://github.com/Q-heart-space/Cosmos.ai
 *
 * ── 版本史 ───────────────────────────────────────────────────
 * v1.0.0  初版。漏了 inject 声明，技能被静默跳过（守卫却照常工作）。
 * v1.0.1  补 inject: ['skills']；加 boot.jsonl 自诊断。
 * v1.1.0  补 S9 硬拦截（agent/pre-step reject）；分层由两层改三层；
 *         **有意不做** S3/S7 —— DSH 已有沙箱与审批策略，重复平台能力
 *         只会扩大误报面。误报的代价高于漏报，这是本协议的设计律。
 */

import { appendFileSync, mkdirSync } from 'node:fs'
import { homedir } from 'node:os'
import { dirname, join } from 'node:path'
import { createLedger, evaluate, isStopMessage } from './core.mjs'

export const name = 'ai-drift-guard'

// skills 是硬依赖：apply 必须等它挂载完成，否则技能注册会被静默跳过。
export const inject = ['skills']

const ADAPTER_VERSION = '1.1.0'

const DSH_HOME = process.env.DSH_HOME && process.env.DSH_HOME.length > 0
  ? process.env.DSH_HOME
  : join(homedir(), '.dsh')
const STATE_DIR = join(DSH_HOME, 'ai-drift-guard')
const LOG_PATH = join(STATE_DIR, 'blocks.jsonl')
const BOOT_PATH = join(STATE_DIR, 'boot.jsonl')

/* ------------------------------------------------------------------ *
 * 1. 适配器配置 —— 平台专有的东西全部集中在这里
 * ------------------------------------------------------------------ */

const DSH_CONFIG = {
  searchTools: ['grep', 'glob'],
  // 第一个元素被当作"全量写入"（读 arguments.content），其余读 arguments.new_string
  writeTools: ['write', 'edit'],
  globalRuleMatchers: [
    { basename: 'cordis.yml' },
    { basename: 'cordis.patch.yml' },
    { basename: 'settings.yaml' },
    { basename: 'pnpm-workspace.yaml' },
    { basename: 'AGENTS.md' },
    { basename: 'CLAUDE.md' },
    { basename: '.npmrc' },
    // package.json 只在 DSH 自己的 profile 目录下才算"全局"——
    // 这个路径片段属于适配器，不属于协议。
    { basename: 'package.json', pathIncludes: '/profiles/' },
  ],
}

// S9 的停止词表与判定在 ./core.mjs（isStopMessage / STOP_TOKENS / evaluateUserTurn）——
// 纯判定属于核心，适配器不重写它。
const ledger = createLedger()
let seq = 0

/* ------------------------------------------------------------------ *
 * 2. 落盘：拦截日志 + 启动自诊断
 * ------------------------------------------------------------------ */

function appendLine(path, record) {
  try {
    mkdirSync(dirname(path), { recursive: true })
    appendFileSync(path, JSON.stringify(record) + '\n', 'utf8')
    return null
  } catch (error) {
    return String(error && error.message ? error.message : error)
  }
}

const persist = (record) => appendLine(LOG_PATH, record)
const bootRecord = (record) => appendLine(BOOT_PATH, record)

/** 记一次拦截，返回落盘错误（或 null）。两个缝共用。 */
function recordBlock(signal, tool, target, reason, detail) {
  seq += 1
  return persist({
    seq,
    at: Date.now(),
    signal,
    tool: String(tool === undefined || tool === null ? '' : tool),
    target: String(target === undefined ? '' : target),
    reason,
    detail: detail === undefined ? null : detail,
  })
}

/* ------------------------------------------------------------------ *
 * 3. 辅助：从 UserMessage 取文本（只读叶子字段，不碰 live 对象）
 * ------------------------------------------------------------------ */

function messageText(message) {
  if (message === undefined || message === null) return ''
  if (!Array.isArray(message.content)) return ''
  let out = ''
  for (const block of message.content) {
    if (block !== null && typeof block === 'object' && typeof block.text === 'string') {
      out += ' ' + block.text
    }
  }
  return out.trim()
}

/* ------------------------------------------------------------------ *
 * 4. 技能文本（Tier C 提示协议）
 * ------------------------------------------------------------------ */

const SKILL_CONTENT = [
  '# AI-Drift-Guard — DSH 版',
  '',
  'Q博士 原创（Cosmos.ai 公开库）。本版为 DSH 适配器：判定逻辑来自可移植核心，本文件只负责接线。',
  '',
  '## 三层：规则的强度取决于它挂在哪个缝上',
  '',
  '一条规则能有多硬，**不取决于它写得多好，取决于它能挂在 agent loop 的哪个接缝上**。',
  '',
  '| Tier | 机制 | 保证 | 本版覆盖 |',
  '|:--|:--|:--|:--|',
  '| **A 硬拦截** | tools/pre-execute deny、agent/pre-step reject | 动作**不会发生** | S5、S4、S9 |',
  '| **B 确定性注入** | agent/pre-step enter、tools/post-execute additionalContexts | 提醒**必然在场** | 未实现（见下） |',
  '| **C 纯提示** | 只在技能文本里 | 读不读、用不用全看模型 | S1 S2 S3 S6 S7 S8 S10 |',
  '',
  '**不要声称 Tier C 被保证了。** 它们是提醒，不是中断。',
  '',
  '## 被强制的信号（Tier A）',
  '',
  '**S5 — 模板占位符泄漏**。写入或编辑 .html/.htm 时，内容中若存在未替换的占位符（如 {title}、{标题}），写入会被直接拒绝并列出具体行号。判定表与忽略列表与公开库 references/drift-guard-core.mjs 一致。',
  '',
  '**S4 — 改全局规则文件前先做关联扫描**。cordis.yml、cordis.patch.yml、settings.yaml、pnpm-workspace.yaml、.npmrc、AGENTS.md、CLAUDE.md，以及 DSH profile 内的 package.json，在未记录关联扫描前会被拒绝。解除方式：先对该文件名执行一次 grep 或 glob。',
  '',
  '**S9 — 说停就停**。用户消息**精确等于**停止词（停/停止/stop/…）时，该步被 reject，模型根本不生成——**真的零输出**。这是提示词永远做不到的一层。',
  '',
  '## 本版未实现 Tier B，以及为什么',
  '',
  'S1/S2/S3/S6/S7/S8/S10 目前仍是 Tier C。其中 S3、S7 **有意不做**：DSH 自带沙箱与审批策略，再加一层只是重复平台能力、并且扩大误报面——**误报的代价高于漏报**。',
  '',
  'S3/S7 另一个理由是触发谓词不可判定（"模型与任务匹配""他确认的是什么"是判断，不是可观测量的全函数），硬做只会制造误伤。',
  '',
  '## 能力边界（必须如实告知用户）',
  '',
  '- Tier A 只覆盖能被工具调用或用户消息观测到的机械模式。拦不住模型推理，拦不住已开始执行的工具，也覆盖不了客户端的停止按钮。',
  '- Tier C 不是系统钩子。它们只是提醒。',
  '- 想要 S10/S8 一类的硬保证，应当用平台的 **plan mode / 只读模式** 与 **todo 门禁**，而不是本技能。',
  '',
  '每次拦截都会写入 $DSH_HOME/ai-drift-guard/blocks.jsonl；每次插件加载写入 boot.jsonl。',
  '',
  '## 出处',
  '',
  '原创：Q博士（https://github.com/Q-heart-space/Cosmos.ai）。本适配器不含判定逻辑，全部委托给同目录 core.mjs。',
].join('\n')

/* ------------------------------------------------------------------ *
 * 5. 接线
 * ------------------------------------------------------------------ */

export function apply(ctx) {
  // ---- 技能注册（inject: ['skills'] 保证 ctx.skills 存在）----
  let registered = false
  let registerError = null
  try {
    const dispose = ctx.effect(() => ctx.skills.register({
      name: 'ai-drift-guard',
      description: 'AI 跑偏守卫（DSH 版）：S5/S4/S9 由运行时强制执行，其余信号为提示协议。',
      whenToUse: '需要抑制过度工程化、格式蔓延、范围膨胀，或在生成 HTML、修改全局配置、以及用户喊停时使用。',
      source: 'runtime',
      content: SKILL_CONTENT,
    }))
    registered = typeof dispose === 'function'
  } catch (error) {
    registerError = String(error && error.message ? error.message : error)
  }

  bootRecord({
    at: Date.now(),
    event: 'apply',
    adapterVersion: ADAPTER_VERSION,
    inject: inject.join(','),
    skillsService: ctx.skills === undefined || ctx.skills === null ? 'absent' : 'present',
    skillRegistered: registered,
    registerError,
    hooks: 'tools/pre-execute, agent/pre-step',
  })

  // 反查一次：真注册进去了，就一定能按名字取回来。
  Promise.resolve()
    .then(() => ctx.skills.get('ai-drift-guard', {}))
    .then((found) => bootRecord({
      at: Date.now(),
      event: 'skill-probe',
      found: found !== undefined && found !== null,
      resolvedName: found ? found.name : null,
      source: found ? found.source : null,
    }))
    .catch((error) => bootRecord({
      at: Date.now(),
      event: 'skill-probe',
      error: String(error && error.message ? error.message : error),
    }))

  // ---- 缝3：工具门禁（S5 / S4）----
  // waterfall：返回 deny 即阻断 dispatch；否则必须调用并返回 next()。
  ctx.on('tools/pre-execute', async (exec, next) => {
    let decision
    try {
      decision = evaluate(exec, ledger, DSH_CONFIG)
    } catch (error) {
      console.error('ai-drift-guard evaluate error: ' + String(error && error.message ? error.message : error))
      return next()
    }
    if (decision.kind === 'allow') return next()

    const logError = recordBlock(
      decision.signal,
      exec.name,
      decision.target,
      decision.signal === 'S5' ? 'leaked template placeholders' : 'global rule file without a dependent scan',
      decision.detail,
    )
    const suffix = logError === null ? '' : '\n[log unavailable: ' + logError + ']'
    return { kind: 'deny', reason: decision.reason + suffix }
  })

  // ---- 缝2：S9 说停就停 ----
  // 用户消息精确等于停止词 → reject 该步 → 模型不生成 → 零输出。
  ctx.on('agent/pre-step', async (payload, next) => {
    try {
      const messages = payload === undefined || payload === null ? [] : payload.messages
      if (Array.isArray(messages) && messages.length > 0) {
        const text = messageText(messages[messages.length - 1])
        if (isStopMessage(text)) {
          recordBlock('S9', 'agent/pre-step', '', 'user asked to stop', [text.slice(0, 40)])
          return { kind: 'reject' }
        }
      }
    } catch (error) {
      console.error('ai-drift-guard pre-step error: ' + String(error && error.message ? error.message : error))
    }
    return next()
  })
}
