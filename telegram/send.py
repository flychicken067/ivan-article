#!/usr/bin/env python3
"""
发送工具：Claude 调用这个脚本向你的 Telegram 推送内容
用法：
  python3 telegram/send.py "消息内容"
  python3 telegram/send.py --file path/to/file.md
  python3 telegram/send.py --article 08  # 发送完整文章包
"""

import requests
import os
import sys
import argparse
from pathlib import Path

# ── 加载 .env ──────────────────────────────────────────────────────────────
def load_env():
    env_file = Path(__file__).parent.parent / '.env'
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())

load_env()

TOKEN   = os.environ.get('TELEGRAM_BOT_TOKEN', '')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')
ROOT    = Path(os.environ.get('PROJECT_ROOT',
               '/Users/ivan/Desktop/AI-Native-Projects/my-first-project'))

# ── Telegram API helpers ───────────────────────────────────────────────────
def send_text(text: str, parse_mode: str = 'Markdown') -> bool:
    """发送文字消息（自动分割超过 4000 字符的内容）"""
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
    ok = True
    for chunk in chunks:
        resp = requests.post(url, data={
            'chat_id': CHAT_ID,
            'text': chunk,
            'parse_mode': parse_mode
        }, timeout=15)
        if not resp.json().get('ok'):
            # 降级：去掉 parse_mode 重试
            resp2 = requests.post(url, data={
                'chat_id': CHAT_ID,
                'text': chunk,
            }, timeout=15)
            ok = ok and resp2.json().get('ok', False)
    return ok

def send_file(file_path: Path, caption: str = '') -> bool:
    """发送文件附件"""
    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'
    with open(file_path, 'rb') as f:
        resp = requests.post(url,
            data={'chat_id': CHAT_ID, 'caption': caption},
            files={'document': (file_path.name, f)},
            timeout=30)
    return resp.json().get('ok', False)

# ── 文章包发送逻辑 ─────────────────────────────────────────────────────────
def send_article_package(article_num: str):
    """
    发送完整文章包，包括：
    1. 概要卡片（标题/副标题/框架/发布日期）
    2. 公众号正文 .md 文件
    3. X Thread 文件
    4. 审核清单
    """
    num = article_num.zfill(2)

    # 找文章文件（支持 article_08_medvi.md 这种带 topic 后缀的）
    articles_dir = ROOT / 'output' / 'articles'
    article_files = list(articles_dir.glob(f'article_{num}_*.md'))
    # 排除 _caio 等草稿（取最新修改的那个）
    article_files = [f for f in article_files if 'preview' not in f.name]
    if not article_files:
        send_text(f'❌ 找不到 Article {num} 的文章文件')
        return
    article_file = sorted(article_files, key=lambda f: f.stat().st_mtime)[-1]

    # 找 Thread 文件
    tweets_dir   = ROOT / 'output' / 'tweets'
    thread_files = list(tweets_dir.glob(f'article_{num}_thread*.md'))
    thread_file  = thread_files[0] if thread_files else None

    # ── 读取文章元信息 ──
    content = article_file.read_text(encoding='utf-8')
    lines   = content.splitlines()

    title    = next((l.lstrip('# ') for l in lines if l.startswith('# ')), '（无标题）')
    subtitle = next((l.lstrip('**副标题**：').strip('*') for l in lines
                     if '副标题' in l), '')
    platform = next((l.lstrip('**发布平台**：').strip('*') for l in lines
                     if '发布平台' in l), '微信公众号')
    pub_date = next((l.lstrip('**计划发布**：').strip('*') for l in lines
                     if '计划发布' in l), '')
    tags     = next((l.lstrip('**框架标签**：').strip('*') for l in lines
                     if '框架标签' in l), '')

    # ── 消息 1：概要卡片 ──
    card = f"""📦 *Article {num} · 发布包*

📌 *标题*
{title}

📝 *副标题*
{subtitle}

🏷 框架：{tags}
📅 计划：{pub_date}
📢 平台：{platform}

---
⬇️ 正在发送文件..."""

    send_text(card)

    # ── 消息 2：公众号正文文件 ──
    ok = send_file(article_file, caption=f'公众号正文 · Article {num}')
    if ok:
        send_text('✅ 公众号正文已发送（直接复制 ## 正文 以下内容粘贴进公众号编辑器）')

    # ── 消息 3：X Thread ──
    if thread_file:
        send_file(thread_file, caption=f'X Thread · Article {num}')
        # 同时发纯文本方便直接复制推文
        thread_content = thread_file.read_text(encoding='utf-8')
        # 提取5条推文（两个 --- 之间的内容）
        parts = thread_content.split('\n---\n')
        tweets = [p.strip() for p in parts if p.strip()
                  and not p.strip().startswith('#')
                  and not p.strip().startswith('**')
                  and len(p.strip()) > 20]
        if tweets:
            tweet_text = '🐦 *X Thread（可直接发推）*\n\n'
            for i, t in enumerate(tweets[:5], 1):
                tweet_text += f'*{i}/*\n{t}\n\n'
            send_text(tweet_text)

    # ── 消息 4：审核清单 ──
    checklist = f"""✅ *发布前审核清单 · Article {num}*

公众号
☐ 标题是否有吸引力
☐ 数据来源是否已核实（见 article_{num}_sources/）
☐ CTA 二维码是否有效（检查过期时间）
☐ 封面图是否已准备

X Thread
☐ 5 条推文是否每条独立站得住
☐ 最后一条链接是否已替换为公众号发布后的真实 URL
☐ 发布后搜索相关话题回复 3 条

发布后
☐ 在 publish-log.md 记录发布 URL
☐ 24h 后回填阅读/点赞/转发数据"""

    send_text(checklist)
    send_text(f'🚀 Article {num} 发布包发送完毕。审核后直接复制发布。')

# ── 主入口 ─────────────────────────────────────────────────────────────────
def main():
    if not TOKEN or TOKEN == '你的token放这里':
        print('❌ 请先在 .env 里填写 TELEGRAM_BOT_TOKEN')
        sys.exit(1)
    if not CHAT_ID or CHAT_ID == '你的chat_id放这里':
        print('❌ 请先运行 python3 telegram/get_chat_id.py 获取 Chat ID')
        sys.exit(1)

    parser = argparse.ArgumentParser(description='发送内容到 Telegram')
    parser.add_argument('message', nargs='?', help='要发送的文字消息')
    parser.add_argument('--file',    help='发送文件路径')
    parser.add_argument('--article', help='发送完整文章包（传入文章编号，如 08）')
    parser.add_argument('--test',    action='store_true', help='发送测试消息验证连接')
    args = parser.parse_args()

    if args.test:
        ok = send_text('✅ Telegram 连接成功！Ivan 的文章助手已就绪。')
        print('✅ 测试消息发送成功' if ok else '❌ 发送失败，检查 token 和 chat_id')

    elif args.article:
        send_article_package(args.article)
        print(f'✅ Article {args.article} 发布包已推送到 Telegram')

    elif args.file:
        path = Path(args.file)
        if not path.exists():
            print(f'❌ 文件不存在：{args.file}')
            sys.exit(1)
        ok = send_file(path)
        print('✅ 文件已发送' if ok else '❌ 发送失败')

    elif args.message:
        ok = send_text(args.message)
        print('✅ 消息已发送' if ok else '❌ 发送失败')

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
