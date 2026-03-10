#!/usr/bin/env python3
"""
时事热点推送脚本
每天定时抓取国际时事、科技、财经、八卦热点新闻，推送到钉钉群
"""

import os
import sys
import json
import subprocess
from datetime import datetime

# 配置
SEARXNG_URL = os.environ.get("SEARXNG_URL", "http://localhost:8080")
DINGTALK_CHANNEL_ID = "cid5P1UzrvK7Xx2yiCGZVit+Q=="  # 钉钉群「时事热点」

# 搜索领域和关键词（含指定数据源）
# 说明：腾讯微博已于 2020 年停止服务，无法获取
# X (Twitter) 和 Facebook 内容通过 SearXNG 聚合搜索获取
TOPICS = {
    "国际时事": [
        "site:reuters.com world news",
        "X Twitter 国际新闻 2026",
        "global politics 2026",
        "world news today"
    ],
    "科技前沿": [
        "site:reuters.com technology",
        "X Twitter AI artificial intelligence",
        "tech breakthrough 2026",
        "科技新闻"
    ],
    "财经动态": [
        "site:reuters.com finance OR stock market",
        "X Twitter 财经 OR 股票",
        "stock market today",
        "financial news 2026"
    ],
    "娱乐八卦": [
        "X Twitter celebrity gossip",
        "微博热搜 娱乐 2026",
        "明星八卦",
        "entertainment news 2026"
    ]
}

def search_news(query, num_results=10):
    """使用 searxng 搜索新闻"""
    try:
        cmd = [
            "uv", "run",
            "/home/admin/.openclaw/workspace/skills/searxng/scripts/searxng.py",
            "search", query,
            "-n", str(num_results),
            "--format", "json"
        ]
        env = os.environ.copy()
        env["SEARXNG_URL"] = SEARXNG_URL
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, env=env)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("results", [])
        else:
            print(f"搜索失败：{result.stderr}", file=sys.stderr)
            return []
    except Exception as e:
        print(f"搜索异常：{e}", file=sys.stderr)
        return []

def push_to_dingtalk(message):
    """推送到钉钉群"""
    try:
        # 截断过长的消息（钉钉有长度限制）
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
    print(f"🕐 开始抓取时事热点 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_news = []
    total_count = 0
    
    # 遍历每个领域
    for topic, queries in TOPICS.items():
        print(f"\n📰 搜索领域：{topic}")
        topic_news = []
        
        # 每个领域用多个关键词搜索，取最佳结果
        for query in queries:
            results = search_news(query, num_results=5)
            if results:
                for item in results[:5]:
                    if item.get("title") and item.get("url"):
                        topic_news.append(item)
        
        # 去重（按 URL）
        seen_urls = set()
        unique_news = []
        for item in topic_news:
            url = item.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_news.append(item)
        
        # 取前 10 条
        topic_news = unique_news[:10]
        all_news.append((topic, topic_news))
        total_count += len(topic_news)
        print(f"  找到 {len(topic_news)} 条新闻")
    
    # 格式化消息 - 简洁版
    message_lines = [
        f"📰 时事热点速递",
        f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"📊 共 {total_count} 条热点\n"
    ]
    
    for topic, news_list in all_news:
        if news_list:
            message_lines.append(f"🔹 {topic}")
            for i, item in enumerate(news_list[:8], 1):  # 每个领域最多 8 条，避免过长
                title = item.get("title", "无标题")
                url = item.get("url", "")
                
                # 清理标题中的换行
                title = title.replace("\n", " ").strip()
                if len(title) > 60:
                    title = title[:57] + "..."
                
                message_lines.append(f"  {i}. {title}")
                if url:
                    # 短链接显示
                    short_url = url[:50] + "..." if len(url) > 50 else url
                    message_lines.append(f"     🔗 {short_url}")
            message_lines.append("")
    
    message = "\n".join(message_lines)
    
    # 推送
    print(f"\n📤 推送消息到钉钉群...")
    success = push_to_dingtalk(message)
    
    if not success:
        # 发送极简版
        simple_msg = f"📰 时事热点速递\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n✅ 今日热点已抓取完成，共 {total_count} 条新闻。"
        print("🔄 发送极简版...")
        push_to_dingtalk(simple_msg)
    
    print("\n✅ 完成")

if __name__ == "__main__":
    main()
