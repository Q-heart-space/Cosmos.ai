#!/usr/bin/env python3
# > **用途**：**Hermes → Q博士 台账的 payload 适配器**——把 Hermes shell hook 的 stdin JSON 翻译成
# >   `ledger_userprompt_hook.py` 认的 `UserPromptSubmit` 载荷，并把"抽不到 prompt"变成**可见**而非静默空转。
# > **盲区**：①Hermes 的 `pre_llm_call` payload **无顶层 `prompt`**（本适配器按链式抽取·抽不到则写诊断并**不**调台账）
# >   ②事件名是**平台语义**：`pre_llm_call`＝每轮用户提示词·**不是** `pre_command`（后者仅 CLI 斜杠命令）
# >   ③不读原文入库（只把原文交给台账脚本·台账自身只存 sha256 与长度）
# > **变更**：v1.0→v1.1 🛑 **合成测试载荷冒充真实用户流量（source_kind 硬编码 "user"）**（2026-09-21·B 机实测驱动·T-3-1883）——【缺口·实测】`source_kind` 原**硬编码** `"user"`，而 Hermes 自带的 `hermes hooks test` / `doctor` 经 `agent/shell_hooks.py:590 run_once()` **走生产路径**投递**合成载荷**（逐字取证 `hermes_cli/hooks.py:109,113,117,120,122,126`：`session_id="test-session"`·`task_id="test-task"`·`tool_call_id="test-call"`·内置 `user_message="What is the weather?"`）⇒ **从 wire 上看不出与真实轮的差别**，于是自测流量被记成"人类提示词"：本机 5 条 hermes 事件里 3 条即此类（prompt 恒 20 字符·sha 恒 `49c64f94c9fe5d32…`·`turn_id` 空·`identity_quality=degraded`），若据此判断"Hermes hook 已在用"＝**近似量冒充真实量**同族。【修法】新增 `_is_synthetic()`（标志**取自宿主自身实现**·非我方猜测：`test-*` 标识族 + 显式 `synthetic: true`），`source_kind` 如实落 `synthetic`/`user`；`--self-test` 补 4 例（3 真合成 + 1 反例）。【验证】实跑 `hermes hooks test pre_llm_call` → 新事件 `source_kind="synthetic"`。｜原变更：v1.0 首建（2026-09-21·B 机源码实测）——Hermes 支持 `hooks:`（39 事件·`agent/shell_hooks.py`），
# >   但 wire 为 `{hook_event_name, tool_name, tool_input, session_id, cwd, profile, extra}` ⇒ **prompt 落在 `extra`**；
# >   直连 `ledger_userprompt_hook.py` 会因 `data["prompt"]` 为空而 `return 0`＝**静默空转**（判例「事件落了 ≠ 数据对」同族）。
# >   ⇒ 本适配器：**链式抽取 + 抽不到写诊断（fail-visible）+ 幂等**。

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# 🛑 v1.0.1 修复（2026-09-21·自测当场崩）：Windows 默认控制台为 GBK ⇒ 打印 emoji/中文会
#   `UnicodeEncodeError` 直接终止进程（本仓历史同族坑·判例：mojibake/编码腐败）。Hermes 可能以
#   任意控制台编码调本适配器 ⇒ **必须自持编码**，不依赖宿主环境（对齐 qdr_action_cli 的 stdin/stdout 加固）。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DIAG = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")) / "hooks" / "_qdr_adapter_diag.jsonl"


def _text_of(v):
    """从 Hermes 的 content 形态取纯文本（字符串 / 块数组 / 嵌套）。"""
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        parts = []
        for b in v:
            if isinstance(b, str):
                parts.append(b)
            elif isinstance(b, dict):
                for k in ("text", "content", "value"):
                    if isinstance(b.get(k), str):
                        parts.append(b[k])
                        break
        return "\n".join(p for p in parts if p)
    if isinstance(v, dict):
        for k in ("text", "content", "value"):
            if isinstance(v.get(k), str):
                return v[k]
    return ""


