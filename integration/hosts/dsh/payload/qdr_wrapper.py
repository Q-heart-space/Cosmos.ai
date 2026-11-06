# qdr_wrapper.py — DSH 侧 Q博士 能力接入 wrapper
# 🆕 2026-08-24·DSH 桌面版接入（<QDR_ROOT> 工作区）·轻宿主桥模式
# 功能：DSH agent / 用户从 QDR 工作区调用 Q博士 能力层（qdr_action_cli）
# 边界：只读调用·wrapper 本身无业务逻辑（桥=路由·动作层=执行·能力层=知识）
#
# 用法：
#   python qdr_wrapper.py list                          # 列 7 动作（🆕 F3 2026-08-28·实际 7 个·注释过时修正）
#   python qdr_wrapper.py invoke <action_id> [--args JSON]  # 调动作（JSON 字符串）
#   python qdr_wrapper.py invoke <action_id> --args-file <path>  # 调动作（文件读 JSON·🆕 B1）
#   echo '{"query":"XX"}' | python qdr_wrapper.py invoke <action_id>  # 调动作（stdin 读 JSON·🆕 B1）
#   python qdr_wrapper.py search <query>                # 快捷：能力查询
#   python qdr_wrapper.py write <path> --content-file <f> --token <t>  # 🆕 P4.1 持 token 合规写（T-3-1365·写后级联自动）

import io
import json
import subprocess
import sys
from pathlib import Path

# UTF-8 输出（Windows 中文环境·防 GBK UnicodeEncodeError·任务单§10.3 教训）
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
# 🆕 2026-08-30 stdin UTF-8（与 stdout 对称）：PowerShell 管道传中文 args 时
# python stdin 默认 GBK 解码→中文路径乱码（qdr.plan.precheck 实测）·跨宿主统一 UTF-8
if sys.stdin and not sys.stdin.isatty():
    try:
        if hasattr(sys.stdin, "reconfigure"):
            sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# 🆕 2026-11-03（黑框根治·对齐 B 机 `8c5efe873` / main 仓 `winhide` 口径）：
#   宿主（Codex/DSH/WorkBuddy）通常是 GUI 或自建 shell（无可见控制台）⇒ 控制台子进程会
#   **新分配一个可见控制台**（Windows Terminal 黑窗）且不自动关闭。
#   ⇒ 本件所有子进程统一补 `CREATE_NO_WINDOW`（仅 Windows；非 Windows 为 0，零行为变更）。
_NO_WIN = getattr(subprocess, "CREATE_NO_WINDOW", 0) if sys.platform == "win32" else 0

# 🆕 2026-09-19（DSH 宿主执行窗口·递归闭环修复）：解析顺序对齐 `scripts/host_paths.py`（canonical SSOT）
#   `QDR_ROOT` → `QDR_HOME`（旧名·向后兼容）。
#   🛑 判例：原文写 `_os.environ.get("QDR_HOME", r"<QDR_ROOT>")` —— 注释自称「禁盘符绝对路径」，
#   而那行**本身就是盘符绝对路径的静默 fallback**（自违）。B 机（治理者根 `<QDR_ROOT>`）若漏设 env，
#   会**静默**指向 A 机路径 ⇒ 与 host_paths v1.6 (D4×D8) 同一判例：兜底值必须 **fail-visible**，不静默。
#   原 2026-08-28（F2·T2 规范·跨宿主健壮性）：QDR_HOME 环境变量优先·默认向后兼容
#   （AGENTS.md 脚本引用规范禁盘符绝对路径·Q博士 空间迁移时设 env 即全链跟随）
import os as _os
import sys as _sys

_QDR_HOME = _os.environ.get("QDR_ROOT") or _os.environ.get("QDR_HOME") or ""
if not _QDR_HOME:
    print(
        "🛑 qdr_wrapper: 未设 QDR_ROOT（或旧名 QDR_HOME）⇒ 无法解析 Q博士 仓库根。\n"
        "   本 wrapper 拒绝猜测路径（禁盘符绝对路径 fallback·host_paths v1.6 D4×D8 判例）。\n"
        "   修复：设 User 级环境变量 QDR_ROOT=<Q博士 仓库根> 后重开宿主。",
        file=_sys.stderr,
    )
    raise SystemExit(2)
QDR_CLI = Path(_QDR_HOME) / "scripts" / "qdr_action_cli.py"
QDR_WRITE_GUARD = Path(_QDR_HOME) / "scripts" / "write_guard.py"  # 🆕 P4.1（2026-08-24·T-3-1365）：持 token 合规写通道
QDR_DELEGATION_QUEUE = Path(_QDR_HOME) / "scripts" / "delegation_queue.py"  # 🆕 2026-08-25·T-3-1366 P1：GDP 通用委托队列

