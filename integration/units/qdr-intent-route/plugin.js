// Q博士 意图识别 DSH 插件（订阅 user/message 事件 → ledger_userprompt_hook 意图识别+写证据）
// 官方机制：DSH = 一切皆插件（Cordis）·会话事件流订阅 user/message（用户提示词）
// 版本：v1.3 | 2026-09-21 | 🛑 **载荷保真修复：内容块数组被 JSON 序列化 ⇒ 路由收到 JSON 而非人话**
//   判例（B 机重启后通电实测·**哈希级证据**）：`perceive/dsh/2026-09-21/n_signal_intent_dsh-5f3f7f9b…json`
//   记 `prompt_length=30`、`prompt_sha256=55a30c7362f4800f6c04e675…`，而人输入的原文是 3 字的「重启了」。
//   实测 `sha256('[{"type":"text","text":"重启了"}]')` **与该 sha 逐位相同** ⇒ 送进 hook 的是
//   **内容块数组的 JSON 文本**。根因：DSH 的 `UserMessage.content` 类型是 `ContentBlock[]`
//   （`SessionEventMap['user/message']: UserMessage`），而原实现 `typeof content === 'string' ? content : JSON.stringify(content)`
//   ⇒ **永远走 stringify**。影响：①路由拿到 JSON 不是散文 ⇒ 带 `^…$` 锚点的判据（如 `QUAD_RULES.Q1` 的第二条）
//   **永不命中**·`prompt_length` 虚高（3→30）⇒ 长度类门禁失真 ②台账 `prompt_sha256`/`route_input_sha256`
//   记的是 JSON 的哈希 ⇒ **与会话原文无法对账**（本轮第一次哈希比对正是因此失败）。
//   🔑 教训：**"事件落了" ≠ "数据对"**——接线验收必须做到字段级/哈希级，不能只看"有记录"。
//   修法：`promptText()` 从 `{type:'text', text}` 块抽纯文本（块形状由上述哈希比对反证）。
// 版本：v1.2 | 2026-09-19 | 宿主绑定债根治：仓库根改 env 解析（原写死 A 机盘符路径）
//   判例（DSH 宿主执行窗口·递归闭环修复）：原实现把 `<工作空间根>` 写死在 spawn 的脚本路径与
//   cwd 上 ⇒ **本插件只在 A 机可用**；B 机（治理者根 = `<本库根>`）会 spawn 一个不存在的
//   脚本（且因 detached + stdio ignore，失败只会在 error 回调里留一行 warn）。本分支（host-adapters）
//   的存在意义正是消除此类宿主绑定，故改为 env 解析，解析顺序与 `scripts/host_paths.py` 同源：
//       `QDR_ROOT`（canonical）→ `QDR_HOME`（旧名·向后兼容）→ 皆无则 **fail-visible 跳过**
//   🛑 不猜路径：宁可留一条 warn 也不静默 spawn 错路径（与 host_paths v1.6「命中后校验存在性并
//   fail-visible 告警」同构）。A 机行为不变（实测 QDR_ROOT=<工作空间根> 已在进程 env 中）。
// 版本：v1.1 | 2026-09-13 | P0-1 修复：只路由人类提示词
//   判据与 DSH 自带 isUserMessage 同构（app.asar 实证：event.type === "user/message" && event.data.source.kind === "user"）。
//   旧版仅判 event.type，导致 harness 注入的 user-role 块也被路由入库：2026-09-13 实证一批 4 事件中
//   3 条为注入块（审批注记 103 / 运行时上下文 421 / 技能清单 11510），仅 1 条为人类原文（124·sha 精确匹配），
//   使「覆盖率 / 未覆盖(UNHANDLED)」指标被稀释。现按官方语义 fail-closed：非人类提示词一律不路由。
import { spawn } from 'node:child_process'
import { existsSync } from 'node:fs'
import { join } from 'node:path'

export const name = 'qdr-intent-route'
export const inject = ['sessions']

/** 与 DSH 官方 isUserMessage 同构：只有 source.kind === 'user' 才是人类提示词。 */
export function isHumanPrompt(event) {
  return event?.type === 'user/message' && event?.data?.source?.kind === 'user'
}

