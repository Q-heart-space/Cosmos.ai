#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# > **用途**：**全局记忆制品生成器** —— 在**持有 L1 正本的机器**上，把宿主配置根的全局记忆件
# >   打包为 **portable 制品**（制品目录 ＋ `MANIFEST.json` 含逐件 sha16），供**无正本的机器**
# >   经制品分支检出后落位使用。
# > **盲区**：只打包 `PLATFORM_LAYOUTS` 声明件 ＋ 已知身份件名单；不校验内容语义；不做增量。

"""全局记忆制品生成器（生成端）。

骨架不依赖任何绝对路径：宿主配置根一律经 `host_paths.host_config_dir()` 运行期解析。

用法（持有 L1 正本的机器）：
  python host-adapters/global-memory/build_artifacts.py --out <制品目录> --verify

然后：把制品目录推入「制品分支」⇒ 消费机检出 ⇒ 跑
  python scripts/global_memory_install.py --check / --apply
落位到该机宿主配置根。
"""
import argparse
import hashlib
import io
import json
import os
import sys

# 🆕 2026-10-01（B机 r1537·`HO-089` 族级判据 `--scan-root` **扫到·via-var 形态**）：
#   `L113` 的 print 载荷经**变量**拼接引入 GBK 不可编码字符（🆕/⇒）⇒ 手工 grep 看不见，
#   AST 面看得见 ⇒ 补**防御式 reconfigure**（🛑 仅输出层·零判定变更）。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


_HERE = os.path.dirname(os.path.abspath(__file__))
for _cand in (os.path.join(_HERE, "..", "..", "Q博士", "scripts"),
              os.path.join(_HERE, "..", "..", "..", "scripts")):
    if os.path.isdir(_cand):
        sys.path.insert(0, os.path.abspath(_cand))
try:
    import host_paths
except Exception:  # noqa: BLE001
    host_paths = None

RC_OK, RC_P1, RC_P0, RC_UNAVAIL = 0, 1, 2, 3
LF = chr(10)
KNOWN = ("MEMORY.md", "MEMORY_RULES.md", "MEMORY_SKILLS.md",
         "IDENTITY.md", "SOUL.md", "USER.md", ".MEMORY_CHANGELOG.md")


def sha16(p):
    return hashlib.sha256(io.open(p, "rb").read()).hexdigest()[:16]


def main():
    ap = argparse.ArgumentParser(description="全局记忆制品生成器（在持有 L1 正本的机器上跑）")
    ap.add_argument("--out", required=True, help="制品目录（会被创建）")
    ap.add_argument("--config-dir", default="", help="宿主配置根（默认由 host_paths 解析）")
    ap.add_argument("--host", default="workbuddy", help="宿主名（默认 workbuddy）")
    ap.add_argument("--files", default="", help="覆盖打包清单（逗号分隔）")
    ap.add_argument("--verify", action="store_true", help="生成后逐件回读校验 sha16")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    cfgdir = a.config_dir
    if not cfgdir:
        if host_paths is None:
            print("[build_artifacts] 无法导入 host_paths 且未传 --config-dir", file=sys.stderr)
            return RC_UNAVAIL
        cfgdir = str(host_paths.host_config_dir(a.host))
    if not os.path.isdir(cfgdir):
        print("[build_artifacts] 宿主配置根不存在：%s" % cfgdir, file=sys.stderr)
        return RC_P0

    names = [x.strip() for x in a.files.split(",") if x.strip()] or list(KNOWN)
    if host_paths is not None and not a.files:
        gi = (getattr(host_paths, "PLATFORM_LAYOUTS", {}) or {}).get(a.host, {}).get("global_identity") or []
        for n in gi:
            if n not in names:
                names.insert(0, n)

    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    items, missing = [], []
    for n in names:
        s = os.path.join(cfgdir, n)
        if not os.path.isfile(s):
            missing.append(n)
            continue
        d = os.path.join(out, n)
        io.open(d, "wb").write(io.open(s, "rb").read())
        items.append({"file": n, "bytes": os.path.getsize(d), "sha16": sha16(d)})

    if not items:
        print("[build_artifacts] 无可打包件（宿主配置根：%s）" % cfgdir, file=sys.stderr)
        return RC_P0

    man = {"_meta": {"purpose": "全局记忆 portable 制品（供无正本的机器落位）",
                     "host": a.host,
                     "source": {"resolver": "host_paths.host_config_dir", "host": a.host,
                                "note": "🆕 2026-09-28 R36：原写产机绝对路径 ⇒ 跨机不可用且触发制品核对器 rc=1（清单产地绑定=是）；机器无关表达＝解析式＋宿主名，消费机自行解析"},
                     "generated_by": "host-adapters/global-memory/build_artifacts.py",
                     "criterion": "件名来自 PLATFORM_LAYOUTS[host].global_identity 与已知身份/台账名单",
                     "note": "制品含全文·只得经制品分支分发（见同目录 README）"},
           "artifacts": items, "missing": missing}
    io.open(os.path.join(out, "MANIFEST.json"), "w", encoding="utf-8",
            newline=LF).write(json.dumps(man, ensure_ascii=False, indent=2) + LF)

    if a.verify:
        bad = [it for it in items if sha16(os.path.join(out, it["file"])) != it["sha16"]]
        if bad:
            print("[build_artifacts] 回读失败 %d 件" % len(bad), file=sys.stderr)
            return RC_P0

    if a.json:
        print(json.dumps(man, ensure_ascii=False, indent=1))
    else:
        print("制品已生成：%s" % out)
        for it in items:
            print("   OK %-24s %8d B  sha16=%s" % (it["file"], it["bytes"], it["sha16"]))
        if missing:
            print("   未打包（宿主配置根无此件）：%s" % missing)
        print("   下一步：把本目录推入制品分支；消费机跑 scripts/global_memory_install.py --apply")
    return RC_OK if not missing else RC_P1


if __name__ == "__main__":
    sys.exit(main())
