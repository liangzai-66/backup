#!/usr/bin/env python3
"""
新闻推送脚本 - 专业国际时事热点，全文翻译
每天 8:00, 12:00, 18:00 推送到钉钉
"""

import os
import subprocess
import json
import urllib.request
import re
import xml.etree.ElementTree as ET
import time
from datetime import datetime

# 确保日志目录存在（cron环境下尤为重要）
LOG_DIR = "/home/admin/.openclaw/workspace/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# 配置
DINGTALK_CHANNEL_ID = "cid5P1UzrvK7Xx2yiCGZVit+Q=="

def fetch_aljazeera():
    """获取Al Jazeera最新新闻 - 更新更快"""
    try:
        url = "https://www.aljazeera.com/xml/rss/all.xml"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            xml = response.read().decode('utf-8')
        
        root = ET.fromstring(xml)
        news = []
        for item in root.findall(".//item")[:8]:
            title = item.find("title")
            link = item.find("link")
            # 过滤视频类
            title_text = title.text if title is not None else ""
            if title_text and "video" not in title_text.lower():
                news.append({
                    "title": title_text,
                    "url": link.text if link is not None else ""
                })
        return news[:10]
    except Exception as e:
        print(f"Al Jazeera 获取失败: {e}")
        return []

def translate(text):
    """翻译文本到中文"""
    try:
        # 分段翻译，每段最多500字符
        if len(text) > 500:
            text = text[:500]
        
        text = urllib.parse.quote(text)
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|zh"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            result = data.get("responseData", {}).get("translatedText", "")
            if result:
                return result
        return text
    except Exception as e:
        print(f"翻译失败: {e}")
        return text

def fetch_article_content(url):
    """抓取文章内容"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # 提取段落
        paragraphs = re.findall(r'<p[^>]*>([^<]+)</p>', html)
        content = []
        for p in paragraphs:
            # 清理HTML实体
            p = p.replace('&#x27;', "'").replace('&amp;', '&').replace('&quot;', '"')
            p = p.replace('&lt;', '<').replace('&gt;', '>')
            if len(p) > 30 and 'BBC' not in p and 'Follow' not in p and 'Subscribe' not in p:
                content.append(p.strip())
            if len(content) >= 4:
                break
        
        full_content = " ".join(content)
        return full_content[:800] if full_content else ""
    except:
        return ""

def push_to_dingtalk(message, max_retries=3):
    """推送到钉钉群，带重试"""
    for attempt in range(1, max_retries + 1):
        try:
            print(f"📤 推送尝试 {attempt}/{max_retries}...")
            cmd = [
                "openclaw", "message", "send",
                "--channel", "dingtalk",
                "--target", DINGTALK_CHANNEL_ID,
                "--message", message
            ]
            result = subprocess.run(cmd, timeout=30, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                print(f"✅ 第 {attempt} 次推送成功")
                return True
            else:
                print(f"❌ 第 {attempt} 次失败")
        except Exception as e:
            print(f"❌ 第 {attempt} 次异常: {e}")
        
        if attempt < max_retries:
            time.sleep(attempt * 5)
    
    return False

def main():
    print(f"📰 获取专业新闻 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # 获取Al Jazeera最新新闻
    print("🌍 正在获取Al Jazeera最新新闻...")
    news_list = fetch_aljazeera()
    print(f"   获取到 {len(news_list)} 条")
    
    if not news_list:
        print("❌ 没有获取到任何新闻")
        return
    
    # 格式化消息 - 全文翻译
    message_lines = []
    message_lines.append(f"## 🌍 国际时事热点")
    message_lines.append(f"*{datetime.now().strftime('%Y-%m-%d %H:%M')} · Al Jazeera 最新*")
    message_lines.append("")
    
    for i, item in enumerate(news_list[:10], 1):
        title = item["title"]
        url = item["url"]
        
        print(f"   处理: {title[:40]}...")
        
        # 翻译标题
        title_cn = translate(title)
        
        # 获取文章内容并翻译
        content_cn = ""
        if url:
            content = fetch_article_content(url)
            if content:
                print(f"      翻译内容中...")
                content_cn = translate(content)
                time.sleep(0.5)  # 避免API限流
        
        message_lines.append(f"### {i}. {title_cn}")
        
        if content_cn:
            message_lines.append(f">{content_cn}")
        else:
            message_lines.append(f"🔗 [查看原文]({url})")
        
        message_lines.append("")
    
    message = "\n".join(message_lines)
    
    # 推送
    success = push_to_dingtalk(message, max_retries=3)
    if success:
        print("✅ 推送成功")
    else:
        print("❌ 推送失败")

if __name__ == "__main__":
    main()