#!/usr/bin/env python3
# > **版本**：v1.2 | **类型**：🔌 | **日期**：2026-10-17 | **状态**：活跃
# > **职责**：跨宿主 QDR MCP stdio 适配器（协议转发 + 参数化绑定收据注入）
# > **边界**：不实现 Q博士业务逻辑、不签发加密身份凭证、不扩大工具/授权面。
# > **变更**：v1.1→v1.2（DSH 宿主会话绑定验证闭环）：tools/call 注入稳定会话句柄
# >   `session_id`，使 `call_context_state=CALL_CONTEXT_BOUND`（仅回执关联·非宿主身份）。
# > **变更**：v1.0→v1.1 🆕 2026-10-12（跨宿主 **JSON-RPC 通知被当成请求 ⇒ 整条桥永久卡死**）——`exchange()` 对**每一条**输入都无条件 `child.stdout.readline()` 等回包；而 `notifications/initialized` 按 MCP 规范**没有回包** ⇒ 单线程主循环卡在 readline，**宿主后续请求再不进子进程**。官方 DSH 侧表现为 `mcp-client(qdr): connection attempt failed: SdkError: Request timed out`（SDK `DEFAULT_REQUEST_TIMEOUT_MSEC=6e4`）⇒ `connectedAt` 永不置位 ⇒ 之后每次资源/工具调用报 `mcp-client(qdr): server is disconnected`。**通知 → 只转发不回读**；请求 → 跳过服务端主动消息直到 `id` 匹配。同一缺陷**同时影响 DSH／WorkBuddy／Hermes 三宿主**（三者的 MCP 客户端都会发该通知）。
# > **被依赖**：dsh/qdr_mcp_proxy.py · workbuddy/qdr_mcp_proxy.py · hermes/qdr_mcp_proxy.py（三件薄适配器只提供身份，协议面唯一实现在此）。
"""Shared MCP stdio host adapter.

Every host-specific launcher supplies identity through environment variables;
the forwarding and receipt rules stay in this one implementation.  The QDR
server remains the only business/action implementation and independently
cross-checks the receipt against the live process ancestry.
"""

from __future__ import annotations

import argparse
import copy
import datetime as _dt
import json
import os
import subprocess
import sys
import uuid
from typing import Any

# 🆕 2026-11-03（黑框根治·对齐 B 机 `8c5efe873` / main 仓 `winhide` 口径）：宿主 GUI/自建 shell
#   无可见控制台 ⇒ 控制台子进程会新分配**可见**控制台（Windows Terminal 黑窗）。统一补 CREATE_NO_WINDOW。
_NO_WIN = getattr(subprocess, "CREATE_NO_WINDOW", 0) if sys.platform == "win32" else 0


MODERN_PROTOCOL = "2026-07-28"


def _utc_now() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0)


