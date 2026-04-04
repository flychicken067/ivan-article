**English** | [中文](README.zh-CN.md)

# WeChat Article Pipeline

A Claude Code skill that handles the full production pipeline for WeChat public account articles — from raw input to a publish-ready package delivered to your phone via Telegram.

**Philosophy:** You spend your time on judgment. The pipeline handles research, writing, formatting, and delivery.

## What You Get

For each article, the skill produces:

- 📄 **Full article draft** — structured WeChat-format Markdown, with sourced data
- 🐦 **X/Twitter thread** — 5 tweets in Zara Zhang "Party not Stage" style
- 🖥 **Multi-channel HTML preview** — WeChat / X / Xiaohongshu / Zhishi Xingqiu in one page
- 📦 **Source folder** — every claim traced to government docs, official earnings, or primary reporting
- 📱 **Telegram delivery** — full package pushed to your phone, ready to copy-paste and publish

## How It Works

1. You send a raw input — a tweet link, podcast note, AI conversation excerpt, or book quote
2. The skill identifies the source type and framework tag automatically
3. Research phase: Tavily searches verify every number against primary sources
4. Article written in a fixed structure: hook → story → hidden angle → framework analysis → philosophical note → 3 questions for bosses → CTA
5. X thread written in Zara Zhang style: join conversations, don't lecture
6. HTML preview generated for all four channels
7. Everything pushed to your Telegram — you review, copy, publish

## Input Types

The skill is built around a "four-quarter time allocation" framework:

| Source | Signal | Output |
|--------|--------|--------|
| Twitter/X tweet | Link or screenshot | Research-backed article with hidden angle |
| Podcast note | Show name + episode | Core insight → business decision language |
| AI dialogue | Description of your Claude/GPT conversation | Institutional AI framework (unique content) |
| Book note | Title + chapter + excerpt | Eastern philosophy × AI governance (moat content) |

## Quick Start

### 1. Install

```bash
git clone https://github.com/flychicken067/ivan-article.git ~/.claude/skills/ivan-article
cd ~/.claude/skills/ivan-article
pip install requests
```

### 2. Set Up Telegram (optional but recommended)

```bash
cp .env.example .env
# Fill in TELEGRAM_BOT_TOKEN and PROJECT_ROOT
python3 telegram/get_chat_id.py   # sends your chat_id after you message your bot
python3 telegram/send.py --test   # verify connection
```

To create a Telegram bot: message [@BotFather](https://t.me/BotFather) → `/newbot`

### 3. Use

In Claude Code:

```
/ivan-article

Here's today's input:
[paste tweet / podcast note / AI dialogue / book excerpt]
```

Or invoke directly:
```
今天的素材是：[内容]
```

## Output Structure

The skill writes to your project directory:

```
output/
├── articles/
│   ├── article_08_medvi.md               ← Full article
│   ├── article_08_medvi_preview.html     ← Multi-channel preview
│   └── article_08_sources/
│       ├── 00_INDEX.md                   ← Source index + verification table
│       ├── 01_primary_source.md
│       └── ...
├── tweets/
│   └── article_08_thread.md              ← X thread (5 tweets)
└── publish-log.md                        ← Running record of all articles
```

## Source Verification Standards

Every number in every article must trace to a ⭐⭐⭐ or higher source:

| Rating | Source Type |
|--------|-------------|
| ⭐⭐⭐⭐⭐ | Government documents, official earnings reports, primary journalism, peer-reviewed papers |
| ⭐⭐⭐⭐ | Law firm analyses, specialist trade press |
| ⭐⭐⭐ | Major business media, first-person podcast quotes |
| ⭐⭐ | Secondary summaries, personal blogs |
| ⭐ | Unverifiable — flagged ⚠️, not used |

## Article Structure

Every article follows the same skeleton:

1. **Hook** (3–5 lines) — one fact that makes the reader need the next sentence
2. **Story** — enough detail to make it real
3. **Hidden angle** — what the mainstream coverage missed, backed by documents
4. **Framework analysis** — Three Bills (维护税/聚焦税/版权税) or organizational architecture
5. **Philosophical note** — Tao Te Ching / Sun Tzu × AI governance (≤100 words)
6. **Three questions for bosses** — not suggestions, interrogations
7. **CTA** — fixed format
8. **Sources** — numbered list

## X Thread Style

Built on Zara Zhang's "Party not Stage" framework:
- No numbering (not 1/5, 2/5...)
- Enter existing conversations, don't start lectures
- Personal voice ("In enterprise AI consulting, the question I get most is...")
- Each tweet stands alone
- Link only in the last tweet

## Requirements

- Claude Code (or compatible agent)
- Python 3.8+ with `requests` library
- Telegram bot (optional, for mobile delivery)
- Tavily MCP or web search capability for research phase

## Configuration

```env
# .env
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
PROJECT_ROOT=/path/to/your/project
```

## Telegram Scripts

| Script | Purpose |
|--------|---------|
| `telegram/send.py --article 08` | Push full article package to phone |
| `telegram/send.py --test` | Verify connection |
| `telegram/send.py "message"` | Send any text |
| `telegram/listen.py` | Listen for inputs from your phone |
| `telegram/get_chat_id.py` | One-time setup: get your chat ID |

## Example Output

**Article hook:**
> Matthew Gallagher, 41, launched a company from his living room in September 2024. $20,000. Two months. Zero employees.
>
> 2025 full-year revenue: $401 million. Net margin: 16.2%.
>
> The New York Times published a glowing profile on April 2, 2026.
>
> **Six weeks earlier, the FDA had sent a formal warning letter.**

**X thread tweet 3:**
> Nic Carter's tweet got 2.79M impressions.
>
> He asked: "first vibecoded billion-dollar company?"
>
> The part the NYT didn't write: the glowing profile ran 6 weeks after FDA warning letter #721455 landed at Medvi's door. Feb 20, 2026.

## License

MIT

---

Built by [@flychicken067](https://github.com/flychicken067)
