#!/usr/bin/env python3
"""
天气推送脚本 - 每天早上7:50推送到钉钉
"""

import os
import subprocess
import json
from datetime import datetime

# 配置
LOCATION = "杭州市余杭区五常街道"
DINGTALK_CHANNEL_ID = "cid5P1UzrvK7Xx2yiCGZVit+Q=="

def get_weather():
    """通过 wttr.in 获取天气"""
    import urllib.request
    import urllib.parse
    
    # 获取实时天气
    url = f"https://wttr.in/{urllib.parse.quote(LOCATION)}?format=j1&lang=zh"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            
        current = data.get("current_condition", [{}])[0]
        
        # 解析数据 - weatherDesc 是数组，取第一个并提取 value
        temp = current.get("temp_C", "N/A")
        feels_like = current.get("FeelsLikeC", "N/A")
        humidity = current.get("humidity", "N/A")
        wind = current.get("windspeedKmph", "N/A")
        weather_desc = current.get("weatherDesc", [])
        if weather_desc and isinstance(weather_desc[0], dict):
            weather = weather_desc[0].get("value", "N/A")
        else:
            weather = str(weather_desc[0]) if weather_desc else "N/A"
        
        # 中英文天气对照
        weather_map = {
            "Sunny": "晴天",
            "Clear": "晴朗",
            "Partly cloudy": "多云",
            "Cloudy": "阴天",
            "Overcast": "阴",
            "Mist": "雾",
            "Fog": "大雾",
            "Light drizzle": "小毛毛雨",
            "Patchy light drizzle": "零星小毛雨",
            "Patchy rain nearby": "附近有零星雨",
            "Rain": "雨",
            "Light rain": "小雨",
            "Moderate rain": "中雨",
            "Heavy rain": "大雨",
            "Thunderstorm": "雷暴",
            "Snow": "雪",
            "Light snow": "小雪",
            "Heavy snow": "大雪",
            "Sleet": "雨夹雪",
        }
        weather_cn = weather_map.get(weather, weather)
        uv = current.get("UVindex", "N/A")
        
        # 获取今天和明天预报
        weather_data = data.get("weather", [])
        today = weather_data[0] if weather_data else {}
        
        # 获取当天最低和最高温度
        maxtemp = today.get("maxtempC", "N/A")
        mintemp = today.get("mintempC", "N/A")
        
        return {
            "location": LOCATION,
            "temp": temp,
            "feels_like": feels_like,
            "humidity": humidity,
            "wind": wind,
            "weather": weather_cn,
            "uv": uv,
            "today": today,
            "maxtemp": maxtemp,
            "mintemp": mintemp
        }
    except Exception as e:
        print(f"获取天气失败: {e}")
        return None

def push_to_dingtalk(message):
    """推送到钉钉群"""
    try:
        cmd = [
            "openclaw", "message", "send",
            "--channel", "dingtalk",
            "--target", DINGTALK_CHANNEL_ID,
            "--message", message
        ]
        result = subprocess.run(cmd, timeout=30, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception as e:
        print(f"推送失败: {e}")
        return False

def main():
    print(f"🌤️ 获取天气 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    weather = get_weather()
    if not weather:
        print("❌ 天气获取失败")
        return
    
    # 格式化消息 - 精美的卡片样式
    message = f"""## 🌤️ {weather['location']} 天气预报

*更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*

---

### 🌡️ 温度详情

| 最低 | 当前 | 最高 |
|:----:|:----:|:----:|
| {weather['mintemp']}°C | {weather['temp']}°C | {weather['maxtemp']}°C |

### 📊 其他信息

| 项目 | 数值 |
|------|------|
| 😰 体感 | {weather['feels_like']}°C |
| 💧 湿度 | {weather['humidity']}% |
| 💨 风速 | {weather['wind']} km/h |
| ☀️ 天气 | {weather['weather']} |

---

### ⏰ 逐小时预报

"""
    
    # 添加今日预报
    today = weather.get("today", {})
    if today:
        for hour in today.get("hourly", [])[:8]:  # 当天24小时
            time = hour.get("time", "")
            temp = hour.get("tempC", "")
            weather_code = hour.get("weatherCode", "")
            # 简化显示
            hour_time = int(time.split()[0]) if time else 0
            if 6 <= hour_time <= 22:
                message += f"{hour_time}:00 | {temp}°C | {weather_code}\n"
    
    message += f"\n*数据来源：wttr.in*"
    
    # 推送
    success = push_to_dingtalk(message)
    if success:
        print("✅ 推送成功")
    else:
        print("❌ 推送失败")

if __name__ == "__main__":
    main()