def extract_prompt(payload):
    """链式抽取用户提示词。返回 (prompt, how)。抽不到 ⇒ ("", 原因)。

    🛑 设计纪律：**抽不到不兜底成 JSON**（那正是 DSH 插件踩过的坑：把整块数组 stringify 当成原文，
    导致路由吃 JSON、长度虚高、哈希与原文无法对账）。宁可返回空并**写诊断**。
    """
    extra = payload.get("extra") if isinstance(payload.get("extra"), dict) else {}
    # ① 顶层直给（某些事件会把 prompt 放平）
    for k in ("prompt", "user_prompt", "text", "message", "input"):
        t = _text_of(payload.get(k))
        if t.strip():
            return t, f"top:{k}"
    # ② extra 常见键
    for k in ("prompt", "user_prompt", "text", "message", "content", "input", "user_message"):
        t = _text_of(extra.get(k))
        if t.strip():
            return t, f"extra:{k}"
    # ③ messages / history：取最后一条 role=user
    for k in ("messages", "history", "transcript", "turns"):
        arr = extra.get(k)
        if isinstance(arr, list):
            for item in reversed(arr):
                if isinstance(item, dict) and str(item.get("role", "")).lower() == "user":
                    t = _text_of(item.get("content"))
                    if t.strip():
                        return t, f"extra:{k}[-1 user].content"
                t = _text_of(item)
                if t.strip():
                    return t, f"extra:{k}[-1]"
    # ④ 兜底：递归找首个"键名含 prompt/message/user"的非空字符串
    def walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                p2 = f"{path}.{k}" if path else k
                if any(t in str(k).lower() for t in ("prompt", "message", "user", "text")):
                    t = _text_of(v)
                    if t.strip():
                        return t, f"deep:{p2}"
                r = walk(v, p2)
                if r:
                    return r
        elif isinstance(o, list):
            for i, v in enumerate(o):
                r = walk(v, f"{path}[{i}]")
                if r:
                    return r
        return None
    r = walk(payload)
    if r:
        return r
    return "", "not-found(keys=%s)" % ",".join(sorted(list(payload) + list(extra))[:12])


def write_diag(rec):
    try:
        DIAG.parent.mkdir(parents=True, exist_ok=True)
        with DIAG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


# 🆕 v1.1（2026-09-21·B 机实测驱动）：合成载荷判定。
# 依据＝**宿主自身实现**，非我方猜测：`hermes_cli/hooks.py` 的测试载荷用
# `session_id="test-session"` / `task_id="test-task"` / `tool_call_id="test-call"`，
# 经 `agent/shell_hooks.py:590 run_once()` **走生产路径**投递 ⇒ wire 上与真实轮不可区分，
# 唯一可用标记就是这组 `test-*` 标识（外加显式 `synthetic: true` 的前向兼容）。
_SYNTHETIC_ID_PREFIX = "test-"


