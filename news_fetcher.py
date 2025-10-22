#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日新闻推送到微信
支持热点新闻和科技新闻
"""

import os
import json
import re
import requests
from datetime import datetime
import feedparser


class NewsFetcher:
    def __init__(self):
        self.hot_news = []
        self.toutiao_hot = []
        self.douyin_hot = []
        self.tech_news = []
        self.ai_news = []
        self.weather = None

    def get_clothing_suggestion(self, temp):
        """根据温度给出穿衣建议"""
        try:
            temp = int(temp)
            if temp >= 28:
                return "👕 短袖短裤，注意防晒"
            elif temp >= 23:
                return "👔 短袖长裤，舒适凉爽"
            elif temp >= 18:
                return "👕 长袖薄外套，早晚加件衣服"
            elif temp >= 13:
                return "🧥 薄外套或卫衣，适当保暖"
            elif temp >= 8:
                return "🧥 厚外套，建议穿毛衣"
            elif temp >= 3:
                return "🧥 冬装外套，保暖很重要"
            else:
                return "🧥 羽绒服或棉衣，注意保暖防寒"
        except:
            return "👔 根据天气适当增减衣物"

    def fetch_hot_news(self, limit=10):
        """获取热点新闻 - 使用知乎热榜"""
        print("正在获取热点新闻...")
        try:
            # 知乎热榜 API
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                for item in data.get('data', [])[:limit]:
                    target = item.get('target', {})
                    self.hot_news.append({
                        'title': target.get('title', ''),
                        'url': f"https://www.zhihu.com/question/{target.get('id', '')}",
                        'hot': item.get('detail_text', '')
                    })
                print(f"成功获取 {len(self.hot_news)} 条热点新闻")
            else:
                print(f"获取知乎热榜失败: {response.status_code}")
                # 备用方案：使用百度热搜
                self._fetch_baidu_hot(limit)
        except Exception as e:
            print(f"获取热点新闻出错: {str(e)}")
            self._fetch_baidu_hot(limit)

    def _fetch_baidu_hot(self, limit=10):
        """备用方案：获取百度热搜"""
        try:
            url = "https://top.baidu.com/api/board?platform=wise&tab=realtime"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                for item in data.get('data', {}).get('cards', []):
                    content = item.get('content', [])
                    for news in content[:limit]:
                        self.hot_news.append({
                            'title': news.get('word', ''),
                            'url': news.get('url', ''),
                            'hot': news.get('hotScore', '')
                        })
                print(f"成功获取 {len(self.hot_news)} 条百度热搜")
        except Exception as e:
            print(f"获取百度热搜出错: {str(e)}")

    def fetch_toutiao_hot(self, limit=10):
        """获取今日头条热榜"""
        print("正在获取今日头条热榜...")
        try:
            # 使用今日头条热榜API
            url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                hot_list = data.get('data', [])
                for item in hot_list[:limit]:
                    self.toutiao_hot.append({
                        'title': item.get('Title', ''),
                        'url': item.get('Url', ''),
                        'hot': item.get('HotValue', '')
                    })
                print(f"成功获取 {len(self.toutiao_hot)} 条头条热榜")
            else:
                print(f"今日头条API返回 {response.status_code}")
                self._fetch_toutiao_backup(limit)
        except Exception as e:
            print(f"获取今日头条热榜出错: {str(e)}")
            self._fetch_toutiao_backup(limit)

    def _fetch_toutiao_backup(self, limit=10):
        """备用方案：通过RSSHub获取头条热榜"""
        try:
            url = "https://rsshub.app/toutiao/keyword/热点"
            feed = feedparser.parse(url)
            for entry in feed.entries[:limit]:
                self.toutiao_hot.append({
                    'title': entry.title,
                    'url': entry.link,
                    'hot': ''
                })
            print(f"备用方案成功获取 {len(self.toutiao_hot)} 条头条热榜")
        except Exception as e:
            print(f"头条热榜备用方案失败: {str(e)}")

    def fetch_douyin_hot(self, limit=10):
        """获取抖音热榜"""
        print("正在获取抖音热榜...")
        try:
            # 使用抖音热榜API
            url = "https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                word_list = data.get('word_list', [])
                for item in word_list[:limit]:
                    self.douyin_hot.append({
                        'title': item.get('word', ''),
                        'url': f"https://www.douyin.com/search/{item.get('word', '')}",
                        'hot': item.get('hot_value', '')
                    })
                print(f"成功获取 {len(self.douyin_hot)} 条抖音热榜")
            else:
                print(f"抖音API返回 {response.status_code}")
                self._fetch_douyin_backup(limit)
        except Exception as e:
            print(f"获取抖音热榜出错: {str(e)}")
            self._fetch_douyin_backup(limit)

    def _fetch_douyin_backup(self, limit=10):
        """备用方案：通过RSSHub获取抖音热榜"""
        try:
            url = "https://rsshub.app/douyin/hot"
            feed = feedparser.parse(url)
            for entry in feed.entries[:limit]:
                self.douyin_hot.append({
                    'title': entry.title,
                    'url': entry.link,
                    'hot': ''
                })
            print(f"备用方案成功获取 {len(self.douyin_hot)} 条抖音热榜")
        except Exception as e:
            print(f"抖音热榜备用方案失败: {str(e)}")

    def fetch_tech_news(self, limit=10):
        """获取科技新闻 - 使用 RSS 源"""
        print("正在获取科技新闻...")

        # 科技新闻 RSS 源列表
        rss_feeds = [
            'https://www.36kr.com/feed',  # 36氪
            'https://sspai.com/feed',  # 少数派
            'https://www.ifanr.com/feed',  # 爱范儿
        ]

        try:
            for feed_url in rss_feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    for entry in feed.entries[:limit//len(rss_feeds) + 1]:
                        if len(self.tech_news) >= limit:
                            break
                        self.tech_news.append({
                            'title': entry.title,
                            'url': entry.link,
                            'summary': entry.get('summary', '')[:100] + '...'
                        })
                except Exception as e:
                    print(f"获取 {feed_url} 失败: {str(e)}")
                    continue

            print(f"成功获取 {len(self.tech_news)} 条科技新闻")
        except Exception as e:
            print(f"获取科技新闻出错: {str(e)}")

    def fetch_ai_news(self, limit=8):
        """获取AI新闻 - 使用多个来源"""
        print("正在获取AI新闻...")

        # AI新闻来源
        sources = [
            {
                'name': '机器之心',
                'url': 'https://api.jiqizhixin.com/api/articles',
                'type': 'api'
            }
        ]

        try:
            # 尝试从机器之心API获取
            try:
                url = "https://www.jiqizhixin.com/"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                # 由于API可能有限制，我们使用RSS作为替代
                rss_feeds = [
                    'https://rsshub.app/jiqizhixin/ai',  # 机器之心AI
                    'https://rsshub.app/36kr/search/AI',  # 36氪AI
                ]

                for feed_url in rss_feeds:
                    try:
                        feed = feedparser.parse(feed_url)
                        for entry in feed.entries[:limit//len(rss_feeds) + 1]:
                            if len(self.ai_news) >= limit:
                                break
                            self.ai_news.append({
                                'title': entry.title,
                                'url': entry.link,
                                'summary': entry.get('summary', '')[:100] + '...'
                            })
                    except Exception as e:
                        print(f"获取 {feed_url} 失败: {str(e)}")
                        continue

                # 如果RSS获取失败，使用备用的简单AI关键词搜索
                if len(self.ai_news) == 0:
                    # 备用：从已获取的科技新闻中筛选AI相关
                    ai_keywords = ['AI', '人工智能', '机器学习', 'ChatGPT', 'GPT', '大模型', 'LLM', '深度学习']
                    for news in self.tech_news[:]:
                        if any(keyword in news['title'] for keyword in ai_keywords):
                            if len(self.ai_news) < limit:
                                self.ai_news.append(news)

                print(f"成功获取 {len(self.ai_news)} 条AI新闻")
            except Exception as e:
                print(f"获取AI新闻出错: {str(e)}")
        except Exception as e:
            print(f"AI新闻获取失败: {str(e)}")

    def fetch_weather(self, city="北京"):
        """获取天气预报 - 使用免费API"""
        print(f"正在获取{city}天气...")

        try:
            # 使用免费的天气API
            # 方案1: wttr.in (无需API key)
            url = f"https://wttr.in/{city}?format=j1"
            headers = {
                'User-Agent': 'curl/7.68.0'
            }
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                current = data.get('current_condition', [{}])[0]
                tomorrow = data.get('weather', [{}])[1] if len(data.get('weather', [])) > 1 else {}

                self.weather = {
                    'city': city,
                    'today': {
                        'temp': current.get('temp_C', 'N/A'),
                        'weather': current.get('weatherDesc', [{}])[0].get('value', '未知'),
                        'humidity': current.get('humidity', 'N/A')
                    },
                    'tomorrow': {
                        'temp_max': tomorrow.get('maxtempC', 'N/A'),
                        'temp_min': tomorrow.get('mintempC', 'N/A'),
                        'weather': tomorrow.get('hourly', [{}])[0].get('weatherDesc', [{}])[0].get('value', '未知') if tomorrow.get('hourly') else '未知'
                    }
                }
                print(f"成功获取{city}天气")
            else:
                # 备用方案：使用简单的API
                print(f"天气API返回 {response.status_code}，使用备用方案")
                self._fetch_weather_backup(city)
        except Exception as e:
            print(f"获取天气失败: {str(e)}")
            self._fetch_weather_backup(city)

    def _fetch_weather_backup(self, city):
        """备用天气获取方案"""
        try:
            # 使用v1.yiketianqi.com免费API
            url = f"https://v1.yiketianqi.com/api?unescape=1&version=v91&appid=43656176&appsecret=I42og6Lm&ext=&cityid=&city={city}"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                self.weather = {
                    'city': city,
                    'today': {
                        'temp': data.get('tem', 'N/A'),
                        'weather': data.get('wea', '未知'),
                        'humidity': data.get('humidity', 'N/A')
                    },
                    'tomorrow': {
                        'temp_max': data.get('tem1', 'N/A').replace('°C', ''),
                        'temp_min': data.get('tem2', 'N/A').replace('°C', ''),
                        'weather': data.get('wea', '未知')
                    }
                }
                print(f"备用方案成功获取{city}天气")
        except Exception as e:
            print(f"备用天气方案也失败: {str(e)}")
            # 设置默认值
            self.weather = {
                'city': city,
                'today': {'temp': '--', 'weather': '数据获取失败', 'humidity': '--'},
                'tomorrow': {'temp_max': '--', 'temp_min': '--', 'weather': '数据获取失败'}
            }

    def format_message(self, title="每日新闻"):
        """格式化消息内容 - 简洁白风格"""
        now = datetime.now()
        date_str = now.strftime("%Y年%m月%d日")
        time_str = now.strftime("%H:%M")
        weekday_map = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}
        weekday = weekday_map[now.weekday()]

        # 简洁白风格 HTML 模板
        html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    body {{
        background: #f5f5f7;
        color: #1d1d1f;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", "PingFang SC", sans-serif;
        padding: 0;
        margin: 0;
        line-height: 1.6;
    }}
    .container {{
        max-width: 100%;
        background: #f5f5f7;
    }}
    .header {{
        background: #fff;
        padding: 24px 16px;
        text-align: center;
        border-bottom: 1px solid #e5e5e7;
    }}
    .header h1 {{
        color: #1d1d1f;
        font-size: 22px;
        font-weight: 600;
        margin: 0;
    }}
    .time-bar {{
        background: #fff;
        padding: 12px 16px;
        font-size: 13px;
        color: #86868b;
        text-align: center;
        border-bottom: 1px solid #e5e5e7;
    }}
    .section {{
        margin-top: 12px;
    }}
    .section-header {{
        background: #fff;
        color: #1d1d1f;
        padding: 12px 16px;
        font-size: 17px;
        font-weight: 600;
        border-bottom: 1px solid #e5e5e7;
    }}
    .news-card {{
        background: #fff;
        border-bottom: 1px solid #e5e5e7;
        padding: 16px;
    }}
    .news-card:active {{
        background: #f5f5f7;
    }}
    .rank {{
        display: inline-block;
        background: #f5f5f7;
        color: #1d1d1f;
        font-weight: 600;
        font-size: 12px;
        padding: 4px 10px;
        border-radius: 12px;
        margin-bottom: 8px;
        min-width: 36px;
        text-align: center;
    }}
    .rank.top {{
        background: #ff3b30;
        color: #fff;
    }}
    .news-title {{
        color: #1d1d1f;
        font-size: 15px;
        line-height: 1.5;
        text-decoration: none;
        display: block;
        margin-bottom: 8px;
        font-weight: 400;
    }}
    .hot-tag {{
        display: inline-block;
        background: #ff3b30;
        color: #fff;
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 10px;
        font-weight: 500;
        margin-top: 4px;
    }}
    .tech-card {{
        background: #fff;
        border-left: 3px solid #007aff;
        padding: 16px;
        margin-bottom: 1px;
    }}
    .tech-card:active {{
        background: #f5f5f7;
    }}
    .tech-number {{
        color: #007aff;
        font-weight: 600;
        font-size: 13px;
        margin-bottom: 8px;
    }}
    .tech-title {{
        color: #1d1d1f;
        font-size: 15px;
        font-weight: 500;
        line-height: 1.5;
        margin-bottom: 8px;
    }}
    .tech-title a {{
        color: #1d1d1f;
        text-decoration: none;
    }}
    .tech-summary {{
        color: #86868b;
        font-size: 13px;
        line-height: 1.5;
        margin-bottom: 8px;
    }}
    .read-more {{
        color: #007aff;
        font-size: 13px;
        font-weight: 500;
        text-decoration: none;
    }}
    .weather-card {{
        background: linear-gradient(135deg, #007aff 0%, #5ac8fa 100%);
        padding: 20px 16px;
        color: #fff;
        margin-top: 12px;
    }}
    .weather-title {{
        font-size: 17px;
        font-weight: 600;
        margin-bottom: 16px;
        text-align: center;
    }}
    .weather-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }}
    .weather-item {{
        background: rgba(255, 255, 255, 0.15);
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        backdrop-filter: blur(10px);
    }}
    .weather-day {{
        font-size: 13px;
        opacity: 0.9;
        margin-bottom: 8px;
    }}
    .weather-temp {{
        font-size: 32px;
        font-weight: 600;
        margin: 8px 0;
    }}
    .weather-desc {{
        font-size: 14px;
        opacity: 0.9;
    }}
    .ai-card {{
        background: #fff;
        border-left: 3px solid #ff9500;
        padding: 16px;
        margin-bottom: 1px;
    }}
    .ai-card:active {{
        background: #f5f5f7;
    }}
    .footer {{
        background: #fff;
        border-top: 1px solid #e5e5e7;
        padding: 20px 16px;
        text-align: center;
        color: #86868b;
        font-size: 12px;
        margin-top: 12px;
    }}
    .footer-text {{
        color: #86868b;
        margin: 4px 0;
    }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>{title}</h1>
    </div>
    <div class="time-bar">
        {date_str} {weekday} {time_str}
    </div>
"""

        # 天气预报部分
        if self.weather:
            w = self.weather
            # 获取穿衣建议
            clothing = self.get_clothing_suggestion(w['today']['temp'])
            html += f"""
    <div class="weather-card">
        <div class="weather-title">🌤️ {w['city']} 天气预报</div>
        <div class="weather-grid">
            <div class="weather-item">
                <div class="weather-day">今天</div>
                <div class="weather-temp">{w['today']['temp']}°</div>
                <div class="weather-desc">{w['today']['weather']}</div>
                <div class="weather-desc">湿度 {w['today']['humidity']}%</div>
            </div>
            <div class="weather-item">
                <div class="weather-day">明天</div>
                <div class="weather-temp">{w['tomorrow']['temp_min']}~{w['tomorrow']['temp_max']}°</div>
                <div class="weather-desc">{w['tomorrow']['weather']}</div>
            </div>
        </div>
        <div style="background: rgba(255, 255, 255, 0.2); padding: 12px; border-radius: 12px; margin-top: 12px; text-align: center; font-size: 14px; backdrop-filter: blur(10px);">
            <div style="opacity: 0.9;">穿衣建议</div>
            <div style="font-weight: 600; margin-top: 4px;">{clothing}</div>
        </div>
    </div>
"""

        # 热点新闻部分
        if self.hot_news:
            html += """
    <div class="section">
        <div class="section-header">🔥 热点新闻</div>
"""
            for idx, news in enumerate(self.hot_news[:10], 1):
                # 格式化热度
                hot_tag = ""
                if news['hot']:
                    try:
                        hot_num = int(str(news['hot']).replace('万', '0000'))
                        if hot_num >= 10000:
                            hot_tag = f'<span class="hot-tag">🔥 {hot_num//10000}万热度</span>'
                        else:
                            hot_tag = f'<span class="hot-tag">🔥 {news["hot"]}</span>'
                    except:
                        hot_tag = f'<span class="hot-tag">🔥 {news["hot"]}</span>'

                # 前三名特殊标记
                rank_class = "top" if idx <= 3 else ""

                html += f"""
        <div class="news-card">
            <span class="rank {rank_class}">#{idx}</span>
            <a href="{news['url']}" class="news-title">{news['title']}</a>
            {hot_tag}
        </div>
"""
            html += """
    </div>
"""

        # 今日头条热榜部分
        if self.toutiao_hot:
            html += """
    <div class="section">
        <div class="section-header" style="background: linear-gradient(90deg, #ff6b35, #f7931e);">📱 今日头条</div>
"""
            for idx, news in enumerate(self.toutiao_hot[:10], 1):
                # 格式化热度
                hot_tag = ""
                if news['hot']:
                    try:
                        hot_num = int(str(news['hot']).replace('万', '0000'))
                        if hot_num >= 10000:
                            hot_tag = f'<span class="hot-tag">🔥 {hot_num//10000}万</span>'
                        else:
                            hot_tag = f'<span class="hot-tag">🔥 {news["hot"]}</span>'
                    except:
                        if news['hot']:
                            hot_tag = f'<span class="hot-tag">🔥 {news["hot"]}</span>'

                # 前三名特殊标记
                rank_class = "top" if idx <= 3 else ""

                html += f"""
        <div class="news-card">
            <span class="rank {rank_class}">#{idx}</span>
            <a href="{news['url']}" class="news-title">{news['title']}</a>
            {hot_tag}
        </div>
"""
            html += """
    </div>
"""

        # 抖音热榜部分
        if self.douyin_hot:
            html += """
    <div class="section">
        <div class="section-header" style="background: linear-gradient(90deg, #000, #333);">🎵 抖音热榜</div>
"""
            for idx, news in enumerate(self.douyin_hot[:10], 1):
                # 格式化热度
                hot_tag = ""
                if news['hot']:
                    try:
                        hot_num = int(str(news['hot']))
                        if hot_num >= 10000:
                            hot_tag = f'<span class="hot-tag">🔥 {hot_num//10000}万</span>'
                        else:
                            hot_tag = f'<span class="hot-tag">🔥 {hot_num}</span>'
                    except:
                        if news['hot']:
                            hot_tag = f'<span class="hot-tag">🔥 {news["hot"]}</span>'

                # 前三名特殊标记
                rank_class = "top" if idx <= 3 else ""

                html += f"""
        <div class="news-card">
            <span class="rank {rank_class}">#{idx}</span>
            <a href="{news['url']}" class="news-title">{news['title']}</a>
            {hot_tag}
        </div>
"""
            html += """
    </div>
"""

        # 科技新闻部分
        if self.tech_news:
            html += """
    <div class="section">
        <div class="section-header">💻 科技资讯</div>
"""
            for idx, news in enumerate(self.tech_news[:10], 1):
                # 清理摘要（缩短长度以减少总内容）
                summary = ""
                if news.get('summary'):
                    summary = news['summary'].strip()
                    summary = re.sub(r'<[^>]+>', '', summary)
                    if len(summary) > 50:
                        summary = summary[:50] + "..."

                html += f"""
        <div class="tech-card">
            <div class="tech-number">[{idx:02d}]</div>
            <div class="tech-title">
                <a href="{news['url']}">{news['title']}</a>
            </div>
"""
                # 只在前5条显示摘要
                if summary and idx <= 5:
                    html += f"""
            <div class="tech-summary">{summary}</div>
"""
                html += f"""
            <a href="{news['url']}" class="read-more">阅读全文 →</a>
        </div>
"""
            html += """
    </div>
"""

        # AI新闻部分
        if self.ai_news:
            html += """
    <div class="section">
        <div class="section-header">🤖 AI 前沿</div>
"""
            for idx, news in enumerate(self.ai_news[:8], 1):
                # 清理摘要（缩短长度）
                summary = ""
                if news.get('summary'):
                    summary = news['summary'].strip()
                    summary = re.sub(r'<[^>]+>', '', summary)
                    if len(summary) > 50:
                        summary = summary[:50] + "..."

                html += f"""
        <div class="ai-card">
            <div class="tech-number">[{idx:02d}]</div>
            <div class="tech-title">
                <a href="{news['url']}">{news['title']}</a>
            </div>
"""
                # 只在前3条显示摘要
                if summary and idx <= 3:
                    html += f"""
            <div class="tech-summary">{summary}</div>
"""
                html += f"""
            <a href="{news['url']}" class="read-more">阅读全文 →</a>
        </div>
"""
            html += """
    </div>
"""

        # 底部
        html += """
    <div class="footer">
        <div class="footer-text">每日 08:00 / 20:00 自动推送</div>
    </div>
</div>
</body>
</html>
"""
        return html


