/**
 * AI-Drift-Guard — portable core (reference implementation of SKILL.md v1.4 Tier A)
 *
 * 平台中立：本文件不 import 任何 AI 平台 SDK，不假设任何宿主目录结构，
 * 也不含任何平台的私有路径。宿主差异全部通过 createGuard() 的 config 注入。
 *
 * 运行环境：Node >=18 / Deno / Bun（只用标准 ESM + node:fs）。
 *
 * 独立使用（不需要任何 AI 平台）：
 *     node drift-guard-core.mjs check path/to/page.html
 *     退出码 0 = 干净；1 = 有泄漏占位符
 *
 * 接入宿主：见 adapters.md。核心只暴露纯函数，副作用（落盘、拦截）由宿主负责。
 */

import { readFileSync } from 'node:fs'

export const CORE_VERSION = '1.4.0'

/**
 * 含 {} 但明确不是占位符的 JS/CSS 关键字。
 * 与 template_validator.py 的 IGNORE_KEYWORDS 必须保持一致。
 */
export const IGNORE_KEYWORDS = Object.freeze([
  'type', 'data', 'labels', 'datasets', 'scales', 'options',
  'plugins', 'legend', 'title', 'animation', 'indexAxis',
  'beginAtZero', 'display', 'position', 'usePointStyle',
  'boxWidth', 'pointRadius', 'fill', 'tension', 'borderColor',
  'backgroundColor', 'callbacks', 'tooltip', 'label', 'parsed',
  'stacked', 'grid', 'draw', 'responsive', 'maintainAspectRatio',
  'cutout', 'padding', 'borderWidth', 'fontSize', 'fontFamily',
  'barPercentage', 'categoryPercentage', 'spanGaps', 'stepped',
])

/** 含 {} 但不是占位符的整行模式。与 template_validator.py 保持一致。 */
export const IGNORE_PATTERNS = Object.freeze([
  /^\s*\{\d+\}\s*$/,
  /^[^:]*:\s*\{[^}]+\}$/,
])

/** Unicode 感知的占位符模式：{ 字母/数字/下划线 }。 */
export const PLACEHOLDER_PATTERN = /\{[\p{L}\p{N}_]+\}/gu

/**
 * URL 方案分隔符 `://` 的中和替换物。
 * 用控制字符，确保它既不会是 `//`，也不会影响 `{...}` 的识别。
 */
const URL_SCHEME_GUARD = ':\u0001\u0001'

/** 把 `://` 中和掉，使 URL 不会被误判为 JS 注释起始。 */
export function neutralizeUrlSchemes(text) {
  return text.split('://').join(URL_SCHEME_GUARD)
}

/**
 * 判断一整行（已 trim）是否应整行跳过。
 * 注释判定前先中和 URL 方案——这是 v1.4 修复的盲区：
 * v1.3 用 /\/\/.*$/ 直接匹配，导致任何含 `https://` 的行被整行跳过。
 */
