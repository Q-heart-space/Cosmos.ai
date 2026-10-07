#!/usr/bin/env python3
"""
积分日志综合分析——单次加载，全部维度输出。
替代 task-retrospective Step B1-B5 的多次串行调用。

用法: python analyze_usage.py [目录路径]
默认搜索: 积分消耗记录/request-usage-*.xlsx（相对工作区根目录）
"""
import openpyxl
from collections import Counter, defaultdict
import glob, os, sys
from datetime import datetime

# ── 1. 自动发现所有日志文件 ──
SEARCH_DIR = sys.argv[1] if len(sys.argv) > 1 else "积分消耗记录"
files = sorted(glob.glob(os.path.join(SEARCH_DIR, "request-usage-*.xlsx")))

if not files:
    print("未找到积分日志文件")
    sys.exit(1)

print(f"发现 {len(files)} 个日志文件: {[os.path.basename(f) for f in files]}")

# ── 2. 一次加载全部 ──
all_rows = []
for f in files:
    wb = openpyxl.load_workbook(f, read_only=True)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        rid, cost, prompt, model, client, time_str = row
        prompt_str = str(prompt).strip() if prompt else ''
        cost_val = float(cost) if cost else 0
        model_str = str(model).strip() if model else 'unknown'
        time_s = str(time_str) if time_str else ''
        if not prompt_str or len(prompt_str) < 5:
            continue
        all_rows.append({
            'cost': cost_val,
            'model': model_str,
            'prompt': prompt_str,
            'time': time_s,
        })
    wb.close()

# Deduplicate by request content (same prompt within 1 min = same request)
seen = set()
deduped = []
for r in sorted(all_rows, key=lambda x: x['time']):
    key = (r['time'][:16], r['prompt'][:50])
    if key not in seen:
        seen.add(key)
        deduped.append(r)

print(f"总请求: {len(deduped)} (去重后)")

# ── 3. 基础画像 ──
total_cost = sum(r['cost'] for r in deduped)
model_counts = Counter(r['model'] for r in deduped)
model_costs = defaultdict(float)
for r in deduped:
    model_costs[r['model']] += r['cost']

dates = set(r['time'][:10] for r in deduped if r['time'])
print(f"\n{'='*50}")
print(f"总体: {len(dates)}天, {min(dates)}~{max(dates)}")
print(f"总积分: {total_cost:.0f}, 日均: {total_cost/len(dates):.0f}")
print(f"\n模型分布:")
for m, c in model_counts.most_common():
    print(f"  {m}: {c}次, {model_costs[m]:.0f}分, 均价{model_costs[m]/c:.1f}")

# ── 4. 用户用词频率 ──
keywords = ['复盘','深度复盘','强制深度复盘','元模式','全时空','检查','验证','校验','审计',
            '生成','创建','修复','升级','优化','日报','报告','推送','同步',
            '全局','修订','分析','对比','评估','总结','继续','执行','更新',
            '修改','写入','扫描','构建','发版','脱敏']
word_freq = Counter()
for r in deduped:
    clean = r['prompt'].replace('_x000d_',' ')
    for w in keywords:
        if w in clean:
            word_freq[w] += 1

print(f"\n用户用词 TOP15:")
for w, c in word_freq.most_common(15):
    print(f"  {w}: {c}次")

# ── 5. 多轮重复任务检测 ──
deduped.sort(key=lambda x: x['time'])
task_clusters = []
i = 0
while i < len(deduped):
    cur = deduped[i]
    sig = cur['prompt'].replace('_x000d_',' ')[:40]
    cluster = [cur]
    j = i + 1
    while j < len(deduped) and j < i + 15:
        nxt = deduped[j]
        nxt_sig = nxt['prompt'].replace('_x000d_',' ')[:40]
        if nxt_sig == sig:
            cluster.append(nxt)
            j += 1
        else:
            break
    if len(cluster) >= 3 and any(kw in cur['prompt'] for kw in ['复盘','报告','审计','日报','校验']):
        total = sum(r['cost'] for r in cluster)
        task_clusters.append({
            'rounds': len(cluster),
            'cost': total,
            'topic': sig[:80],
            'time': cur['time'][:16]
        })
        i = j
    else:
        i += 1

task_clusters.sort(key=lambda x: x['cost'], reverse=True)
print(f"\n🔴 多轮重复任务 ({len(task_clusters)}个):")
for tc in task_clusters[:10]:
    print(f"  [{tc['rounds']}轮/{tc['cost']:.0f}分] {tc['time']} | {tc['topic'][:80]}")

# ── 6. 触发词缺口检测 ──
triggers_have = {'复盘':'task-retrospective','日报':'daily-report','报告':'apq-report-deliver',
                 '推送':'wecom-push','脱敏':'report-desensitize','审计':'task-retrospective',
                 '构建':'apq-report-deliver'}
triggers_missing = []
for w, c in word_freq.most_common():
    if w not in triggers_have and c >= 10:
        triggers_missing.append((w, c))

if triggers_missing:
    print(f"\n⚠️ 高频但无触发词 ({len(triggers_missing)}个):")
    for w, c in triggers_missing:
        print(f"  {w}: {c}次 → 建议注册为触发词")

# ── 7. 模型浪费估算 ──
kimi_rows = [r for r in deduped if r['model'] == 'kimi-k2.7']
simple_kw = ['继续','执行','同意','是的','好的','可以','ok','确认']
kimi_simple = [r for r in kimi_rows if any(k in r['prompt'].lower()[:20] for k in simple_kw)]
flash_avg = sum(r['cost'] for r in deduped if r['model']=='deepseek-v4-flash') / max(sum(1 for r in deduped if r['model']=='deepseek-v4-flash'), 1)

print(f"\n💰 优化估算:")
print(f"  kimi简单指令: {len(kimi_simple)}次/{sum(r['cost'] for r in kimi_simple):.0f}分")
print(f"  若用flash替代(均价{flash_avg:.1f}): 省{sum(r['cost'] for r in kimi_simple)-len(kimi_simple)*flash_avg:.0f}分")
print(f"  多轮重复浪费: {sum(tc['cost'] for tc in task_clusters):.0f}分")
print(f"  触发词缺口: {len(triggers_missing)}个高频词无触发")

# ── 8. 结论 ──
print(f"\n{'='*50}")
print(f"分析完成。建议:")
if kimi_simple:
    print(f"  1. kimi简单指令用flash替代 → 预计省{sum(r['cost'] for r in kimi_simple)-len(kimi_simple)*flash_avg:.0f}分")
if task_clusters:
    print(f"  2. {len(task_clusters)}个多轮任务建立触发词 → 预计省{sum(tc['cost'] for tc in task_clusters)*0.7:.0f}分")
if triggers_missing:
    print(f"  3. 注册 {len(triggers_missing)} 个触发词到对应技能")
