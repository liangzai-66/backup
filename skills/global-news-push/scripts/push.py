#!/usr/bin/env python3
"""
全球热点新闻推送脚本
抓取全球权威媒体的最新资讯，整合为中文简报推送到钉钉群
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta

# 配置
SEARXNG_URL = os.environ.get("SEARXNG_URL", "http://localhost:8080")
DINGTALK_CHANNEL_ID = "cid5P1UzrvK7Xx2yiCGZVit+Q=="  # 钉钉群「时事热点」

# 信息来源配置
NEWS_SOURCES = {
    "政治要闻": {
        "sources": ["reuters.com", "apnews.com", "bbc.com", "afp.com"],
        "keywords": ["国际新闻", "时事热点", "政治新闻", "外交", "峰会"],
        "limit": 3
    },
    "军事动态": {
        "sources": ["janes.com", "defensenews.com", "huanqiu.com"],
        "keywords": ["军事新闻", "国防", "军演", "武器", "安全"],
        "limit": 3
    },
    "财经资讯": {
        "sources": ["bloomberg.com", "ft.com", "wsj.com", "caixin.com"],
        "keywords": ["财经新闻", "股市", "经济", "金融", "投资"],
        "limit": 3
    },
    "科技前沿": {
        "sources": ["techcrunch.com", "theverge.com", "technologyreview.com", "36kr.com"],
        "keywords": ["科技新闻", "AI", "人工智能", "芯片", "创新"],
        "limit": 3
    },
    "娱乐八卦": {
        "sources": ["variety.com", "tmz.com", "weibo.com"],
        "keywords": ["娱乐新闻", "明星", "电影", "八卦", "热搜"],
        "limit": 3
    }
}

def search_news(query, num_results=10):
    """使用 searxng 搜索新闻（仅当天内容，仅中文）"""
    try:
        cmd = [
            "/home/admin/.local/bin/uv", "run",
            "/home/admin/.openclaw/workspace/skills/searxng/scripts/searxng.py",
            "search", query,
            "-n", str(num_results),
            "--format", "json",
            "--time-range", "day",
            "--language", "zh"
        ]
        env = os.environ.copy()
        env["SEARXNG_URL"] = SEARXNG_URL
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, env=env)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            results = data.get("results", [])
            # 二次过滤：确保内容包含中文
            zh_results = []
            for item in results:
                title = item.get("title", "")
                content = item.get("content", "")
                if any('\u4e00' <= c <= '\u9fff' for c in title) or any('\u4e00' <= c <= '\u9fff' for c in content):
                    zh_results.append(item)
            return zh_results
        else:
            print(f"搜索失败：{result.stderr}", file=sys.stderr)
            return []
    except Exception as e:
        print(f"搜索异常：{e}", file=sys.stderr)
        return []

def push_to_dingtalk(message):
    """推送到钉钉群"""
    try:
        max_len = 3500
        if len(message) > max_len:
            message = message[:max_len] + "\n\n... 消息过长，已截断"
        
        cmd = [
            "openclaw", "message", "send",
            "--channel", "dingtalk",
            "--target", DINGTALK_CHANNEL_ID,
            "--message", message
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ 推送成功")
            return True
        else:
            print(f"推送失败：{result.stderr}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"推送异常：{e}", file=sys.stderr)
        return False

def main():
    print(f"🕐 开始抓取全球热点新闻 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_news = {}
    
    # 遍历每个领域
    for category, config in NEWS_SOURCES.items():
        limit = config["limit"]
        keywords = config["keywords"]
        print(f"\n📰 搜索领域：{category} (限{limit}条)")
        
        category_news = []
        for keyword in keywords:
            results = search_news(keyword, num_results=5)
            for item in results:
                if item.get("title") and item.get("url"):
                    category_news.append(item)
        
        # 去重
        seen_urls = set()
        unique_news = []
        for item in category_news:
            url = item.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_news.append(item)
        
        category_news = unique_news[:limit]
        all_news[category] = category_news
        print(f"  找到 {len(category_news)} 条新闻")
    
    # 格式化消息
    message_lines = [
        f"📰 **全球热点新闻简报**",
        f"🕐 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"━━━━━━━━━━━━━━━━━━"
    ]
    
    category_emojis = {
        "政治要闻": "🏛️",
        "军事动态": "⚔️",
        "财经资讯": "💹",
        "科技前沿": "🔬",
        "娱乐八卦": "🎬"
    }
    
    all_items = []
    
    for category, news_list in all_news.items():
        if news_list:
            emoji = category_emojis.get(category, "📌")
            message_lines.append(f"\n{emoji} **【{category}】**")
            
            for i, item in enumerate(news_list, 1):
                title = item.get("title", "无标题").replace("\n", " ").strip()
                if len(title) > 60:
                    title = title[:57] + "..."
                
                content = item.get("content", "").replace("\n", " ").strip()
                if len(content) > 100:
                    content = content[:97] + "..."
                
                url = item.get("url", "")
                engines = item.get("engines", [])
                source = engines[0] if engines else "未知"
                
                message_lines.append(f"")
                message_lines.append(f"{i}️⃣ {title}")
                message_lines.append(f"📍 来源：{source} | ⏰ {datetime.now().strftime('%H:%M')}")
                if content:
                    message_lines.append(f"📝 摘要：{content}")
                if url:
                    message_lines.append(f"🔗 {url}")
                
                all_items.append({"title": title, "source": source, "url": url})
    
    # 热度榜 TOP 3
    if len(all_items) >= 3:
        message_lines.append(f"\n━━━━━━━━━━━━━━━━━━")
        message_lines.append(f"📊 **今日热度榜 TOP 3**")
        message_lines.append(f"🥇 {all_items[0]['title']}")
        message_lines.append(f"🥈 {all_items[1]['title']}")
        message_lines.append(f"🥉 {all_items[2]['title']}")
        message_lines.append(f"\n💡 **编辑点评：**")
        message_lines.append(f"今日全球热点主要集中在政治、科技和财经领域，请持续关注后续发展。")
    
    message = "\n".join(message_lines)
    
    # 推送
    print(f"\n📤 推送消息到钉钉群...")
    success = push_to_dingtalk(message)
    
    if not success:
        simple_msg = f"📰 全球热点新闻简报\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n✅ 已抓取 {len(all_items)} 条热点新闻。"
        print("🔄 发送极简版...")
        push_to_dingtalk(simple_msg)
    
    print("\n✅ 完成")

if __name__ == "__main__":
    main()