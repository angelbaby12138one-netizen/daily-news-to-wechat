# 快速启动指南

## 三步开始使用

### 步骤 1：准备推送服务

选择以下任一服务：

**PushPlus（推荐，最简单）**
1. 访问 http://www.pushplus.plus/
2. 微信扫码登录
3. 复制 Token

**Server酱（备选）**
1. 访问 https://sct.ftqq.com/
2. GitHub 登录并绑定微信
3. 复制 SendKey

### 步骤 2：上传到 GitHub

```bash
cd daily-news-to-wechat
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/daily-news-to-wechat.git
git push -u origin main
```

### 步骤 3：配置 GitHub Secrets

在 GitHub 仓库页面：

1. Settings → Secrets and variables → Actions
2. 点击 New repository secret
3. 添加：
   - Name: `PUSH_KEY`
   - Value: 你的 Token/SendKey
4. （可选）添加：
   - Name: `PUSH_TYPE`
   - Value: `pushplus` 或 `serverchan`

### 步骤 4：启用并测试

1. 进入 Actions 标签页
2. 启用 Workflows
3. 点击 "每日新闻推送"
4. 点击 "Run workflow" 测试

完成！现在每天早上 8 点和晚上 8 点会自动推送新闻到你的微信。

## 本地测试

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量（Windows PowerShell）
$env:PUSH_TYPE="pushplus"
$env:PUSH_KEY="你的Token"

# 运行
python news_fetcher.py
```

## 故障排除

- 检查 Actions 运行日志
- 确认 Secrets 配置正确
- 验证推送服务绑定状态
- 查看 README.md 获取详细说明
