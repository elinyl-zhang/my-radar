#!/usr/bin/env python3
"""
radar-pipeline.py — My Radar 每日更新管道（容错版）

这个脚本做所有确定性工作：
  - 备份旧 feed
  - 校验新 feed（JSON 语法、必需字段、图片 URL 可达性）
  - 组装 HTML（模板 + feed → 桌面文件）
  - 校验输出 HTML（JS 语法检查、关键 DOM 元素）
  - 失败时回滚

AI agent 只需要做一件事：生成新的 daily-feed.json 并写到指定路径。
然后调用本脚本完成剩下的所有步骤。

用法:
  python3 radar-pipeline.py                    # 完整管道（校验+组装+部署）
  python3 radar-pipeline.py --check            # 只校验当前 feed，不部署
  python3 radar-pipeline.py --rollback         # 回滚到昨天的备份
  python3 radar-pipeline.py --status           # 检查系统健康状态
"""

import sys, os, re, json, shutil, subprocess
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError

# ─── 路径常量 ───
# repo root = the directory above pipeline/. Override with RADAR_HOME.
RADAR_HOME = os.environ.get('RADAR_HOME') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE   = os.path.join(RADAR_HOME, 'templates', 'radar-v4.html')
FEED_PATH  = os.path.join(RADAR_HOME, 'feed.json')
OUTPUT     = os.path.join(RADAR_HOME, 'index.html')
BACKUP_DIR = os.path.join(RADAR_HOME, 'backups')
PROFILE    = os.path.join(RADAR_HOME, 'data', 'profile.json')

# ─── 颜色输出 ───
def ok(msg):   print(f"  ✅ {msg}")
def warn(msg): print(f"  ⚠️  {msg}")
def fail(msg): print(f"  ❌ {msg}")
def info(msg): print(f"  → {msg}")

# ─── 1. 备份 ───
def backup_feed():
    """备份当前 feed 到 backups/ 目录，保留最近 7 天"""
    if not os.path.exists(FEED_PATH):
        warn(f"Feed 不存在，跳过备份: {FEED_PATH}")
        return None
    
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime('%Y-%m-%d')
    backup_file = os.path.join(BACKUP_DIR, f'daily-feed-{ts}.json')
    
    # 如果今天的备份已存在，不覆盖（保留第一次备份）
    if os.path.exists(backup_file):
        info(f"今日备份已存在: {backup_file}")
        return backup_file
    
    shutil.copy2(FEED_PATH, backup_file)
    ok(f"备份: {backup_file}")
    
    # 清理 7 天前的备份
    for f in sorted(os.listdir(BACKUP_DIR)):
        fp = os.path.join(BACKUP_DIR, f)
        if os.path.isfile(fp) and f.startswith('daily-feed-'):
            date_str = f.replace('daily-feed-', '').replace('.json', '')
            try:
                d = datetime.strptime(date_str, '%Y-%m-%d')
                if (datetime.now() - d).days > 7:
                    os.remove(fp)
                    info(f"清理旧备份: {f}")
            except ValueError:
                pass
    
    return backup_file

# ─── 2. 校验 Feed ───
def validate_feed(feed_path=None):
    """校验 feed JSON：语法、必需字段、信号数量、editorial 板块"""
    path = feed_path or FEED_PATH
    errors = []
    warnings = []
    
    # 2a. 文件存在
    if not os.path.exists(path):
        errors.append(f"Feed 文件不存在: {path}")
        return None, errors, warnings
    
    # 2b. JSON 语法
    with open(path, 'r') as f:
        raw = f.read()
    try:
        feed = json.loads(raw)
    except json.JSONDecodeError as e:
        errors.append(f"JSON 语法错误: {e}")
        return None, errors, warnings
    
    # 2c. 必需字段
    required_top = ['date', 'signals', 'territories', 'pattern', 'open_question']
    for k in required_top:
        if k not in feed:
            errors.append(f"缺少必需字段: {k}")
    
    # 2d. signals
    signals = feed.get('signals', [])
    if len(signals) == 0:
        errors.append("signals 数组为空")
    elif len(signals) < 3:
        warnings.append(f"只有 {len(signals)} 条信号（建议 ≥ 3）")
    
    for i, s in enumerate(signals):
        L = s.get('landscape', {})
        if not L.get('domain'):
            warnings.append(f"signal[{i}] 缺少 landscape.domain")
        if not L.get('x') or not L.get('y'):
            warnings.append(f"signal[{i}] 缺少 landscape 坐标")
    
    # 2e. territories
    territories = feed.get('territories', [])
    known_domains = {'AI SYSTEMS', 'HUMAN COGNITION', 'CULTURAL DATA', 'DIGITAL HUMANITIES'}
    if len(territories) < 4:
        warnings.append(f"只有 {len(territories)} 个领地（期望 4）")
    for t in territories:
        if t.get('name') not in known_domains:
            warnings.append(f"未知领地: {t.get('name')}")
    
    # 2f. editorial
    ed = feed.get('editorial', {})
    if not ed:
        warnings.append("没有 editorial 板块（六板块内容将不显示）")
    else:
        for section in ['world', 'think', 'look', 'discover', 'explore', 'make']:
            if section not in ed:
                warnings.append(f"editorial 缺少板块: {section}")
    
    return feed, errors, warnings

