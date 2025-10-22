# 每日新闻推送到微信

每天自动推送热点新闻和科技资讯到微信，使用 GitHub Actions 免费运行，无需服务器。

## 功能特性

- 每天早上 8:00 和晚上 8:00 自动推送
- 支持热点新闻（知乎热榜/百度热搜）
- 支持科技资讯（36氪、少数派、爱范儿等）
- 支持 Server酱 和 PushPlus 推送服务
- 完全免费，基于 GitHub Actions

## 快速开始

### 1. Fork 本仓库

点击右上角的 Fork 按钮，将项目 Fork 到你的 GitHub 账号下。

### 2. 获取推送服务密钥

#### 方法 A：使用 PushPlus（推荐）

1. 访问 [PushPlus 官网](http://www.pushplus.plus/)
2. 使用微信扫码登录
3. 复制你的 Token

#### 方法 B：使用 Server酱

1. 访问 [Server酱官网](https://sct.ftqq.com/)
2. 使用 GitHub 登录
3. 绑定微信
4. 复制 SendKey

### 3. 配置 GitHub Secrets

在你 Fork 的仓库中：

1. 点击 `Settings` → `Secrets and variables` → `Actions`
2. 点击 `New repository secret` 添加以下密钥：

   **必需配置：**
   - `PUSH_KEY`: 你的推送服务密钥（PushPlus Token 或 Server酱 SendKey）

   **可选配置：**
   - `PUSH_TYPE`: 推送服务类型
     - 填写 `pushplus` (默认) 或 `serverchan`

### 4. 启用 GitHub Actions

1. 点击仓库的 `Actions` 标签页
2. 如果看到提示，点击 `I understand my workflows, go ahead and enable them`
3. 点击左侧的 `每日新闻推送` workflow
4. 点击 `Enable workflow`

### 5. 测试运行

点击 `Run workflow` → `Run workflow` 手动触发一次，测试是否配置成功。

## 配置说明

### 推送时间修改

如需修改推送时间，编辑 `.github/workflows/daily-news.yml` 文件中的 cron 表达式：

```yaml
schedule:
  # 早上 8:00 北京时间 (UTC+8, 所以是 UTC 0:00)
  - cron: '0 0 * * *'
  # 晚上 8:00 北京时间 (UTC+8, 所以是 UTC 12:00)
  - cron: '0 12 * * *'
```

时区转换：北京时间 = UTC + 8 小时

示例：
- 北京时间 07:00 → UTC 23:00 前一天 → `0 23 * * *`
- 北京时间 12:00 → UTC 04:00 → `0 4 * * *`
- 北京时间 20:00 → UTC 12:00 → `0 12 * * *`

### 新闻源自定义

编辑 `news_fetcher.py` 中的 RSS 源列表：

```python
rss_feeds = [
    'https://www.36kr.com/feed',  # 36氪
    'https://sspai.com/feed',     # 少数派
    'https://www.ifanr.com/feed', # 爱范儿
    # 添加你想要的 RSS 源
]
```

## 项目结构

```
daily-news-to-wechat/
├── .github/
│   └── workflows/
│       └── daily-news.yml      # GitHub Actions 工作流配置
├── news_fetcher.py              # 新闻获取和推送脚本
├── requirements.txt             # Python 依赖
├── .gitignore
└── README.md                    # 说明文档
```

## 常见问题

### 1. 为什么没有收到推送？

- 检查 GitHub Actions 是否已启用
- 检查 Secrets 是否正确配置
- 查看 Actions 运行日志，确认是否有错误
- 确认推送服务（PushPlus/Server酱）的微信绑定状态

### 2. 如何修改推送内容？

编辑 `news_fetcher.py` 中的 `format_message()` 方法，自定义消息格式。

### 3. 可以只推送一次吗？

修改 `.github/workflows/daily-news.yml`，删除其中一个 cron 表达式即可。

### 4. GitHub Actions 免费额度够用吗？

GitHub 为公开仓库提供无限制的 Actions 分钟数，私有仓库每月 2000 分钟。
本项目每次运行约 1-2 分钟，一天两次，一个月约 60-120 分钟，完全够用。

### 5. 如何添加更多新闻源？

在 `news_fetcher.py` 的 `fetch_tech_news()` 或 `fetch_hot_news()` 方法中添加更多 API 或 RSS 源。

## 技术栈

- Python 3.10
- GitHub Actions
- PushPlus / Server酱
- RSS Parser

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v1.0.0 (2025-01-22)
- 初始版本
- 支持热点新闻和科技资讯
- 每天早晚自动推送
- 支持 PushPlus 和 Server酱