export function isIgnorableLine(trimmed) {
  for (const pattern of IGNORE_PATTERNS) {
    if (pattern.test(trimmed)) return true
  }
  const neutral = neutralizeUrlSchemes(trimmed)
  if (/\/\/.*$/.test(neutral)) return true
  if (/\/\*.*\*\//.test(neutral)) return true
  return false
}

/**
 * S5 检测（SKILL.md A.4 的参考实现）。
 * @param {{ path?: string, content?: string }} input
 * @returns {string[]} 形如 "line 5: {x} in: <title>{x}</title>" 的发现列表；空数组表示干净。
 */
export function detectS5(input) {
  const content = input && typeof input.content === 'string' ? input.content : ''
  const issues = []
  if (content.length === 0) return issues

  const lines = content.split('\n')
  const seenLines = new Set()

  for (let index = 0; index < lines.length; index += 1) {
    const lineNo = index + 1
    const raw = lines[index]
    const trimmed = raw.trim()
    if (isIgnorableLine(trimmed)) continue

    // 每行重新绑定：全局正则的 lastIndex 在 String.match 下会被重置，这里显式重建更稳。
    const found = raw.match(PLACEHOLDER_PATTERN)
    if (found === null) continue

    for (const token of found) {
      const key = token.slice(1, -1)
      if (IGNORE_KEYWORDS.includes(key)) continue
      if (/^\d+$/.test(key)) continue
      if (seenLines.has(lineNo)) continue
      seenLines.add(lineNo)
      issues.push('line ' + lineNo + ': ' + token + ' in: ' + trimmed.slice(0, 100))
    }
  }
  return issues
}

/** S5 是否只适用于该路径。 */
export function isHtmlPath(path) {
  if (typeof path !== 'string') return false
  const lower = path.replace(/\\/g, '/').toLowerCase()
  return lower.endsWith('.html') || lower.endsWith('.htm')
}

/** basename（把反斜杠归一为斜杠）。 */
export function baseName(path) {
  if (typeof path !== 'string') return ''
  const text = path.replace(/\\/g, '/')
  const cut = text.lastIndexOf('/')
  return cut === -1 ? text : text.slice(cut + 1)
}

/**
 * 探测串：去掉反斜杠，使转义正则（cordis\.patch\.yml）与原生路径都能命中 basename。
 * v1.3 用字面量 indexOf，导致规范写法的转义正则无法解除 S4——这是本版的修复点。
 */
export function scanProbe(pattern, path) {
  const left = typeof pattern === 'string' ? pattern : ''
  const right = typeof path === 'string' ? path : ''
  return (left + ' ' + right).replace(/\\/g, '')
}

/* ------------------------------------------------------------------ *
 * S9 —— 说停就停（缝2 pre-step 里唯一可判定的部分）
 * ------------------------------------------------------------------ */

/**
 * 停止词表。**精确匹配**是这条规则误报率≈0 的全部原因。
 * 不要往里加模糊匹配或语义判断：宁可漏，不可误伤——
 * 一个会拦住正常说话的守卫，第二天就会被关掉。
 */
export const STOP_TOKENS = Object.freeze([
  '停', '停止', '打住', '别说了', '停下',
  'stop', 'stop it', 'shut up', 'halt',
])

/** 归一化：去首尾空白、折小写、去尾部标点。不改动正文。 */
export function normalizeStopCandidate(text) {
  if (typeof text !== 'string') return ''
  return text.trim().toLowerCase().replace(/[.!?。！？~\s]+$/u, '')
}

/** 用户是否在喊停。只做精确匹配。 */
export function isStopMessage(text) {
  return STOP_TOKENS.includes(normalizeStopCandidate(text))
}

/**
 * 缝2（pre-step）判定：这一步该不该被拒绝。
 * 宿主负责把最后一条用户消息的**纯文本**取出来传进来——核心不认识任何
 * 平台的 Message 结构，这是平台中立的一部分。
 *
 * @param {{ text?: string }} input
 * @returns {{ kind: 'allow' } | { kind: 'reject', signal: 'S9', reason: string }}
 */
export function evaluateUserTurn(input) {
  const text = input !== null && typeof input === 'object' && typeof input.text === 'string'
    ? input.text
    : ''
  if (isStopMessage(text)) {
    return {
      kind: 'reject',
      signal: 'S9',
      reason: 'AI-Drift-Guard S9: the user asked to stop. Reject this step so the model generates nothing — not a summary, not an acknowledgement, not an emoji.',
    }
  }
  return { kind: 'allow' }
}

/** 新建一个会话级扫描台账（SKILL.md A.2）。 */
export function createLedger() {
  return new Set()
}

/**
 * 判定一次工具调用。纯函数：除 ledger 外无状态。
 *
 * @param {{ name?: string, arguments?: object }} exec
 * @param {Set<string>} ledger
 * @param {{ searchTools?: string[], writeTools?: string[], globalRuleMatchers?: Array<object> }} [config]
 * @returns {{ kind: 'allow' } | { kind: 'deny', signal: string, reason: string, detail: string[]|null, target: string }}
 */
export function evaluate(exec, ledger, config = {}) {
  const searchTools = config.searchTools ?? ['grep', 'glob', 'search']
  const writeTools = config.writeTools ?? ['write', 'edit']
  const matchers = config.globalRuleMatchers ?? []

  if (exec === null || exec === undefined) return { kind: 'allow' }
  const toolName = exec.name
  const args = exec.arguments ?? {}

  // 第 1 步：搜索类调用登记扫描台账。
  if (searchTools.includes(toolName)) {
    const probe = scanProbe(args.pattern, args.path)
    for (const matcher of matchers) {
      if (typeof matcher.basename !== 'string') continue
      if (probe.includes(matcher.basename)) ledger.add(matcher.basename)
    }
    return { kind: 'allow' }
  }

  if (!writeTools.includes(toolName)) return { kind: 'allow' }

  const filePath = typeof args.file_path === 'string' ? args.file_path : ''

  // 第 3 步：S5
  if (isHtmlPath(filePath)) {
    const content = toolName === writeTools[0] ? args.content : args.new_string
    const issues = detectS5({ path: filePath, content })
    if (issues.length > 0) {
      const shown = issues.slice(0, 5)
      return {
        kind: 'deny',
        signal: 'S5',
        target: filePath,
        detail: shown,
        reason: 'AI-Drift-Guard S5 blocked this write: leaked template placeholder(s) in ' + filePath + '.\n'
          + shown.join('\n')
          + '\nReplace each placeholder with a real value (or drop the line), then retry. '
          + 'This guard is mechanical and blocks again until the content is clean.',
      }
    }
  }

  // 第 4 步：S4
  const matcher = matchGlobalRule(filePath, matchers)
  if (matcher !== null) {
    const base = baseName(filePath)
    if (!ledger.has(base)) {
      const dir = filePath.replace(/\\/g, '/').replace(/\/[^/]*$/, '')
      return {
        kind: 'deny',
        signal: 'S4',
        target: filePath,
        detail: [base],
        reason: 'AI-Drift-Guard S4 blocked this edit: "' + base + '" is a global rule/composition file '
          + 'and no dependent scan is recorded in this session.\n'
          + 'Scan what consumes it first, then retry. For example:\n'
          + '  search pattern="' + base + '" path="' + dir + '"\n'
          + 'That scan lifts this block.',
      }
    }
  }

  // 第 5 步
  return { kind: 'allow' }
}

/**
 * 路径是否命中宿主提供的全局规则清单（SKILL.md A.5）。
 * 匹配规则：
 *   { basename: 'cordis.yml' }                        → basename 精确相等
 *   { basename: 'package.json', pathIncludes: '/profiles/' } → 且路径包含该片段
 */
export function matchGlobalRule(path, matchers) {
  if (typeof path !== 'string' || !Array.isArray(matchers)) return null
  const normalized = path.replace(/\\/g, '/')
  const base = baseName(path)
  for (const matcher of matchers) {
    if (matcher === null || typeof matcher !== 'object') continue
    if (matcher.basename !== base) continue
    if (typeof matcher.pathIncludes === 'string' && !normalized.includes(matcher.pathIncludes)) continue
    return matcher
  }
  return null
}

/** 构造一行日志记录（SKILL.md A.6）。宿主负责写到哪里。 */
export function makeLogRecord(hit, exec, seq, at = Date.now()) {
  return {
    seq,
    at,
    signal: hit.signal,
    tool: String(exec && exec.name ? exec.name : ''),
    target: hit.target,
    reason: hit.signal === 'S5' ? 'leaked template placeholders' : 'global rule file without a dependent scan',
    detail: hit.detail ?? null,
  }
}

/* ------------------------------------------------------------------ *
 * CLI —— 不依赖任何 AI 平台，适合 pre-commit / CI
 * ------------------------------------------------------------------ */

function runCli(argv) {
  const [command, ...rest] = argv
  if (command === 'version' || command === '--version' || command === '-V') {
    console.log('ai-drift-guard core ' + CORE_VERSION)
    return 0
  }
  if (command !== 'check') {
    console.error('usage: node drift-guard-core.mjs check <file.html> [more.html ...]')
    console.error('       node drift-guard-core.mjs version')
    return 2
  }
  if (rest.length === 0) {
    console.error('check: no input files')
    return 2
  }
  let failed = false
  for (const file of rest) {
    if (!isHtmlPath(file)) {
      console.log('[SKIP] ' + file + ' (not .html/.htm)')
      continue
    }
    let content
    try {
      content = readFileSync(file, 'utf8')
    } catch (error) {
      console.error('[ERROR] ' + file + ': ' + (error && error.message ? error.message : String(error)))
      failed = true
      continue
    }
    const issues = detectS5({ path: file, content })
    if (issues.length > 0) {
      failed = true
      console.log('[FAIL] ' + file + ' — ' + issues.length + ' leaked placeholder(s):')
      for (const issue of issues) console.log('  ' + issue)
    } else {
      console.log('[PASS] ' + file)
    }
  }
  return failed ? 1 : 0
}

const invokedDirectly = typeof process !== 'undefined'
  && Array.isArray(process.argv)
  && typeof process.argv[1] === 'string'
  && process.argv[1].replace(/\\/g, '/').endsWith('drift-guard-core.mjs')

if (invokedDirectly) {
  process.exitCode = runCli(process.argv.slice(2))
}