class MessagePusher:
    """消息推送器"""

    def __init__(self, push_type, push_key):
        self.push_type = push_type
        self.push_key = push_key

    def push_server_chan(self, title, content):
        """Server酱推送"""
        url = f"https://sctapi.ftqq.com/{self.push_key}.send"
        data = {
            "title": title,
            "desp": content
        }
        response = requests.post(url, data=data)
        return response.json()

    def push_pushplus(self, title, content):
        """PushPlus推送"""
        url = "http://www.pushplus.plus/send"
        data = {
            "token": self.push_key,
            "title": title,
            "content": content,
            "template": "html"
        }
        response = requests.post(url, json=data)
        return response.json()

    def push(self, title, content):
        """统一推送接口"""
        try:
            if self.push_type.lower() == "serverchan":
                result = self.push_server_chan(title, content)
                print(f"Server酱推送结果: {result}")
            elif self.push_type.lower() == "pushplus":
                result = self.push_pushplus(title, content)
                print(f"PushPlus推送结果: {result}")
            else:
                print(f"不支持的推送类型: {self.push_type}")
                return False
            return True
        except Exception as e:
            print(f"推送失败: {str(e)}")
            return False


def main():
    """主函数"""
    # 从环境变量获取配置
    push_type = os.getenv('PUSH_TYPE', 'pushplus')  # serverchan 或 pushplus
    push_key = os.getenv('PUSH_KEY', '')
    city = os.getenv('CITY', '北京')  # 天气城市，默认北京

    if not push_key:
        print("错误: 未设置 PUSH_KEY 环境变量")
        return

    # 获取新闻和天气（优化数量以避免内容过长）
    fetcher = NewsFetcher()
    fetcher.fetch_weather(city=city)
    fetcher.fetch_hot_news(limit=6)
    fetcher.fetch_toutiao_hot(limit=6)
    fetcher.fetch_douyin_hot(limit=6)
    fetcher.fetch_tech_news(limit=5)
    fetcher.fetch_ai_news(limit=3)  # 在tech_news之后，可以从中筛选AI内容

    # 格式化消息
    current_hour = datetime.now().hour
    if current_hour < 12:
        title = "早间新闻"
    else:
        title = "晚间新闻"

    message = fetcher.format_message(title)

    # 推送消息
    pusher = MessagePusher(push_type, push_key)
    success = pusher.push(title, message)

    if success:
        print("✅ 新闻推送成功!")
    else:
        print("❌ 新闻推送失败!")


if __name__ == "__main__":
    main()
