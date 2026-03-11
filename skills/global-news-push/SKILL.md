---
name: global-news-push
description: 全球热点新闻推送技能。定时或手动抓取全球权威媒体的最新资讯，整合为中文简报推送到钉钉群。支持政治/时事、军事、财经、科技、娱乐八卦等领域。使用场景：(1) 用户要求推送最新新闻 (2) 用户询问全球热点 (3) 定时推送任务触发 (4) 用户要求抓取特定领域新闻。
---

# 全球热点新闻推送

专业的全球新闻编辑，精通多语言资讯整合，将全球权威媒体的最新资讯以简洁、准确的中文呈现。

## 推送配置

- **推送频率**: 每日 8:00 / 12:00 / 18:00（可自定义）
- **时效范围**: 过去 6 小时内最新资讯
- **输出语言**: 简体中文
- **推送渠道**: 钉钉群「时事热点」cid5P1UzrvK7Xx2yiCGZVit+Q==

## 信息来源（按优先级）

### 政治/时事类
- Reuters（路透社）| reuters.com
- AP News（美联社）| apnews.com
- BBC News | bbc.com/news
- 法新社 AFP | afp.com

### 军事类
- Jane's Defence | janes.com
- Defense News | defensenews.com
- 环球网军事频道 | huanqiu.com

### 财经类
- Bloomberg（彭博社）| bloomberg.com
- Financial Times | ft.com
- 华尔街日报 WSJ | wsj.com
- 财新网 | caixin.com

### 科技类
- TechCrunch | techcrunch.com
- The Verge | theverge.com
- MIT Technology Review | technologyreview.com
- 36氪 | 36kr.com

### 娱乐八卦类
- Variety | variety.com
- TMZ | tmz.com
- 娱乐圈热搜榜
- 微博热搜 TOP10

## 输出格式

```
📰 **全球热点新闻简报**
🕐 更新时间：[当前时间]
━━━━━━━━━━━━━━━━━━

🏛️ **【政治要闻】**
1️⃣ [标题]
 📍 来源：[媒体名] | ⏰ [发布时间]
 📝 摘要：[100字以内核心内容]
 🔗 [原文链接]

⚔️ **【军事动态】**
（同上格式，2-3条）

💹 **【财经资讯】**
（同上格式，2-3条）

🔬 **【科技前沿】**
（同上格式，2-3条）

🎬 **【娱乐八卦】**
（同上格式，2-3条）

━━━━━━━━━━━━━━━━━━
📊 **今日热度榜 TOP 3**
🥇 [最热新闻]
🥈 [次热新闻] 
🥉 [第三热点]

💡 **编辑点评：**
[用3句话总结今日全球大事走势]
```

## 质量标准

✅ 必须是过去 6 小时内的新鲜资讯
✅ 每条新闻必须标注信息来源
✅ 翻译准确，避免机器翻译腔
✅ 敏感信息客观呈现，不带立场
✅ 摘要控制在 100 字以内，精准传递核心信息

## 执行脚本

运行推送脚本：

```bash
/home/admin/.local/bin/uv run /home/admin/.openclaw/workspace/skills/global-news-push/scripts/push.py
```

## 定时任务配置

crontab 已配置为每天 8:00、12:00、18:00 自动推送。