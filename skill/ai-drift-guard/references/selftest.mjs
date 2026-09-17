/**
 * AI-Drift-Guard core self-test.
 *
 * 把 SKILL.md →「可验证性」里那几条声明变成可复现的断言。
 * 任何人都能跑，不需要任何 AI 平台：
 *
 *     node references/selftest.mjs
 *     退出码 0 = 全绿
 */

import { detectS5, evaluate, createLedger, CORE_VERSION } from './drift-guard-core.mjs'

let failed = 0

function check(label, condition, extra) {
  if (condition) {
    console.log('  PASS  ' + label)
  } else {
    failed += 1
    console.log('  FAIL  ' + label + (extra === undefined ? '' : '  :: ' + extra))
  }
}

console.log('ai-drift-guard core ' + CORE_VERSION + ' — selftest\n')

/* ---- S5: 必须抓到泄漏的占位符 ---------------------------------- */
const denyHtml = [
  '<!DOCTYPE html>',
  '<html>',
  '<head>',
  '  <title>{page_title}</title>',
  '</head>',
  '<body>',
  '  <h1>{heading}</h1>',
  '</body>',
  '</html>',
  '',
].join('\n')

const denyIssues = detectS5({ path: 'a.html', content: denyHtml })
check('S5 抓到 {page_title} 与 {heading}', denyIssues.length === 2, JSON.stringify(denyIssues))
check('S5 报出行号（首条为 line 4）', denyIssues[0] === undefined ? false : denyIssues[0].startsWith('line 4:'), denyIssues[0])
check('S5 报出原始 token', denyIssues[0] === undefined ? false : denyIssues[0].includes('{page_title}'))

/* ---- S5: 不得误报合法的 JS/CSS 花括号 -------------------------- */
const allowHtml = [
  '<canvas id="c"></canvas>',
  '<script>',
  '  const payload = {data};',
  '  const shape = {type};',
  '  const opts = { labels: ["a"], datasets: [] };',
  '</script>',
  '',
].join('\n')

const allowIssues = detectS5({ path: 'b.html', content: allowHtml })
check('S5 放行 {data} / {type}（IGNORE_KEYWORDS）', allowIssues.length === 0, JSON.stringify(allowIssues))

/* ---- S5: v1.1 修复的盲区 --------------------------------------- *
 * 含 https:// 的行不得被整行跳过，否则该行上的占位符会漏检。      */
const urlLine = '<a href="https://example.com/p">{link_text}</a>'
const urlIssues = detectS5({ path: 'c.html', content: urlLine })
check('S5 仍扫描含 https:// 的行（v1.1 修复）', urlIssues.length === 1, JSON.stringify(urlIssues))

// 回归证明：v1.0 的注释规则确实会跳过这一行（所以修复不是多余的）
const oldRuleWouldSkip = /\/\/.*$/.test(urlLine.trim())
check('（回归证明）v1.0 的 // 规则会跳过该行', oldRuleWouldSkip === true)

// 协议相对 URL 仍是已知残留盲区——如实断言，不掩盖
const protocolRelative = '<img src="//cdn.example.com/x.png">{alt_text}</img>'
check('（已知盲区）协议相对 // 仍会被跳过', detectS5({ path: 'd.html', content: protocolRelative }).length === 0)

/* ---- S4: 状态化门禁 -------------------------------------------- */
const matchers = [
  { basename: 'settings.yaml' },
  { basename: 'package.json', pathIncludes: '/profiles/' },
]
const ledger = createLedger()
const writeSettings = { name: 'write', arguments: { file_path: 'C:/proj/settings.yaml', content: 'x' } }

check('S4 拒绝未扫描的全局规则文件', evaluate(writeSettings, ledger, { globalRuleMatchers: matchers }).kind === 'deny')

// 关键：转义正则也必须能解除封锁（v1.3 用字面量 indexOf，做不到）
evaluate({ name: 'grep', arguments: { pattern: 'settings\\.yaml', path: 'C:/proj' } }, ledger, { globalRuleMatchers: matchers })
check('S4 被转义正则搜索解除（v1.3 缺陷修复）', evaluate(writeSettings, ledger, { globalRuleMatchers: matchers }).kind === 'allow')

check('S4 不误伤普通文件', evaluate({ name: 'write', arguments: { file_path: 'C:/proj/readme.md', content: 'x' } }, ledger, { globalRuleMatchers: matchers }).kind === 'allow')
check('S4 用 pathIncludes 限定 package.json', evaluate({ name: 'write', arguments: { file_path: 'C:/proj/package.json', content: 'x' } }, ledger, { globalRuleMatchers: matchers }).kind === 'allow')
check('S4 抓到 /profiles/ 下的 package.json', evaluate({ name: 'write', arguments: { file_path: 'C:/home/.dsh/profiles/desktop/package.json', content: 'x' } }, ledger, { globalRuleMatchers: matchers }).kind === 'deny')

check('非 write/edit/搜索类调用一律放行', evaluate({ name: 'pwsh', arguments: {} }, ledger, { globalRuleMatchers: matchers }).kind === 'allow')

console.log('')
if (failed === 0) {
  console.log('ALL GREEN')
} else {
  console.log(failed + ' FAILED')
}
process.exitCode = failed === 0 ? 0 : 1
