[English](README.md) | **中文**

# 公众号文章流水线

一个 Claude Code skill，把公众号文章的完整生产流程自动化——从原始素材到发布包，全部推送到你手机的 Telegram，你只需要审核和发布。

**核心哲学：你的精力花在判断上。研究、写作、排版、推送，流水线来做。**

## 你会得到什么

每篇文章，skill 产出：

- 📄 **公众号正文**——结构化 Markdown，所有数字有来源
- 🐦 **X / 推特 Thread**——5 条，Zara Zhang "派对不是舞台"风格
- 🖥 **多渠道 HTML 预览**——公众号 / X / 小红书 / 知识星球 四合一
- 📦 **来源文件夹**——每一个数字追溯到政府文件、官方财报或一手报道
- 📱 **Telegram 推送**——完整发布包到你手机，复制粘贴即可发布

## 使用方式

1. 给 Claude 发一条素材：推文链接、播客笔记、AI 对话摘录、旧书原文
2. Skill 自动判断素材类型和框架标签
3. Tavily 搜索核实所有关键数字，建立来源文件夹
4. 按固定结构写文章：钩子 → 故事 → 隐藏角度 → 框架分析 → 哲学注解 → 三个追问 → CTA
5. 写 X Thread，Zara Zhang 风格：加入对话，不是开讲座
6. 生成四渠道 HTML 预览
7. 全部推送到你的 Telegram，审核后自己发布

## 四种输入类型

Skill 围绕「四分之一时间分配框架」设计：

| 来源 | 信号 | 产出 |
|------|------|------|
| Twitter/X 推文 | 链接或截图 | 有隐藏角度的研究型文章 |
| 播客笔记 | 节目名 + 集数 | 核心观点 → 企业决策语言 |
| AI 对话 | 你和 Claude/GPT 的对话摘录 | 「把 AI 对话转成机构价值框架」——护城河内容 |
| 旧书笔记 | 书名 + 章节 + 原文 | 东方哲学 × AI 治理 = 不可复制内容 |

## 安装

```bash
git clone https://github.com/flychicken067/ivan-article.git ~/.claude/skills/ivan-article
cd ~/.claude/skills/ivan-article
pip install requests
```

## Telegram 配置（推荐，5 分钟）

```bash
cp .env.example .env
# 打开 .env，填入 TELEGRAM_BOT_TOKEN 和 PROJECT_ROOT
python3 telegram/get_chat_id.py   # 先给你的 bot 发一条消息，再运行
python3 telegram/send.py --test   # 验证连接
```

创建 Telegram bot：Telegram 搜索 [@BotFather](https://t.me/BotFather) → `/newbot`，2 分钟拿到 token。

## 使用

在 Claude Code 里：
```
/ivan-article

今天的素材是：[粘贴推文 / 播客笔记 / AI 对话 / 书摘]
```

## 文章结构（固定框架）

每篇文章都遵循同一骨架：

1. **钩子**（3-5 行）——一个让读者必须看下一句的事实
2. **故事展开**——给够细节，让读者相信这件事是真的
3. **隐藏角度**——主流报道没写的那部分，用文件/数据支撑
4. **框架分析**——三张账单（维护税/聚焦税/版权税）或组织架构框架
5. **哲学注解**——《道德经》/《孙子兵法》× AI 治理（≤100 字）
6. **给中国老板的三个问题**——不是建议，是追问
7. **CTA**——固定格式
8. **数据来源**——编号列表

## 数据核实标准

文章里每一个数字都必须追溯到 ⭐⭐⭐ 及以上来源：

| 级别 | 来源类型 |
|------|---------|
| ⭐⭐⭐⭐⭐ | 政府文件、官方财报、一手新闻报道、同行评审论文 |
| ⭐⭐⭐⭐ | 法律事务所分析、专业行业媒体 |
| ⭐⭐⭐ | 主流商业媒体、播客原话 |
| ⭐⭐ | 二手摘要 |
| ⭐ | 无法核实——标注 ⚠️，不使用 |

## 输出文件结构

```
output/
├── articles/
│   ├── article_08_medvi.md               ← 公众号正文
│   ├── article_08_medvi_preview.html     ← 多渠道预览
│   └── article_08_sources/
│       ├── 00_INDEX.md                   ← 来源索引 + 数字核实表
│       ├── 01_主要来源.md
│       └── ...
├── tweets/
│   └── article_08_thread.md              ← X Thread（5 条）
└── publish-log.md                        ← 所有文章的发布记录
```

## X Thread 风格

基于 Zara Zhang 的「派对不是舞台」框架：
- 不加编号（不写 1/5、2/5）
- 加入正在发生的对话，不是上台讲课
- 用个人语气（「做企业 AI 咨询，这几个月被问最多的问题是...」）
- 每条推文独立站得住
- 链接只放最后一条

## 环境要求

- Claude Code（或兼容的 AI agent）
- Python 3.8+，安装 `requests` 库
- Telegram bot（可选，用于手机推送）
- Tavily MCP 或 web search 能力（用于研究阶段）

## 许可

MIT

---

由 [@flychicken067](https://github.com/flychicken067) 构建