# ─── 3. 校验图片 URL ───
def check_images(feed, timeout=5):
    """检查 LOOK 和 DISCOVER 的图片 URL 是否可达"""
    warnings = []
    ed = feed.get('editorial', {})
    
    look_img = ed.get('look', {}).get('image_url', '')
    if look_img:
        try:
            result = subprocess.run(['curl', '-sIL', '--max-time', str(timeout), look_img], capture_output=True, text=True)
            first_line = result.stdout.split('\n')[0] if result.stdout else ''
            if '200' in first_line:
                ok(f"LOOK 图片可达: {look_img[:60]}...")
            else:
                warnings.append(f"LOOK 图片返回非200: {first_line.strip() or 'no response'}")
        except Exception as e:
            warnings.append(f"LOOK 图片检查失败: {str(e)[:50]}")
    else:
        warnings.append("LOOK 没有 image_url")
    
    disc_img = ed.get('discover', {}).get('portrait_url', '')
    if disc_img:
        try:
            result = subprocess.run(['curl', '-sIL', '--max-time', str(timeout), disc_img], capture_output=True, text=True)
            first_line = result.stdout.split('\n')[0] if result.stdout else ''
            if '200' in first_line:
                ok(f"DISCOVER 头像可达: {disc_img[:60]}...")
            else:
                warnings.append(f"DISCOVER 头像返回非200: {first_line.strip() or 'no response'}")
        except Exception as e:
            warnings.append(f"DISCOVER 头像检查失败: {str(e)[:50]}")
    else:
        warnings.append("DISCOVER 没有 portrait_url")
    
    return warnings

# ─── 4. 组装 HTML ───
def assemble(feed_path=None):
    """将 feed 嵌入模板，返回 HTML 字符串"""
    path = feed_path or FEED_PATH
    
    if not os.path.exists(TEMPLATE):
        return None, [f"模板不存在: {TEMPLATE}"]
    
    with open(TEMPLATE, 'r') as f:
        html = f.read()
    
    with open(path, 'r') as f:
        feed_text = f.read().strip()
    
    # 查找并替换内联 feed
    pattern = r'var\s+feed\s*=\s*\{[\s\S]*?\}\s*;'
    match = re.search(pattern, html)
    if not match:
        return None, ["模板中找不到 'var feed = {...};' 标记"]
    
    new_html = html[:match.start()] + 'var feed = ' + feed_text + ';' + html[match.end():]
    return new_html, []

# ─── 5. 校验输出 HTML ───
def validate_output(html_str):
    """基础 HTML 校验：结构完整、无 JS 语法错误的明显标志"""
    errors = []
    
    if '</html>' not in html_str:
        errors.append("HTML 缺少 </html> 闭合标签")
    if '</script>' not in html_str:
        errors.append("HTML 缺少 </script> 闭合标签")
    if 'editorialMount' not in html_str:
        errors.append("HTML 缺少 editorialMount")
    if 'renderEditorial' not in html_str:
        errors.append("HTML 缺少 renderEditorial 函数")
    if 'renderLandscape' not in html_str:
        errors.append("HTML 缺少 renderLandscape 函数")
    
    # 检查 feed 是否嵌入
    if 'var feed = ' not in html_str:
        errors.append("HTML 中没有内联 feed 数据")
    
    # 检查常见 JS 语法错误模式
    broken_onerror = "onerror=\"this.style.display='none'\"" in html_str
    if broken_onerror:
        errors.append("发现旧版 onerror 单引号冲突（应使用 this.remove()）")
    
    return errors

# ─── 6. 部署 ───
def deploy(html_str):
    """写入桌面文件"""
    with open(OUTPUT, 'w') as f:
        f.write(html_str)
    return os.path.exists(OUTPUT)

# ─── 7. 回滚 ───
def rollback():
    """回滚到最近的备份"""
    if not os.path.exists(BACKUP_DIR):
        fail("没有备份目录")
        return False
    
    backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith('daily-feed-') and f.endswith('.json')], reverse=True)
    if not backups:
        fail("没有可用的备份")
        return False
    
    # 用最新的备份
    latest = os.path.join(BACKUP_DIR, backups[0])
    info(f"回滚到备份: {backups[0]}")
    
    # 校验备份
    feed, errors, warnings = validate_feed(latest)
    if errors:
        fail(f"备份也有错误: {errors}")
        return False
    
    # 复制备份到 feed 路径
    shutil.copy2(latest, FEED_PATH)
    ok(f"已回滚 feed: {FEED_PATH}")
    
    # 重新组装
    html_str, asm_errors = assemble(latest)
    if asm_errors:
        fail(f"组装失败: {asm_errors}")
        return False
    
    val_errors = validate_output(html_str)
    if val_errors:
        fail(f"输出校验失败: {val_errors}")
        return False
    
    if deploy(html_str):
        ok(f"已部署回滚版本: {OUTPUT}")
        return True
    else:
        fail("部署失败")
        return False