/** user/message 但缺 source 字段——无法判定是否人类，fail-closed 跳过并留痕（不静默丢弃）。 */
export function isUnattributableUserMessage(event) {
  return event?.type === 'user/message' && !event?.data?.source
}

/**
 * 🆕 v1.3：从 DSH 内容块数组抽**纯文本**（`UserMessage.content: ContentBlock[]`）。
 *
 * 判例见文件头 v1.3：原实现 stringify 整块数组 ⇒ 路由收到 JSON·哈希与原文不可对账。
 * 块形状 `{type:'text', text: string}` 由哈希级比对反证（`sha256('[{"type":"text","text":"重启了"}]')`
 * 与台账记录的 prompt_sha256 逐位相同）。非文本块（图片/文件/工具结果）不参与路由——
 * 它们不是"人类散文"，路由无依据；无文本块时返回空串（调用方按空处理·不兜底成 JSON）。
 */
export function promptText(content) {
  if (typeof content === 'string') return content
  if (Array.isArray(content)) {
    return content
      .filter((b) => b && b.type === 'text' && typeof b.text === 'string')
      .map((b) => b.text)
      .join('\n')
  }
  return ''
}

/** 构造 hook 入参；附 source_kind 供 Q博士 侧私有证据回溯（注入块不会到达此处）。 */
export function buildHookJson(event, session) {
  const data = event?.data || {}
  const prompt = promptText(data.content)
  return JSON.stringify({
    hook_event_name: 'UserPromptSubmit',
    prompt: prompt,
    session_id: session?.id || '',
    turn_id: event?.turn || event?.seq || '',
    source_kind: String(data?.source?.kind || '')
  })
}

/**
 * 解析 Q博士 仓库根（宿主无关·**禁盘符绝对路径**）。
 *
 * 判例（2026-09-19 DSH 宿主执行窗口）：原实现写死 `<工作空间根>` ⇒ 本插件只在 A 机可用。
 * 解析顺序与 `scripts/host_paths.py` / `dsh/qdr_wrapper.py` 同源：`QDR_ROOT` → `QDR_HOME`（旧名）。
 * 两者皆无 ⇒ 返回空串，由调用方 **fail-visible 跳过**（不猜路径·不静默 spawn 错路径）。
 */
export function resolveQdrRoot(env = process.env) {
  return env?.QDR_ROOT || env?.QDR_HOME || ''
}

export function apply(ctx) {
  ctx.on('session/event', (session, event) => {
    // P0-1：注入的 user-role 消息（环境/技能/注记）不路由，避免污染覆盖率与账本约束
    if (isUnattributableUserMessage(event)) {
      ctx.logger?.warn?.('qdr-intent-route: user/message 无 source 字段·fail-closed 跳过')
      return
    }
    if (!isHumanPrompt(event)) return
    const hookJson = buildHookJson(event, session)
    const parsed = JSON.parse(hookJson)
    if (!parsed.prompt || !parsed.prompt.trim()) return
    // 调 ledger_userprompt_hook（意图识别 + 写证据·host=dsh = **触发本 hook 的运行时宿主**
    // —— 与 `ledger_userprompt_hook.py` 的 `--host` 语义一致（perception/<host>/ 落位）·
    // 非「本机 canonical_writer」（那是 QDR_HOST·A 机=workbuddy），两者勿混）
    const root = resolveQdrRoot()
    if (!root) {
      ctx.logger?.warn?.('qdr-intent-route: 未设 QDR_ROOT/QDR_HOME·fail-closed 跳过（不猜路径）')
      return
    }
    const hookScript = join(root, 'scripts', 'ledger_userprompt_hook.py')
    if (!existsSync(hookScript)) {
      ctx.logger?.warn?.('qdr-intent-route: hook 脚本不存在·fail-closed 跳过: ' + hookScript)
      return
    }
    const child = spawn('python', [hookScript, '--host', 'dsh'], {
      cwd: root, stdio: ['pipe', 'ignore', 'ignore'], detached: true
    })
    child.stdin.write(hookJson)
    child.stdin.end()
    child.on('error', (err) => {
      // 失败留痕（可观测·非静默吞异常）
      ctx.logger?.warn?.('qdr-intent-route hook spawn failed: ' + (err?.message || String(err)))
    })
    child.unref()
  })
}