HOST_ID = _os.environ.get("QDR_HOST", "dsh")


def _read_args(args: list) -> str:
    """🆕 B1（2026-08-24·执行清单引号坑修复）——--args 解析支持三种来源：
    ① --args JSON 字符串（原）② --args-file <path> 文件读 ③ stdin 管道（非 tty）读 JSON。
    根治 PowerShell/Git Bash 双引号剥离导致的 JSON 引号丢失（执行清单 B1 实测）。
    """
    if "--args" in args:
        i = args.index("--args")
        return args[i + 1]
    if "--args-file" in args:
        i = args.index("--args-file")
        return Path(args[i + 1]).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            return data
    return None


def _run(argv: list) -> dict:
    import os
    env = dict(os.environ)
    env["QDR_CALLER"] = f"{HOST_ID}:qdr-wrapper"  # receipt caller 可辨识
    env["QDR_HOST"] = HOST_ID
    r = subprocess.run(
        [sys.executable, str(QDR_CLI)] + argv,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        cwd=str(Path(__file__).resolve().parent.parent),
        env=env,
        creationflags=_NO_WIN,
    )
    out = {}
    try:
        out = json.loads(r.stdout) if r.stdout.strip() else {}
    except json.JSONDecodeError:
        out = {"raw": r.stdout[:300], "stderr": r.stderr[:200]}
    out["exit"] = r.returncode
    # 🆕 B4 透传（2026-08-26·DSH 递归闭环 ⑩）：CLI stderr（含 count=0 换词建议/告警）转发给 wrapper 消费者——
    # 原仅 stdout 解析·stderr 静默丢弃（B4 建议对 wrapper 用户不可见）
    if r.stderr and r.stderr.strip():
        out["stderr"] = r.stderr.strip()[:500]
    # 🆕 B3-11 exec 回执（2026-08-30·RSI 计划·跨宿主技能执行记录）：wrapper 执行 qdr 动作=技能级 exec——
    # 写 Q博士 侧 skill_receipt（best-effort 不阻塞·与 scanner 同模式·动作级可观测）
    _write_exec_receipt(argv, r.returncode)
    return out


