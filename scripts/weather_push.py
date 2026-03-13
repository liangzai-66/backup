#!/usr/bin/env python3
"""
天气推送脚本 - 每天早上7:50推送到钉钉
使用 Open-Meteo API (无需API密钥)
"""

import os
import subprocess
import json
from datetime import datetime

# 配置 - 余杭区五常街道的经纬度
LOCATION = "杭州市余杭区五常街道"
LATITUDE = 30.25
LONGITUDE = 120.0
DINGTALK_CHANNEL_ID = "cid5P1UzrvK7Xx2yiCGZVit+Q=="

# 风力等级转换 (km/h -> 级别)
def wind_to_level(kmh):
    """将风速(km/h)转换为风力等级"""
    if kmh is None or kmh == "N/A":
        return "N/A"
    try:
        kmh = float(kmh)
        if kmh < 1:
            return "0级"
        elif kmh <= 5:
            return "1级"
        elif kmh <= 11:
            return "2级"
        elif kmh <= 19:
            return "3级"
        elif kmh <= 28:
            return "4级"
        elif kmh <= 38:
            return "5级"
        elif kmh <= 49:
            return "6级"
        elif kmh <= 61:
            return "7级"
        elif kmh <= 74:
            return "8级"
        elif kmh <= 88:
            return "9级"
        elif kmh <= 102:
            return "10级"
        elif kmh <= 117:
            return "11级"
        else:
            return "12级"
    except:
        return "N/A"

# WMO 天气代码映射
WEATHER_CODES = {
    0: "晴天",
    1: "晴间多云",
    2: "多云",
    3: "阴天",
    45: "雾",
    48: "雾凇",
    51: "小毛毛雨",
    53: "中毛毛雨",
    55: "大毛毛雨",
    56: "冻毛毛雨",
    57: "强冻毛毛雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    66: "小冻雨",
    67: "大冻雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    77: "雪粒",
    80: "小阵雨",
    81: "中阵雨",
    82: "大阵雨",
    85: "小阵雪",
    86: "大阵雪",
    95: "雷暴",
    96: "雷暴+小冰雹",
    99: "雷暴+大冰雹",
}

def get_weather():
    """通过 Open-Meteo 获取天气"""
    import urllib.request
    import urllib.parse
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=Asia/Shanghai&lang=zh"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        current = data.get("current", {})
        daily = data.get("daily", {})
        
        # 当前天气
        temp = current.get("temperature_2m", "N/A")
        feels_like = current.get("apparent_temperature", "N/A")
        humidity = current.get("relative_humidity_2m", "N/A")
        wind = current.get("wind_speed_10m", "N/A")
        weather_code = current.get("weather_code", 0)
        
        # 今天的预报
        maxtemp = daily.get("temperature_2m_max", ["N/A"])[0]
        mintemp = daily.get("temperature_2m_min", ["N/A"])[0]
        
        weather = WEATHER_CODES.get(weather_code, "未知")
        
        return {
            "location": LOCATION,
            "temp": temp,
            "feels_like": feels_like,
            "humidity": humidity,
            "wind": wind,
            "weather": weather,
            "weather_code": weather_code,
            "maxtemp": maxtemp,
            "mintemp": mintemp,
            "daily": daily
        }
    except Exception as e:
        print(f"获取天气失败: {e}")
        return None

def push_to_dingtalk(message, max_retries=3):
    """推送到钉钉群，带重试机制"""
    import time
    
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
                stderr = result.stderr.decode() if result.stderr else "未知错误"
                print(f"❌ 第 {attempt} 次失败: {stderr}")
        except Exception as e:
            print(f"❌ 第 {attempt} 次异常: {e}")
        
        if attempt < max_retries:
            wait_time = attempt * 5  # 递增等待时间: 5s, 10s, 15s
            print(f"⏳ 等待 {wait_time}s 后重试...")
            time.sleep(wait_time)
    
    print(f"🚫 已重试 {max_retries} 次，全部失败")
    return False

def main():
    print(f"🌤️ 获取天气 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    weather = get_weather()
    if not weather:
        print("❌ 天气获取失败")
        return
    
    # 格式化消息
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
| 💨 风力 | {wind_to_level(weather['wind'])} |
| ☀️ 天气 | {weather['weather']} |

---

### 📅 逐日预报

"""
    
    # 添加未来几天预报 - 表格格式
    daily = weather.get("daily", {})
    times = daily.get("time", [])
    max_temps = daily.get("temperature_2m_max", [])
    min_temps = daily.get("temperature_2m_min", [])
    weather_codes = daily.get("weather_code", [])
    
    weekday_map = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    # 构建表格
    message += "| 日期 | 天气 | 温度 |\n"
    message += "|:----:|:----:|:----:|\n"
    
    for i, (day, maxt, mint, code) in enumerate(zip(times, max_temps, min_temps, weather_codes)):
        if i == 0:
            day_label = "今天"
        elif i == 1:
            day_label = "明天"
        else:
            dt = datetime.strptime(day, "%Y-%m-%d")
            day_label = weekday_map[dt.weekday()]
        
        weather_desc = WEATHER_CODES.get(code, "未知")
        message += f"| {day_label} | {weather_desc} | {mint}~{maxt}°C |\n"
    
    message += f"\n*数据来源：Open-Meteo*"
    
    # 推送（重试3次）
    success = push_to_dingtalk(message, max_retries=3)
    if success:
        print("✅ 推送成功")
    else:
        print("❌ 推送失败")

if __name__ == "__main__":
    main()