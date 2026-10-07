#!/usr/bin/env python3
"""报告敏感数据预扫描——脱敏前必须运行，输出完整命中清单供确认"""
import re, sys, os

def scan_sensitive(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    results = {}

    # === P0: 必须删除 ===
    p0_patterns = {
        '内部财务(¥精确金额)': r'¥[\d,]+(?:万|亿)?',
        '内部财务(¥含千位分隔)': r'¥\d{1,3}(?:,\d{3})+',
        '内部系统名(金蝶/卫瓴/简道云)': r'金蝶|卫瓴|简道云',
        '内部客户名(黑湖/新核云/海特等)': r'黑湖|新核云|海特|先导智能|海兰信',
        '内部工具名(向日葵/飞书/TeamViewer)': r'向日葵|飞书|TeamViewer|1688 AI客服',
        '内部人物(老板/二把手/副总/研发老大)': r'二把手|常务副总|研发老大|工控线|权力地图',
        '内部人物(凌壹老板指代)': r'凌壹.{0,20}老板',
        '版本迭代记录(**vX.X**)': r'\*\*v\d+\.\d+\*\*',
        '版本新增说明(> ⭐ 新增)': r'> ⭐.*新增',
        '版本整合说明(整合自V\d)': r'整合自V\d',
        'ERP精确行数(15,496/51,254)': r'15,?496|51,?254',
        'CRM精确记录(63,981)': r'63,?981',
        '内部客户数量(887家/X家客户)': r'\d+家\s*(?:客户|渠道|集成)',
        '内部系统(SaaS工具矩阵表)': r'月费\s*\|',
        '内部薪资(¥X万/月)': r'万/月|万/年',
        'APQ营收数字(¥1.10亿等)': r'¥\d+\.\d+亿',
        'APQ下滑百分比(-13.4%)': r'-?\d+\.\d+%',
        'APQ精确价格(¥5,700等)': r'¥\d{1,2},\d{3}',
        '博弈底牌(T1-T5止损)': r'T\d\s*[:：]|止损点|止损触发',
        '底线预案(四种情景)': r'底线预案|不签约就撤|退出供板|被竞品收购',
    }

    # === P1: 必须脱敏 ===
    p1_patterns = {
        '竞品供板价(¥XX/片)': r'¥\d+[~/]\s*片',
        'BOM精确价格(¥XXX-XXX)': r'BOM\s*[≈=]\s*¥|BOM\s*约\s*¥',
        '毛利率精确数(XX%)': r'\d{2}%\s*毛利',
        '团队薪资(提及薪资)': r'薪资|工资|万/月|万/年',
        '启动资金(¥XX万)': r'启动资金|¥\d+万.*启动',
        '盈亏平衡(XX台)': r'盈亏平衡\s*[：:]?\s*\d+',
        '竞品营收估算(XX亿)': r'营收.{0,10}[约~]?\d+\.?\d*\s*亿',
    }

    # === P2: 需要软化 ===
    p2_patterns = {
        '博弈用语(防火墙/底牌/筹码)': r'防火墙|底牌|筹码',
        '敌对语言(对手是谁/打击/击败)': r'对手是谁|打击|击败',
        '负面评价(最危险/存疑/失败)': r'最危险|存疑|失败|极差|很差',
        '排他表述(唯一来源/不可替代)': r'唯一来源|不可替代|只有.*才能',
        '谈判语言(谈判)': r'谈判',
        '内部评价(APQ.*下滑/弱/萎缩)': r'APQ.{0,20}(?:下滑|萎缩|弱)',
    }

    # === P3: 需要标注 ===
    p3_patterns = {
        '供板价需确认': r'供板价|供板价格',
        'BOM成本需确认': r'BOM.{0,10}(?:成本|价格|估算)',
    }

    for level, patterns in [('P0-删除', p0_patterns), ('P1-脱敏', p1_patterns), ('P2-软化', p2_patterns), ('P3-标注', p3_patterns)]:
        results[level] = {}
        for name, pattern in patterns.items():
            matches = list(re.finditer(pattern, content))
            if matches:
                results[level][name] = len(matches)

    # Print results
    total = 0
    for level in ['P0-删除', 'P1-脱敏', 'P2-软化', 'P3-标注']:
        items = results[level]
        if items:
            count = sum(items.values())
            total += count
            print(f'\n### {level} ({count}处)')
            for name, cnt in sorted(items.items(), key=lambda x: -x[1]):
                print(f'  [{cnt:4d}] {name}')

    print(f'\n{"="*40}')
    print(f'总计: {total}处敏感数据待处理')
    print(f'预计处理时间: {total * 2}秒（批量替换）')

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else '垦微_爱品科AIPC_类工控业务战略报告_v5.3.md'
    scan_sensitive(path)
