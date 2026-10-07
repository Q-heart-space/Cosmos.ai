#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# >   ① 与本机宿主配置根实件对拍 ② 有漂移 ⇒ 重新生成制品 ③ 覆盖到制品分支并提交推送。
# > **盲区**：只做「本机 → 分支」单向；分支 → 消费机 的落位由 `scripts/global_memory_install.py` 负责。

"""全局记忆制品同步器（本机 L1 → 私密制品分支）。

用法：
  python host-adapters/global-memory/sync_artifacts.py --check     # 看漂移（只读）
  python host-adapters/global-memory/sync_artifacts.py --apply     # 有漂移则再生＋推送
  python host-adapters/global-memory/sync_artifacts.py --self-test # 自检（零副作用）

跨机跨宿主：宿主配置根一律经 `host_paths.host_config_dir()` 运行期解析；零绝对路径字面量。
"""
import argparse
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

# 🆕 2026-10-01（B机 r1535·`HO-089`·**GBK 载荷族·跨分支面**）：**防御式 stdout/stderr reconfigure**——
#   本件 print 载荷含 GBK 不可编码字符（🛑/✅/🔴 等），在 **GBK 控制台**下抛 `UnicodeEncodeError`
#   ⇒ 判据内容对但**出口读数不可信**（主仓同族已修 5 例·本分支此前**不在判据扫描域内**）。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


_HERE = os.path.dirname(os.path.abspath(__file__))
BRANCH = "global-memory-artifacts"
RC_OK, RC_P1, RC_P0, RC_UNAVAIL = 0, 1, 2, 3


