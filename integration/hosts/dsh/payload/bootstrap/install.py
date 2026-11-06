#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q博士 能力自举器（载体自带·stdlib only；Codex hooks 需治理者脚本根）。

用法：python install.py [--dry-run] [--dest <平台配置根>] [--force]
判据：逐文件 sha256 校验（清单≠实体 ⇒ 拒绝落位·fail-closed）；落位前备份到 `~/.qdr-deploy-backups/`。
"""
import argparse
import hashlib
import json
import os
import pathlib
import shlex
import shutil
import subprocess
import sys
import tempfile
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

HERE = pathlib.Path(__file__).resolve().parent


def _bundle_layout():
    """源树 bootstrap/ 与公开包 payload/bootstrap/ 共用同一安装器。"""
    for manifest in (HERE / "manifest.json", HERE.parent / "manifest.json",
                     HERE.parent.parent / "manifest.json"):
        if manifest.is_file():
            return manifest, HERE.parent
    raise FileNotFoundError("manifest.json missing next to bootstrap or package root")


def self_test():
    """只复制清单列出的载荷到临时包，验证真实安装与拒写。"""
    with tempfile.TemporaryDirectory(prefix="qdr-bootstrap-test-") as td:
        temp = pathlib.Path(td)
        manifest, payload_root = _bundle_layout()
        man = json.loads(manifest.read_text(encoding="utf-8"))
        pkg = temp / "pkg"
        (pkg / "bootstrap").mkdir(parents=True)
        shutil.copy2(HERE / "install.py", pkg / "bootstrap/install.py")
        shutil.copy2(manifest, pkg / "bootstrap/manifest.json")
        for item in man["files"]:
            src = payload_root / item["src"]
            dst = pkg / item["src"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        env = os.environ.copy()
        env["HOME"] = str(temp / "home")
        env["USERPROFILE"] = str(temp / "home")
        for key in ("QDR_HOST_ROOT", "QDR_HOST_SKILLS_DIR", "QDR_SKILLS_DIR", "HERMES_HOME", "QDR_ROOT"):
            env.pop(key, None)
        extra = []
        if man.get("_meta", {}).get("platform") == "codex":
            root = temp / "qdr root"
            root.mkdir()
            hooks = json.loads((pkg / "hooks.json").read_text(encoding="utf-8"))
            for groups in hooks.get("hooks", {}).values():
                for group in groups:
                    for hook in group.get("hooks", []):
                        for arg in hook.get("command_argv", []):
                            if isinstance(arg, str) and arg.endswith(".py") and "${QDR_ROOT}" in arg:
                                script = pathlib.Path(arg.replace("${QDR_ROOT}", str(root)))
                                script.parent.mkdir(parents=True, exist_ok=True)
                                script.write_text("print('probe')\n", encoding="utf-8")
            extra = ["--qdr-root", str(root)]

        def run(package, target, *flags):
            return subprocess.run(
                [sys.executable, str(package / "bootstrap/install.py"), "--dest", str(target),
                 *extra, *flags], env=env, capture_output=True, text=True,
                encoding="utf-8", errors="replace")

        target = temp / "installed"
        dry = run(pkg, target, "--dry-run")
        dry_ok = dry.returncode == 0 and not target.exists()
        installed = run(pkg, target)
        second = run(pkg, target)
        bad = temp / "bad"
        shutil.copytree(pkg, bad)
        last = bad / man["files"][-1]["src"]
        last.write_bytes(last.read_bytes() + b"tampered")
        bad_target = temp / "bad_target"
        rejected = run(bad, bad_target)
        missing = temp / "missing"
        shutil.copytree(pkg, missing)
        (missing / man["files"][-1]["src"]).unlink()
        missing_target = temp / "missing_target"
        absent = run(missing, missing_target)
        checks = [dry_ok,
                  installed.returncode == 0 and target.is_dir(),
                  second.returncode == 0 and "跳过" in second.stdout,
                  rejected.returncode == 1 and not bad_target.exists(),
                  absent.returncode == 1 and not missing_target.exists()]
        print("bootstrap self-test: %d/5 PASS checks=%s" % (sum(checks), checks))
        return 0 if all(checks) else 1


def _roots(dest=None, meta=None):
    home = pathlib.Path(os.path.expanduser("~"))
    configured = dest or os.environ.get("QDR_HOST_ROOT")
    convention = str((meta or {}).get("config_dir") or "")
    if not configured and convention.startswith("$"):
        configured = os.environ.get(convention[1:])
    if not configured and convention.startswith(".") and ".." not in pathlib.Path(convention).parts:
        configured = str(home / convention)
    if not configured:
        return None
    cfg = pathlib.Path(configured).expanduser().resolve()
    skills = os.environ.get("QDR_HOST_SKILLS_DIR") or os.environ.get("QDR_SKILLS_DIR")
    return {"${HOME}": str(home), "${PLATFORM_CONFIG_DIR}": str(cfg),
            "${QDR_HOST_SKILLS_DIR}": str(pathlib.Path(skills).expanduser().resolve()) if skills else str(cfg / "skills")}


def _render_codex_hooks(src, qdr_root):
    """随包自举也从 argv 按当前 OS 生成命令；缺依赖时不写半套配置。"""
    if not qdr_root:
        return None, "Codex hooks 需要 --qdr-root 或 QDR_ROOT"
    root = pathlib.Path(qdr_root).expanduser().resolve()
    if not root.is_dir():
        return None, "QDR_ROOT 不存在：%s" % root
    try:
        doc = json.loads(src.read_text(encoding="utf-8"))
        for event, groups in doc["hooks"].items():
            for group in groups:
                for hook in group.get("hooks", []):
                    if hook.get("type") != "command":
                        continue
                    argv = hook.pop("command_argv", None)
                    if not isinstance(argv, list) or not argv or not all(
                            isinstance(arg, str) and arg and "\x00" not in arg
                            and "\n" not in arg and "\r" not in arg for arg in argv):
                        return None, "command_argv 缺失或非法：%s" % event
                    args = [arg.replace("${PYTHON}", sys.executable)
                            .replace("${QDR_ROOT}", str(root)) for arg in argv]
                    if any("${" in arg for arg in args):
                        return None, "hook 占位符未解析：%s" % event
                    scripts = [pathlib.Path(arg) for arg in args if arg.lower().endswith(".py")]
                    if not scripts or not all(script.is_file() for script in scripts):
                        return None, "hook 脚本不存在：%s" % event
                    hook["command"] = (subprocess.list2cmdline(args) if os.name == "nt"
                                       else shlex.join(args))
    except (OSError, ValueError, KeyError, TypeError) as e:
        return None, "hooks 模板不可解析：%s" % type(e).__name__
    return (json.dumps(doc, ensure_ascii=False, indent=2) + "\n").encode("utf-8"), None


def main():
    ap = argparse.ArgumentParser(description="Q博士 能力自举器（载体自带）")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--self-test", action="store_true", help="隔离安装与拒写回归")
    ap.add_argument("--dest", default=None, help="平台配置根（默认 --host 对应目录）")
    ap.add_argument("--force", action="store_true", help="覆盖已存在且内容不同的文件（先备份）")
    ap.add_argument("--qdr-root", default=None, help="Codex hooks 所需的治理者根（或设置 QDR_ROOT）")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    try:
        manifest, payload_root = _bundle_layout()
    except FileNotFoundError as exc:
        print("  ⏸ %s" % exc)
        return 3
    man = json.loads(manifest.read_text(encoding="utf-8"))
    roots = _roots(a.dest, man.get("_meta"))
    if roots is None:
        print("  ⏸ 宿主配置根未判定：请设置 --dest、QDR_HOST_ROOT 或 Hermes 的 HERMES_HOME")
        return 3
    bak = pathlib.Path(os.path.expanduser("~")) / ".qdr-deploy-backups" / time.strftime("%Y%m%d_%H%M%S")
    copied = skipped = backed = 0
    # 整单验真后才写，避免第 N 件缺失或漂移时前 N-1 件已落位。
    invalid = []
    for it in man["files"]:
        src = payload_root / it["src"]
        if not src.is_file():
            invalid.append("清单件缺失：%s" % it["src"])
            continue
        h = hashlib.sha256(src.read_bytes()).hexdigest()
        if it.get("sha256") and h != it["sha256"]:
            invalid.append("校验失败（清单≠实体）：%s" % it["src"])
    if invalid:
        for problem in invalid:
            print("  🛑 " + problem)
        print("自举拒绝：清单校验失败 **%d** 件，零写入" % len(invalid))
        return 1
    rendered_hooks = None
    if man.get("_meta", {}).get("platform") == "codex":
        hook_items = [it for it in man["files"] if it.get("src") == "hooks.json"]
        if len(hook_items) != 1:
            print("  🛑 Codex hooks 清单缺失或重复；零写入")
            return 1
        rendered_hooks, err = _render_codex_hooks(
            payload_root / "hooks.json", a.qdr_root or os.environ.get("QDR_ROOT"))
        if err:
            print("  ⏸ " + err + "；零写入")
            return 3
    for it in man["files"]:
        src = payload_root / it["src"]
        dst = pathlib.Path(it["dst"])
        for k, v in roots.items():
            dst = pathlib.Path(str(dst).replace(k, v))
        payload = rendered_hooks if it["src"] == "hooks.json" and rendered_hooks is not None else src.read_bytes()
        same = dst.is_file() and dst.read_bytes() == payload
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
        if rendered_hooks is not None and it["src"] == "hooks.json":
            dst.write_bytes(payload)
        else:
            shutil.copy2(src, dst)
        copied += 1
    print("自举结果：新增/覆盖 **%d** ｜ 跳过（已同/no-clobber）**%d** ｜ 备份 **%d** ｜ 清单缺件 **%d**"
          % (copied, skipped, backed, 0))
    if not a.dry_run and backed:
        print("备份根：%s" % bak)
    return 0


if __name__ == "__main__":
    sys.exit(main())
