#!/usr/bin/env python3
"""
第一步工具：获取你的 Telegram Chat ID
用法：
  1. 先在 .env 里填好 TELEGRAM_BOT_TOKEN
  2. 在 Telegram 里给你的 bot 发任意消息（比如 "hello"）
  3. 运行：python3 telegram/get_chat_id.py
  4. 把打印出的 chat_id 填进 .env 的 TELEGRAM_CHAT_ID
"""

import requests
import os
import sys
from pathlib import Path

# 加载 .env
env_file = Path(__file__).parent.parent / '.env'
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip(), v.strip())

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
if not TOKEN or TOKEN == '你的token放这里':
    print("❌ 请先在 .env 文件里填写 TELEGRAM_BOT_TOKEN")
    sys.exit(1)

print(f"🔍 正在查询 bot: {TOKEN[:10]}...")

resp = requests.get(f'https://api.telegram.org/bot{TOKEN}/getUpdates', timeout=10)
data = resp.json()

if not data.get('ok'):
    print(f"❌ Token 无效或请求失败: {data}")
    sys.exit(1)

updates = data.get('result', [])
if not updates:
    print("⚠️  没有收到任何消息。")
    print("   → 请先在 Telegram 里给你的 bot 发一条消息，然后再运行这个脚本。")
    sys.exit(1)

# 取最新一条消息的 chat_id
latest = updates[-1]
message = latest.get('message', {})
chat = message.get('chat', {})
chat_id = chat.get('id')
name = chat.get('first_name', '') + ' ' + chat.get('last_name', '')
username = chat.get('username', '')

print(f"\n✅ 找到消息！")
print(f"   发送人: {name.strip()} (@{username})")
print(f"   Chat ID: {chat_id}")
print(f"\n👉 把这个 Chat ID 填进 .env 的 TELEGRAM_CHAT_ID={chat_id}")
