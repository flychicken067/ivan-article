#!/usr/bin/env python3
"""
输入监听器：轮询 Telegram，把你发来的消息保存到 inbox/telegram/
用法：
  python3 telegram/listen.py         # 持续监听（Ctrl+C 停止）
  python3 telegram/listen.py --once  # 只取一次最新消息

消息格式（你在 Telegram 里发）：
  直接发链接：https://x.com/nic_carter/status/xxx
  带说明发：[twitter] https://x.com/... 今天的素材
  发文字：Nic Carter 推文说了什么什么，帮我写成文章
"""

import requests
import os
import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime

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
CHAT_ID = str(os.environ.get('TELEGRAM_CHAT_ID', ''))
ROOT    = Path(os.environ.get('PROJECT_ROOT',
               '/Users/ivan/Desktop/AI-Native-Projects/my-first-project'))
INBOX   = ROOT / 'inbox' / 'telegram'
OFFSET_FILE = Path(__file__).parent / '.last_offset'

INBOX.mkdir(parents=True, exist_ok=True)

# ── API ────────────────────────────────────────────────────────────────────
def get_updates(offset=None):
    url    = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
    params = {'timeout': 20, 'allowed_updates': ['message']}
    if offset:
        params['offset'] = offset
    try:
        resp = requests.get(url, params=params, timeout=30)
        return resp.json()
    except Exception as e:
        print(f'⚠️  网络错误: {e}')
        return {'ok': False, 'result': []}

def send_ack(text: str):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    requests.post(url, data={
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }, timeout=10)

# ── 消息处理 ───────────────────────────────────────────────────────────────
def process_message(message: dict):
    """把收到的消息保存到 inbox，等待 Claude 处理"""
    text    = message.get('text', '')
    photo   = message.get('photo')
    caption = message.get('caption', '')
    chat_id = str(message.get('chat', {}).get('id', ''))

    # 只处理自己发的消息
    if chat_id != CHAT_ID:
        return

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    content   = text or caption or ''

    if not content and not photo:
        return

    # 写入 inbox
    inbox_data = {
        'timestamp': timestamp,
        'type': 'photo' if photo else 'text',
        'content': content,
        'raw': message
    }

    inbox_file = INBOX / f'input_{timestamp}.json'
    inbox_file.write_text(json.dumps(inbox_data, ensure_ascii=False, indent=2))

    # 同时写一个纯文本版（方便 Claude 直接读）
    text_file = INBOX / f'input_{timestamp}.txt'
    text_file.write_text(content)

    print(f'📥 [{timestamp}] 收到输入: {content[:80]}...' if len(content) > 80 else f'📥 [{timestamp}] 收到输入: {content}')

    # 回复确认
    send_ack(f'📥 收到！\n\n`{content[:200]}`\n\n已保存到 inbox，等待处理...')

    return inbox_file

# ── 主循环 ─────────────────────────────────────────────────────────────────
def main():
    if not TOKEN or TOKEN == '你的token放这里':
        print('❌ 请先在 .env 里填写 TELEGRAM_BOT_TOKEN')
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true', help='只取一次，不持续监听')
    args = parser.parse_args()

    # 读取上次的 offset
    offset = None
    if OFFSET_FILE.exists():
        try:
            offset = int(OFFSET_FILE.read_text().strip())
        except:
            pass

    print(f'👂 开始监听 Telegram 消息... (Ctrl+C 停止)')
    print(f'   inbox 目录: {INBOX}')

    try:
        while True:
            data = get_updates(offset)
            if data.get('ok') and data.get('result'):
                for update in data['result']:
                    offset = update['update_id'] + 1
                    OFFSET_FILE.write_text(str(offset))

                    message = update.get('message', {})
                    if message:
                        process_message(message)

            if args.once:
                break

            time.sleep(2)

    except KeyboardInterrupt:
        print('\n⏹  监听已停止')

if __name__ == '__main__':
    main()