def _sh(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def _sha16(p):
    return hashlib.sha256(io.open(p, "rb").read()).hexdigest()[:16]


def _host_paths():
    for cand in (os.path.join(_HERE, "..", "..", "Q博士", "scripts"),
                 os.path.join(_HERE, "..", "..", "..", "scripts"),
                 os.path.join(_HERE, "..", "..", "..", "..", "scripts")):
        p = os.path.abspath(cand)
        if os.path.isdir(p):
            sys.path.insert(0, p)
            try:
                import host_paths
                return host_paths
            except Exception:  # noqa: BLE001
                continue
    return None


def _local_items(hp, host):
    """本机宿主配置根下「应打包的件」→ {name: sha16}。"""
    cfgdir = str(hp.host_config_dir(host))
    gi = (getattr(hp, "PLATFORM_LAYOUTS", {}) or {}).get(host, {}).get("global_identity") or []
    KNOWN = ("MEMORY.md", "MEMORY_RULES.md", "MEMORY_SKILLS.md",
             "IDENTITY.md", "SOUL.md", "USER.md", ".MEMORY_CHANGELOG.md")
    names = []
    for n in list(gi) + list(KNOWN):
        if n not in names:
            names.append(n)
    out = {}
    for n in names:
        p = os.path.join(cfgdir, n)
        if os.path.isfile(p):
            out[n] = _sha16(p)
    return cfgdir, out


def _branch_items(repo, branch):
    """制品分支 MANIFEST 里的 {name: sha16}（经 git show·不检出）。"""
    r = _sh(["git", "show", "%s:artifacts/MANIFEST.json" % branch], cwd=repo)
    if r.returncode != 0:
        return None, "分支 %s 无 artifacts/MANIFEST.json" % branch
    try:
        j = json.loads(r.stdout)
    except ValueError as e:
        return None, "MANIFEST 解析失败：%s" % e
    return {it["file"]: it.get("sha16") for it in (j.get("artifacts") or [])}, ""


def _diff(local, remote):
    """返回 (需更新件, 新增件, 删除件)。"""
    upd, add, dele = [], [], []
    for n, h in sorted(local.items()):
        if n not in remote:
            add.append(n)
        elif remote[n] != h:
            upd.append(n)
    for n in sorted(remote):
        if n not in local:
            dele.append(n)
    return upd, add, dele


def _self_test():
    hp = _host_paths()
    checks = [
        ("T1 host_paths 可导入", hp is not None),
        ("T2 宿主配置根可解析", hp is not None and bool(hp.host_config_dir("workbuddy"))),
        ("T3 制品分支名常量", BRANCH == "global-memory-artifacts"),
        ("T4 rc 契约常量齐备", (RC_OK, RC_P1, RC_P0, RC_UNAVAIL) == (0, 1, 2, 3)),
        ("T5 同目录生成器存在", os.path.isfile(os.path.join(_HERE, "build_artifacts.py"))),
    ]
    for n, ok in checks:
        print("   %s %s" % ("✅" if ok else "🔴", n))
    nb = len([1 for _n, ok in checks if not ok])
    print("📊 自检：%d/%d 通过" % (len(checks) - nb, len(checks)))
    return RC_OK if not nb else RC_P0


def main():
    ap = argparse.ArgumentParser(description="全局记忆制品同步器（本机 L1 → 私密制品分支）")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true", help="只读：列出漂移")
    g.add_argument("--apply", action="store_true", help="有漂移则再生＋提交＋推送")
    g.add_argument("--self-test", action="store_true")
    ap.add_argument("--host", default="workbuddy")
    ap.add_argument("--remote", default="origin")
    ap.add_argument("--apply-no-push", action="store_true", help="再生＋提交·不推送（离线/预览用）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return _self_test()

    hp = _host_paths()
    if hp is None:
        print("[sync_artifacts] 判据不可用：无法导入 host_paths", file=sys.stderr)
        return RC_UNAVAIL
    repo = os.path.abspath(os.path.join(_HERE, ".."))
    cfgdir, local = _local_items(hp, a.host)
    if not local:
        print("[sync_artifacts] 本机宿主配置根无可打包件：%s" % cfgdir, file=sys.stderr)
        return RC_P0

    _sh(["git", "fetch", a.remote, "--prune"], cwd=repo)
    remote, err = _branch_items(repo, "%s/%s" % (a.remote, BRANCH))
    if remote is None:
        print("[sync_artifacts] %s" % err, file=sys.stderr)
        return RC_P0

    upd, add, dele = _diff(local, remote)
    drift = len(upd) + len(add) + len(dele)
    if a.json:
        print(json.dumps({"config_dir": cfgdir, "local": local, "remote": remote,
                          "updated": upd, "added": add, "removed": dele, "drift": drift},
                         ensure_ascii=False, indent=1))
    else:
        print("🔍 制品同步核对：本机=%s ｜ 分支=%s/%s" % (cfgdir, a.remote, BRANCH))
        print("   本机件=%d ｜ 分支件=%d ｜ 漂移=%d" % (len(local), len(remote), drift))
        for n in upd:
            print("   🔧 内容变更 %-24s %s → %s" % (n, remote[n], local[n]))
        for n in add:
            print("   🆕 分支缺件 %-24s %s" % (n, local[n]))
        for n in dele:
            print("   🗑️ 本机已无 %-24s（分支有 %s）" % (n, remote[n]))
        if not drift:
            print("   ✅ 无漂移（本机 L1 与制品分支一致）")
    if not a.apply:
        return RC_OK if not drift else RC_P1

    if not drift:
        print("✅ 无漂移 ⇒ 无需更新")
        return RC_OK

    # 再生制品 → 覆盖分支 → 提交 → 推送
    tmp = tempfile.mkdtemp(prefix="qdr_gm_sync_")
    art = os.path.join(tmp, "artifacts")
    r = _sh([sys.executable, os.path.join(_HERE, "build_artifacts.py"),
             "--out", art, "--host", a.host, "--verify"], cwd=_HERE)
    print("   生成器 rc=%d" % r.returncode)
    if r.returncode not in (0, 1):
        print((r.stderr or r.stdout)[:400], file=sys.stderr)
        shutil.rmtree(tmp, ignore_errors=True)
        return RC_P0
    wt = os.path.join(tmp, "wt")
    if _sh(["git", "worktree", "add", "--detach", wt, "%s/%s" % (a.remote, BRANCH)], cwd=repo).returncode != 0:
        print("[sync_artifacts] worktree add 失败", file=sys.stderr)
        shutil.rmtree(tmp, ignore_errors=True)
        return RC_P0
    try:
        tgt = os.path.join(wt, "artifacts")
        shutil.rmtree(tgt, ignore_errors=True)
        shutil.copytree(art, tgt)
        _sh(["git", "add", "-A"], cwd=wt)
        st = _sh(["git", "status", "--porcelain"], cwd=wt).stdout.strip()
        if not st:
            print("✅ 分支内容已一致 ⇒ 无需提交")
            return RC_OK
        msg = ("chore(global-memory-artifacts): 制品同步（本机 L1 更新）\n\n"
               "漂移：内容变更 %d ｜ 新增 %d ｜ 移除 %d\n%s"
               % (len(upd), len(add), len(dele),
                  "\n".join(["  ~ %s" % x for x in upd] + ["  + %s" % x for x in add] + ["  - %s" % x for x in dele])))
        rc = _sh(["git", "-c", "user.name=Q博士", "-c", "user.email=q博士@local.qdr",
                  "commit", "-m", msg], cwd=wt).returncode
        print("   commit rc=%d" % rc)
        if a.apply_no_push:
            print("   （--apply-no-push ⇒ 未推送）")
            return RC_OK if rc == 0 else RC_P0
        if _sh(["git", "fetch", a.remote, "--prune"], cwd=wt).returncode == 0:
            _sh(["git", "rebase", "%s/%s" % (a.remote, BRANCH)], cwd=wt)
        pr = _sh(["git", "push", a.remote, "HEAD:refs/heads/%s" % BRANCH], cwd=wt)
        print("   push rc=%d ｜ %s" % (pr.returncode, (pr.stderr or pr.stdout).strip().split("\n")[-1][:110]))
        return RC_OK if pr.returncode == 0 else RC_P0
    finally:
        _sh(["git", "worktree", "remove", "--force", wt], cwd=repo)
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
