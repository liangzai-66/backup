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

# 每个领域的推送条数
TOPIC_LIMITS = {
    "国际时事": 10,
    "科技前沿": 5,
    "财经动态": 5,
    "娱乐八卦": 5
}

# 搜索领域和关键词
# 数据源：X 平台 (Twitter) + Facebook + 路透社 (Reuters) + 微博热搜
# 说明：腾讯微博已于 2020 年停止服务，无法获取
TOPICS = {
    "国际时事": [
        "site:reuters.com 国际新闻 中文",
        "X Twitter 国际时事 热点",
        "Facebook 全球新闻",
        "国际局势 最新消息"
    ],
    "科技前沿": [
        "site:reuters.com 科技",
        "X Twitter AI 人工智能",
        "Facebook 科技创新",
        "科技新闻 突破"
    ],
    "财经动态": [
        "site:reuters.com 财经 股票",
        "X Twitter 股市 金融",
        "Facebook 经济数据",
        "财经新闻 市场"
    ],
    "娱乐八卦": [
        "微博热搜 娱乐 top5",
        "X Twitter 明星 娱乐",
        "Facebook celebrity",
        "娱乐八卦 热点"
    ]
}

def search_news(query, num_results=10):
    """使用 searxng 搜索新闻（仅当天内容）"""
    try:
        cmd = [
            "uv", "run",
            "/home/admin/.openclaw/workspace/skills/searxng/scripts/searxng.py",
            "search", query,
            "-n", str(num_results),
            "--format", "json",
            "--time-range", "day"  # 只搜索当天内容
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
        limit = TOPIC_LIMITS.get(topic, 5)  # 获取该领域的条数限制
        print(f"\n📰 搜索领域：{topic} (限{limit}条)")
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
        
        # 按配置的条数限制截取
        topic_news = unique_news[:limit]
        all_news.append((topic, topic_news))
        total_count += len(topic_news)
        print(f"  找到 {len(topic_news)} 条新闻")
    
    # 格式化消息 - 中文摘要版
    message_lines = [
        f"📰 时事热点速递",
        f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"📊 共 {total_count} 条热点\n"
    ]
    
    for topic, news_list in all_news:
        if news_list:
            message_lines.append(f"🔹 {topic}")
            for i, item in enumerate(news_list, 1):
                title = item.get("title", "无标题")
                content = item.get("content", "")
                
                # 清理标题中的换行
                title = title.replace("\n", " ").strip()
                if len(title) > 50:
                    title = title[:47] + "..."
                
                # 中文摘要处理
                summary = content.replace("\n", " ").strip() if content else ""
                if len(summary) > 80:
                    summary = summary[:77] + "..."
                
                message_lines.append(f"  {i}. {title}")
                if summary:
                    message_lines.append(f"     {summary}")
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