def _rfc3339(value: _dt.datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def _value(name: str, fallback: str = "") -> str:
    return str(os.environ.get(name) or fallback).strip()


def _host_id() -> str:
    raw = _value("QDR_HOST_ID") or _value("QDR_MCP_HOST_KEY", "host")
    return raw.lower().replace(" ", "-").replace("_", "-")


def _host_name() -> str:
    return _value("QDR_MCP_CLIENT_NAME") or _value("QDR_MCP_HOST_KEY", "QDR host")


def _trace_id(params: dict[str, Any]) -> str | None:
    args = params.get("arguments") if isinstance(params, dict) else None
    if not isinstance(args, dict):
        return None
    value = args.get("trace_id") or args.get("decision_trace_id")
    return str(value).strip() if value is not None and str(value).strip() else None


def _is_notification(message: Any) -> bool:
    """JSON-RPC notification ⇔ has ``method``, has **no** ``id``.

    Per the MCP/JSON-RPC contract a notification is answered with silence, so a
    forwarder must never block waiting for a reply to one.  Treating the reply
    as compulsory wedges the single-threaded stdio loop and starves every later
    host request — the exact failure that made the DSH host time out.
    """
    return (isinstance(message, dict)
            and isinstance(message.get("method"), str)
            and "id" not in message)


class QDRHostProxy:
    """Forward one MCP stdio stream using host configuration from env."""

    def __init__(self, root: str | None = None) -> None:
        self.root = os.path.abspath(root or _value("QDR_ROOT") or os.getcwd())
        self.host_id = _host_id()
        self.host_name = _host_name()
        self.issuer = _value(
            "QDR_HOST_ADAPTER_ISSUER", f"{self.host_id}-mcp-adapter")
        self.caller = _value("QDR_CALLER", f"{self.host_id}:mcp")
        self.child: subprocess.Popen[str] | None = None
        self.mcp_session_id: str | None = None
        self.protocol_version = "2024-11-05"
        self.host_session_id = f"{self.host_id}-session-{uuid.uuid4().hex}"

    def start(self) -> None:
        server = os.path.join(self.root, "scripts", "qdr_mcp_server.py")
        child_env = os.environ.copy()
        child_env.update({
            "QDR_ROOT": self.root,
            "QDR_HOME": self.root,
            "QDR_CALLER": self.caller,
            "QDR_MCP_HOST_KEY": _value("QDR_MCP_HOST_KEY", self.host_name),
            "QDR_HOST_ID": self.host_id,
            "QDR_HOST_ADAPTER_ISSUER": self.issuer,
            "QDR_HOST_ADAPTER": f"{self.host_id}-mcp-proxy",
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
        })
        self.child = subprocess.Popen(
            [sys.executable, server], cwd=self.root, env=child_env,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None,
            text=True, encoding="utf-8", bufsize=1, creationflags=_NO_WIN)

    def _receipt(self, *, modern: bool, trace: str | None) -> dict[str, Any]:
        issued = _utc_now()
        receipt: dict[str, Any] = {
            "host_id": self.host_id,
            "binding_state": "HOST_SESSION_VERIFIED",
            "issuer": self.issuer,
            "issued_at": _rfc3339(issued),
            "expires_at": _rfc3339(issued + _dt.timedelta(hours=1)),
            "verification_method": f"{self.host_id}_process_ancestry+adapter_proxy",
            "evidence_refs": [f"{self.host_id}_mcp_proxy"],
        }
        if trace:
            receipt["decision_trace_id"] = trace
        if modern:
            receipt.update({
                "transport_lifecycle": "modern_stateless",
                "host_session_id": self.host_session_id,
            })
        else:
            receipt.update({
                "transport_lifecycle": "legacy_initialize",
                "mcp_session_id": self.mcp_session_id or "",
            })
        return receipt

    def _prepare(self, message: dict[str, Any]) -> dict[str, Any]:
        prepared = copy.deepcopy(message)
        method = prepared.get("method")
        params = prepared.setdefault("params", {})
        if not isinstance(params, dict):
            params = {}
            prepared["params"] = params
        if method == "initialize":
            self.protocol_version = str(params.get("protocolVersion") or "2024-11-05")
            client = params.get("clientInfo") if isinstance(params.get("clientInfo"), dict) else {}
            client = dict(client)
            client["name"] = self.host_name
            client.setdefault("version", f"{self.host_id}-mcp-proxy/1.0")
            params["clientInfo"] = client
        meta = params.get("_meta") if isinstance(params.get("_meta"), dict) else {}
        modern = (str(meta.get("io.modelcontextprotocol/protocolVersion") or
                       meta.get("protocolVersion") or "").strip() == MODERN_PROTOCOL)
        if not modern and method in {"tools/call", "tools/list"}:
            modern = self.protocol_version == MODERN_PROTOCOL
        if modern:
            meta = dict(meta)
            meta["io.modelcontextprotocol/clientInfo"] = {
                "name": self.host_name,
                "version": f"{self.host_id}-mcp-proxy/1.0",
            }
        if method == "tools/call":
            meta = dict(meta)
            meta["qdr_host_session_binding"] = self._receipt(
                modern=modern, trace=_trace_id(params))
            # 🆕 v1.2：注入适配器**稳定会话句柄**（进程生命周期内不变）⇒ 服务端
            # `_call_metadata_binding` 据此置 `call_context_state=CALL_CONTEXT_BOUND`。
            # 🛑 只用于「同一 MCP session＋decision_trace_id 的回执关联」，不升级宿主
            # 身份/权限/写入授权；句柄是适配器自生成的不透明串，非宿主真实会话标识。
            meta.setdefault("session_id", self.host_session_id)
        if meta:
            params["_meta"] = meta
        return prepared

    def exchange(self, message: dict[str, Any]) -> dict[str, Any] | None:
        """Forward one message; return the server reply, or ``None`` for a notification.

        ``None`` means "the protocol owes no answer", not "the server failed" —
        callers must therefore not emit a response envelope for it.
        """
        if self.child is None:
            self.start()
        assert self.child is not None and self.child.stdin is not None and self.child.stdout is not None
        self.child.stdin.write(json.dumps(self._prepare(message), ensure_ascii=False) + "\n")
        self.child.stdin.flush()
        if _is_notification(message):
            # 🛑 Never read a reply here: the server is contractually silent and
            # this loop is single-threaded, so a read would block forever and
            # the host's next request would never reach the child.
            return None
        request_id = message.get("id")
        response: Any = None
        for _ in range(100):
            line = self.child.stdout.readline()
            if not line:
                raise RuntimeError("QDR MCP 子进程提前退出，未返回 JSON-RPC 响应")
            try:
                candidate = json.loads(line)
            except ValueError:
                continue
            if isinstance(candidate, dict) and candidate.get("id") == request_id:
                response = candidate
                break
            # Server-initiated notification or an out-of-band request: not our
            # reply, so keep reading instead of mis-correlating it.
        else:
            raise RuntimeError("QDR MCP 子进程连续 100 条响应均无匹配 id")
        if message.get("method") == "initialize" and isinstance(response, dict):
            session = ((response.get("result") or {}).get("_meta") or {}).get("qdr_mcp_session") or {}
            self.mcp_session_id = session.get("id") or self.mcp_session_id
        return response

    def run(self) -> int:
        try:
            for line in sys.stdin:
                if not line.strip():
                    continue
                message: dict[str, Any] = {}
                try:
                    message = json.loads(line)
                    response = self.exchange(message)
                    if response is None:
                        # Notification: forwarded, and by contract no reply is due.
                        continue
                    sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
                    sys.stdout.flush()
                except Exception as exc:
                    sys.stdout.write(json.dumps({
                        "jsonrpc": "2.0", "id": (message or {}).get("id"),
                        "error": {"code": -32603, "message": str(exc)},
                    }, ensure_ascii=False) + "\n")
                    sys.stdout.flush()
        finally:
            if self.child is not None and self.child.poll() is None:
                self.child.terminate()
        return 0


def self_test() -> int:
    saved = {key: os.environ.get(key) for key in (
        "QDR_HOST_ID", "QDR_MCP_HOST_KEY", "QDR_MCP_CLIENT_NAME",
        "QDR_HOST_ADAPTER_ISSUER", "QDR_CALLER")}
    try:
        os.environ.update({
            "QDR_HOST_ID": "fixture-host",
            "QDR_MCP_HOST_KEY": "Fixture Host",
            "QDR_MCP_CLIENT_NAME": "Fixture Host",
            "QDR_HOST_ADAPTER_ISSUER": "fixture-host-mcp-adapter",
            "QDR_CALLER": "fixture-host:mcp",
        })
        proxy = QDRHostProxy(root=os.getcwd())
        init = proxy._prepare({"method": "initialize", "params": {
            "protocolVersion": "2024-11-05", "clientInfo": {"name": "fixture"}}})
        call = proxy._prepare({"method": "tools/call", "params": {
            "name": "qdr.status", "arguments": {"trace_id": "fixture-trace"}}})
        receipt = call["params"]["_meta"]["qdr_host_session_binding"]
        ok = (init["params"]["clientInfo"]["name"] == "Fixture Host"
              and receipt["host_id"] == "fixture-host"
              and receipt["issuer"] == "fixture-host-mcp-adapter"
              and receipt["mcp_session_id"] == ""
              and call["params"]["_meta"].get("session_id") == proxy.host_session_id)
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    print(json.dumps({"self_test": "PASS" if ok else "FAIL",
                      "assertions": ["parameterized clientInfo", "receipt shape", "trace correlation"]},
                     ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="通用 QDR MCP stdio 宿主适配器")
    parser.add_argument("--self-test", action="store_true", help="运行纯内存自检")
    args = parser.parse_args()
    if args.self_test:
        raise SystemExit(self_test())
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    raise SystemExit(QDRHostProxy().run())