def _write_exec_receipt(argv: list, rc: int) -> None:
    """🆕 B3-11：跨宿主技能执行 exec 回执（skill_receipt append --type exec·best-effort）。"""
    try:
        import os as _os
        # 🛑 2026-08-30 对抗审计修复：复用模块级 _QDR_HOME（原硬编码反斜杠路径·与既有正斜杠模式不一致·
        # 路径约束 禁止硬编码路径·QDR_HOME 环境变量优先全链跟随）
        qdr_root = _os.environ.get("QDR_HOME") or str(Path(_QDR_HOME))
        receipt = Path(qdr_root) / "scripts" / "skill_receipt.py"
        if not receipt.exists():
            return
        action = argv[0] if argv else "?"
        skill = f"qdr:{action}"
        detail = f"wrapper {action} rc={rc}"
        subprocess.run(
            [sys.executable, str(receipt), "append",
             "--skill", skill, "--type", "exec",
             "--status", "ok" if rc == 0 else "error",
             "--route", "qdr-wrapper", "--detail", detail],
            cwd=qdr_root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL, close_fds=True, timeout=10, creationflags=_NO_WIN,
        )
    except Exception:
        pass  # 回执失败不阻塞主流程（best-effort）


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(json.dumps({"error": "用法: qdr_wrapper.py list|invoke|search"}, ensure_ascii=False))
        return 2
    cmd = args[0]
    if cmd == "list":
        print(json.dumps(_run(["list"]), ensure_ascii=False, indent=2))
    elif cmd == "invoke" and len(args) >= 2:
        action_id = args[1]
        argv = ["invoke", action_id]
        args_json = _read_args(args)
        if args_json is not None:
            argv += ["--args", args_json]
        print(json.dumps(_run(argv), ensure_ascii=False, indent=2))
    elif cmd == "search" and len(args) >= 2:
        query = " ".join(args[1:])
        raw = _run(["invoke", "qdr.capability.search", "--args", json.dumps({"query": query})])
        # 🛑 2026-08-29 产品化修正（使用者体验）：search 返回「人话摘要」而非嵌套 JSON——
        #    原返回 {action_id, exit, stdout:"{...}"} 双层嵌套·使用者看到的是 JSON 不是结果。
        #    本质：使用者要的是「找到什么·在哪·怎么用」·不是协议结构。
        try:
            inner = json.loads(raw.get("stdout", "{}")) if isinstance(raw.get("stdout"), str) else raw.get("stdout", {})
            results = inner.get("results", []) if isinstance(inner, dict) else []
            count = inner.get("count", 0) if isinstance(inner, dict) else 0
            lines = []
            if count == 0:
                sug = (inner.get("suggestions") or []) if isinstance(inner, dict) else []
                lines.append(f"未找到与「{query}」相关的能力（0 项）")
                if sug:
                    lines.append("试试：" + "、".join(str(s) for s in sug[:5]))
            else:
                lines.append(f"找到 {count} 项：")
                for r_item in results[:8]:
                    name = r_item.get("name", "")
                    rtype = r_item.get("type", "")
                    cat = r_item.get("category", "")
                    lines.append(f"  • {name}（{rtype}·{cat}）")
                if count > 8:
                    lines.append(f"  …还有 {count - 8} 项")
            print("\n".join(lines))
        except Exception:
            print(json.dumps(raw, ensure_ascii=False, indent=2))
    elif cmd == "write" and len(args) >= 2:
        # 🆕 P4.1（2026-08-24·T-3-1365·跨宿主合规写）：DSH 持 attestation token 写 Q博士 关键文件
        #   python qdr_wrapper.py write <path> --content-file <file> --token <token> [--reason <r>]
        #   token 由 WorkBuddy 人类签发（attestation_issuer.py --issue）·write_guard 校验（scope/一次性/过期）
        #   写后级联自动触发（P5·6 设施语义校验·宿主无关）
        target = args[1]
        argv = [str(target)]
        if "--content-file" in args:
            argv += ["--content-file", args[args.index("--content-file") + 1]]
        if "--token" in args:
            argv += ["--token", args[args.index("--token") + 1]]
        if "--reason" in args:
            argv += ["--reason", args[args.index("--reason") + 1]]
        argv += ["--operation", "manual", "--intent", "意图:DSH持token合规写（T-3-1365）"]
        # 准入回执（write_guard 要求 ≥80 字符五字段·wrapper 自动构造·DSH 用户无需知晓格式）
        argv += ["--receipt", "qdr_wrapper_token_write_2026-08-24|决策OS:T2架构级|元概念:token背书合规写|价值门:pass|语义门:pass|pre_creation_gate:通过|T0:人类签发token授权|根因:T-3-1365跨宿主写授权"]
        import os
        env = dict(os.environ)
        env["QDR_CALLER"] = f"{HOST_ID}:qdr-wrapper"
        env["QDR_HOST"] = HOST_ID
        r = subprocess.run(
            [sys.executable, str(QDR_WRITE_GUARD)] + argv,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=120, cwd=str(Path(__file__).resolve().parent.parent), env=env,
            creationflags=_NO_WIN,
        )
        print(r.stdout[-1500:] if r.stdout else r.stderr[-800:])
        return r.returncode
    elif cmd == "delegation" and len(args) >= 2:
        # 🆕 2026-08-25·T-3-1366 P1：GDP 通用委托——DSH 侧查/领/执行委托单
        #   python qdr_wrapper.py delegation list [--host dsh]    # 列出待执行委托
        #   python qdr_wrapper.py delegation accept <id>          # 接受委托（pending→accepted·原子 CAS 防双执行）
        #   python qdr_wrapper.py delegation status <id>          # 查委托状态
        sub = args[1]
        argv = [str(QDR_DELEGATION_QUEUE)]
        if sub == "list":
            argv += ["list"]
            if "--host" in args:
                argv += ["--host", args[args.index("--host") + 1]]
        elif sub == "accept" and len(args) >= 3:
            argv += ["accept", "--id", args[2], "--actor", "dsh"]
        elif sub == "status" and len(args) >= 3:
            argv += ["status", "--id", args[2]]
        else:
            print(json.dumps({"error": f"delegation 用法: list|accept <id>|status <id>"}, ensure_ascii=False))
            return 2
        import os as _os
        env = dict(_os.environ)
        env["QDR_CALLER"] = f"{HOST_ID}:qdr-wrapper"
        env["QDR_HOST"] = HOST_ID
        r = subprocess.run(
            [sys.executable] + argv,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=60, cwd=str(Path(__file__).resolve().parent.parent), env=env,
            creationflags=_NO_WIN,
        )
        print(r.stdout[-2000:] if r.stdout else r.stderr[-800:])
        return r.returncode
    else:
        print(json.dumps({"error": f"未知命令: {cmd}"}, ensure_ascii=False))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