def _is_synthetic(payload):
    """Hermes 官方合成测试载荷？（`hermes hooks test` / `doctor`）"""
    for key in ("session_id", "task_id", "tool_call_id"):
        v = payload.get(key)
        if isinstance(v, str) and v.startswith(_SYNTHETIC_ID_PREFIX):
            return True
    for holder in (payload, payload.get("extra") or {}):
        if isinstance(holder, dict) and holder.get("synthetic") is True:
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description="Hermes→Q博士 台账 payload 适配器")
    ap.add_argument("--host", default="hermes")
    ap.add_argument("--ledger", default="", help="ledger_userprompt_hook.py 路径（缺省 <QDR_ROOT>/scripts/…）")
    ap.add_argument("--self-test", action="store_true")
    args, _ = ap.parse_known_args()

    root = os.environ.get("QDR_ROOT") or os.environ.get("QDR_HOME") or ""
    ledger = args.ledger or (os.path.join(root, "scripts", "ledger_userprompt_hook.py") if root else "")

    if args.self_test:
        cases = [
            ({"hook_event_name": "pre_llm_call", "extra": {"prompt": "对抗式审查"}}, "对抗式审查"),
            ({"hook_event_name": "pre_llm_call", "extra": {"messages": [{"role": "assistant", "content": "a"},
                                                                      {"role": "user", "content": "回传给Q博士"}]}}, "回传给Q博士"),
            ({"hook_event_name": "pre_llm_call", "extra": {"messages": [{"role": "user",
                                                                        "content": [{"type": "text", "text": "重启了"}]}]}}, "重启了"),
            ({"hook_event_name": "pre_llm_call", "extra": {}}, ""),
        ]
        bad = 0
        for payload, want in cases:
            got, how = extract_prompt(payload)
            ok = got == want
            bad += 0 if ok else 1
            print(("  ✅ " if ok else "  ❌ ") + f"{how:34s} → {got!r}")
        # 🆕 v1.1：合成载荷判定（宿主实现取证：hermes_cli/hooks.py 的 test-* 标识族）
        synth_cases = [
            ({"session_id": "test-session", "extra": {"prompt": "x"}}, True),
            ({"task_id": "test-task", "extra": {"prompt": "x"}}, True),
            ({"extra": {"synthetic": True, "prompt": "x"}}, True),
            ({"session_id": "sess-abc", "extra": {"prompt": "x"}}, False),   # 反例：真实会话
        ]
        for payload, want in synth_cases:
            got = _is_synthetic(payload)
            ok = got is want
            bad += 0 if ok else 1
            print(("  ✅ " if ok else "  ❌ ") + f"is_synthetic={got!s:5s}（期望 {want!s:5s}）")
        print("self_test =", "PASS" if bad == 0 else f"FAIL({bad})")
        return 0 if bad == 0 else 1

    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except Exception as e:
        write_diag({"ts": __import__("datetime").datetime.now().isoformat(), "stage": "parse",
                    "error": type(e).__name__, "raw_len": len(raw)})
        return 0
    prompt, how = extract_prompt(payload)
    if not prompt.strip():
        # 🛑 fail-visible：抽不到 ⇒ 写诊断·**不**调台账（不制造"空转但看着已接"的假象）
        write_diag({"ts": __import__("datetime").datetime.now().isoformat(), "stage": "extract",
                    "how": how, "event": payload.get("hook_event_name"),
                    "top_keys": sorted(payload), "extra_keys": sorted((payload.get("extra") or {})) if isinstance(payload.get("extra"), dict) else []})
        return 0
    out = json.dumps({
        "hook_event_name": "UserPromptSubmit",     # 台账脚本只认这个事件名
        "prompt": prompt,
        "session_id": str(payload.get("session_id") or ""),
        "turn_id": str(payload.get("turn_id") or payload.get("seq") or ""),
        # 🆕 v1.1：如实标注来源——原**硬编码** "user" ⇒ 宿主自带合成测试载荷也自称"人类提示词"
        # （近似量冒充真实量同族）。判定依据见 _is_synthetic() 的取证。
        "source_kind": "synthetic" if _is_synthetic(payload) else "user",
        "adapter": "hermes", "adapter_how": how,
    }, ensure_ascii=False)
    if not ledger or not os.path.exists(ledger):
        write_diag({"ts": __import__("datetime").datetime.now().isoformat(), "stage": "ledger",
                    "error": "ledger 脚本不可达", "ledger": ledger})
        return 0
    try:
        # 🛑 v1.0.1：子进程须**自持 UTF-8**——本适配器用 capture_output 捕获台账 stdout，
        #   而 Windows 下管道默认走 locale(GBK) ⇒ 台账打印 emoji/中文即 `UnicodeEncodeError`
        #   被吞在 stderr 里（实测判例：stage=spawn error=UnicodeEncodeError ⇒ 事件 0 条）。
        #   DSH 侧用 `stdio: ignore` 故未暴露——**同一脚本·不同调用方式即不同命运**。
        child_env = dict(os.environ)
        child_env.setdefault("PYTHONUTF8", "1")
        child_env.setdefault("PYTHONIOENCODING", "utf-8")
        p = subprocess.run([sys.executable, ledger, "--host", args.host], input=out.encode("utf-8"),
                           capture_output=True, timeout=25, env=child_env)
        if p.returncode != 0:
            write_diag({"ts": __import__("datetime").datetime.now().isoformat(), "stage": "run",
                        "rc": p.returncode, "stderr": p.stderr.decode("utf-8", "replace")[:300]})
    except Exception as e:
        write_diag({"ts": __import__("datetime").datetime.now().isoformat(), "stage": "spawn",
                    "error": type(e).__name__})
    return 0


if __name__ == "__main__":
    sys.exit(main())
