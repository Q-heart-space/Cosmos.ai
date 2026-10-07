#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q博士 能力自举器（**載体自带·零治理者依赖**·stdlib only）。

用法：python install.py [--dry-run] [--dest <平台配置根>] [--force]
判据：逐文件 sha256 校验（清单≠实体 ⇒ 拒绝落位·fail-closed）；落位前备份到 `~/.qdr-deploy-backups/`。
"""
import argparse
import hashlib
import json
import os
import pathlib
import shutil
import sys
import time

# 🆕 2026-10-01（B机 r1535·`HO-089`·**GBK 载荷族·跨分支面**）：**防御式 stdout/stderr reconfigure**——
#   本件 print 载荷含 GBK 不可编码字符（🛑/✅/🔴 等），在 **GBK 控制台**下抛 `UnicodeEncodeError`
#   ⇒ 判据内容对但**出口读数不可信**（主仓同族已修 5 例·本分支此前**不在判据扫描域内**）。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


HERE = pathlib.Path(__file__).resolve().parent


def _roots(dest=None):
    home = pathlib.Path(os.path.expanduser("~"))
    return {"${HOME}": str(home), "${PLATFORM_CONFIG_DIR}": dest or str(home / ".workbuddy"),
            "${QDR_HOST_SKILLS_DIR}": str(home / ".workbuddy" / "skills")}


def main():
    ap = argparse.ArgumentParser(description="Q博士 能力自举器（载体自带）")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--dest", default=None, help="平台配置根（默认 --host 对应目录）")
    ap.add_argument("--force", action="store_true", help="覆盖已存在且内容不同的文件（先备份）")
    a = ap.parse_args()
    man = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    roots = _roots(a.dest)
    bak = pathlib.Path(os.path.expanduser("~")) / ".qdr-deploy-backups" / time.strftime("%Y%m%d_%H%M%S")
    ok = copied = skipped = backed = missing = 0
    for it in man["files"]:
        src = HERE.parent / it["src"]        # 🆕 _src_base_fix：载体平台目录（原 `HERE/` ⇒ 清单缺件假红）
        if not src.is_file():
            print("  🛑 清单件缺失：%s" % it["src"]); missing += 1; continue
        h = hashlib.sha256(src.read_bytes()).hexdigest()
        if it.get("sha256") and h != it["sha256"]:
            print("  🛑 校验失败（清单≠实体）：%s" % it["src"]); ok = 1; continue
        dst = pathlib.Path(it["dst"])
        for k, v in roots.items():
            dst = pathlib.Path(str(dst).replace(k, v))
        same = dst.is_file() and dst.read_bytes() == src.read_bytes()
        if same:
            skipped += 1; continue
        if dst.is_file() and not a.force:
            print("  🔵 已存在且不同（no-clobber·需 --force）：%s" % dst); skipped += 1; continue
        if a.dry_run:
            print("  ✏️ [dry-run] %s → %s" % (it["src"], dst)); copied += 1; continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.is_file():
            b = bak / it["src"]; b.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dst, b); backed += 1
        shutil.copy2(src, dst); copied += 1
    print("自举结果：新增/覆盖 **%d** ｜ 跳过（已同/no-clobber）**%d** ｜ 备份 **%d** ｜ 清单缺件 **%d**"
          % (copied, skipped, backed, missing))
    if not a.dry_run and backed:
        print("备份根：%s" % bak)
    return 1 if (missing or ok) else 0


if __name__ == "__main__":
    sys.exit(main())
