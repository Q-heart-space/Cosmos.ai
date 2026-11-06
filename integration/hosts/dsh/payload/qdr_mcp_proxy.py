#!/usr/bin/env python3
# > **版本**：v1.1 | **类型**：🔌 | **日期**：2026-11-06 | **状态**：活跃
# > **职责**：DSH 宿主薄适配器；共享实现由自举器派生到本目录 common/qdr_mcp_host_proxy.py
# > **边界**：只注入 DSH 宿主身份与绑定收据，不复制 QDR 业务逻辑或权限判定。
"""DSH launcher for the shared, parameterized QDR MCP proxy.

DSH's official MCP client starts this launcher as a stdio server.  Keeping the
identity setup here makes the DSH descriptor data-driven while the protocol
and receipt rules remain in the one shared proxy implementation.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

COMMON = Path(__file__).resolve().parent / "common"
if str(COMMON) not in sys.path:
    sys.path.insert(0, str(COMMON))

from qdr_mcp_host_proxy import QDRHostProxy  # noqa: E402


class DSHProxy(QDRHostProxy):
    """Thin DSH identity configuration only; protocol logic is shared."""

    def __init__(self, root: str | None = None) -> None:
        os.environ.setdefault("QDR_HOST_ID", "dsh")
        # 🆕 2026-10-14（B机 r14·**去硬编码地雷**）：原默认值为**旧变体键** `dsh_qdr`。
        #   🎯 契约按判据归一到规范键后，变体键在 `host_support` 中**已不存在** ⇒ 若调用方
        #   **未传** `QDR_MCP_HOST_KEY`（如宿主未按 profile 传 env、或被其它入口直调），
        #   代理会**静默退回旧键 ⇒ 投影 0 个工具**（实测：`dsh_qdr` ⇒ `tools/list = 0`；
        #   `DeepSeek Harness` ⇒ **25**）——**静默失效**，且极难归因。
        #   ⇒ 默认值改为**规范键**（与 profile `cordis.patch.yml` 的 env 一致）；
        #   🛑 理想解＝从宿主声明的 profile/env 解析（本文件不作第二真相源），故此处仅消除地雷，
        #   并保留「env 优先」语义（`setdefault` 不覆盖调用方显式值）。
        os.environ.setdefault("QDR_MCP_HOST_KEY", "DeepSeek Harness")
        os.environ.setdefault("QDR_MCP_CLIENT_NAME", "DSH")
        os.environ.setdefault("QDR_HOST_ADAPTER_ISSUER", "dsh-mcp-adapter")
        os.environ.setdefault("QDR_CALLER", "dsh:mcp")
        super().__init__(root=root)


def self_test() -> int:
    saved = {key: os.environ.get(key) for key in (
        "QDR_HOST_ID", "QDR_MCP_HOST_KEY", "QDR_MCP_CLIENT_NAME",
        "QDR_HOST_ADAPTER_ISSUER", "QDR_CALLER")}
    try:
        os.environ.update({
            # 🆕 2026-10-14（B机 r14）：夹具键同为**旧变体键** ⇒ 亦归一到规范键（自检只断言
            #   身份/回执形状·不含工具数 ⇒ 改键不破坏断言；此处同步防"夹具测的是旧键"）。
            "QDR_HOST_ID": "dsh", "QDR_MCP_HOST_KEY": "DeepSeek Harness",
            "QDR_MCP_CLIENT_NAME": "DSH",
            "QDR_HOST_ADAPTER_ISSUER": "dsh-mcp-adapter",
            "QDR_CALLER": "dsh:mcp",
        })
        proxy = DSHProxy(root=os.getcwd())
        init = proxy._prepare({"method": "initialize", "params": {
            "protocolVersion": "2024-11-05", "clientInfo": {"name": "fixture"}}})
        call = proxy._prepare({"method": "tools/call", "params": {
            "name": "qdr.status", "arguments": {"trace_id": "fixture-trace"}}})
        receipt = call["params"]["_meta"]["qdr_host_session_binding"]
        ok = (init["params"]["clientInfo"]["name"] == "DSH"
              and receipt["host_id"] == "dsh"
              and receipt["issuer"] == "dsh-mcp-adapter"
              and receipt["decision_trace_id"] == "fixture-trace"
              and receipt["mcp_session_id"] == "")
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    print('{"self_test":"%s","assertions":["shared proxy","DSH identity","receipt shape","trace correlation"]}'
          % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="DSH QDR MCP stdio 薄适配器")
    parser.add_argument("--self-test", action="store_true", help="运行纯内存自检")
    args = parser.parse_args()
    if args.self_test:
        raise SystemExit(self_test())
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    raise SystemExit(DSHProxy().run())