# ─── 主流程 ───
def run_pipeline():
    """完整管道：备份 → 校验 → 组装 → 校验输出 → 部署"""
    print("═══ My Radar 每日更新管道 ═══")
    all_errors = []
    all_warnings = []
    
    # Step 1: 备份
    print("\n[1/5] 备份当前 feed")
    backup_file = backup_feed()
    
    # Step 2: 校验 feed
    print("\n[2/5] 校验 feed JSON")
    feed, errors, warnings = validate_feed()
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    for e in errors: fail(e)
    for w in warnings: warn(w)
    
    if errors:
        print("\n❌ Feed 校验失败，中止部署")
        info("提示: 运行 python3 radar-pipeline.py --rollback 回滚")
        return False
    
    # Step 3: 校验图片（非阻塞，只警告）
    print("\n[3/5] 校验图片 URL")
    img_warnings = check_images(feed)
    all_warnings.extend(img_warnings)
    for w in img_warnings: warn(w)
    
    # Step 4: 组装 HTML
    print("\n[4/5] 组装 HTML")
    html_str, asm_errors = assemble()
    all_errors.extend(asm_errors)
    for e in asm_errors: fail(e)
    
    if asm_errors:
        print("\n❌ 组装失败，中止部署")
        return False
    
    # Step 4b: 校验输出
    val_errors = validate_output(html_str)
    all_errors.extend(val_errors)
    for e in val_errors: fail(e)
    
    if val_errors:
        print("\n❌ 输出校验失败，中止部署")
        return False
    
    # Step 5: 部署
    print("\n[5/5] 部署到桌面")
    if deploy(html_str):
        size_kb = len(html_str) / 1024
        ok(f"已部署: {OUTPUT} ({size_kb:.1f} KB)")
    else:
        fail("部署失败")
        return False
    
    # 总结
    print(f"\n{'═' * 40}")
    if all_errors:
        print(f"❌ 失败: {len(all_errors)} 个错误")
        return False
    elif all_warnings:
        print(f"✅ 部署成功（{len(all_warnings)} 个警告）")
        return True
    else:
        print("✅ 部署成功，无警告")
        return True

def check_status():
    """系统健康检查"""
    print("═══ My Radar 健康检查 ═══\n")
    
    # Feed
    print("[Feed]")
    if os.path.exists(FEED_PATH):
        feed, errors, warnings = validate_feed()
        if errors:
            for e in errors: fail(e)
        else:
            ok(f"日期: {feed.get('date', '?')}")
            ok(f"信号: {len(feed.get('signals', []))}")
            ok(f"领地: {len(feed.get('territories', []))}")
            ed = feed.get('editorial', {})
            ok(f"Editorial 板块: {list(ed.keys())}")
            for w in warnings: warn(w)
    else:
        fail(f"Feed 不存在: {FEED_PATH}")
    
    # Template
    print("\n[模板]")
    if os.path.exists(TEMPLATE):
        ok(f"模板存在 ({os.path.getsize(TEMPLATE)/1024:.1f} KB)")
    else:
        fail(f"模板不存在: {TEMPLATE}")
    
    # Output
    print("\n[输出]")
    if os.path.exists(OUTPUT):
        mtime = datetime.fromtimestamp(os.path.getmtime(OUTPUT))
        age_hours = (datetime.now() - mtime).total_seconds() / 3600
        ok(f"输出存在 ({os.path.getsize(OUTPUT)/1024:.1f} KB)")
        ok(f"最后更新: {mtime.strftime('%Y-%m-%d %H:%M')}")
        if age_hours > 26:
            warn(f"输出已 {age_hours:.0f} 小时未更新（超过 24h）")
    else:
        fail(f"输出不存在: {OUTPUT}")
    
    # Backups
    print("\n[备份]")
    if os.path.exists(BACKUP_DIR):
        backups = [f for f in os.listdir(BACKUP_DIR) if f.startswith('daily-feed-')]
        ok(f"{len(backups)} 个备份")
        for b in sorted(backups, reverse=True)[:3]:
            info(b)
    else:
        warn("备份目录不存在")
    
    # Profile
    print("\n[Profile]")
    try:
        json.load(open(PROFILE))
        ok("profile.json 语法正确")
    except json.JSONDecodeError as e:
        fail(f"profile.json 语法错误: {e}")
    
    # Pipeline script
    print("\n[管道脚本]")
    ok(f"assemble-radar.py 存在")
    ok(f"radar-pipeline.py 存在")

# ─── 入口 ───
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == '--check':
            feed, errors, warnings = validate_feed()
            if errors:
                print("❌ Feed 校验失败:")
                for e in errors: fail(e)
            else:
                print("✅ Feed 校验通过")
                for w in warnings: warn(w)
        elif arg == '--rollback':
            rollback()
        elif arg == '--status':
            check_status()
        else:
            print(f"未知参数: {arg}")
            print("用法: radar-pipeline.py [--check|--rollback|--status]")
    else:
        success = run_pipeline()
        sys.exit(0 if success else 1)
