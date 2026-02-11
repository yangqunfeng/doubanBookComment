# 部署指南 / Deployment Guide

[中文](#中文) | [English](#english)

---

## 中文

本指南提供多种部署方案，让你的图书推荐系统可以通过互联网访问。

### 🚀 部署方案对比

| 方案 | 难度 | 费用 | 适用场景 |
|------|------|------|----------|
| [Render](#方案一render-推荐) | ⭐ | 免费 | 个人项目、演示 |
| [Railway](#方案二railway) | ⭐ | 免费/$5/月 | 小型项目 |
| [Heroku](#方案三heroku) | ⭐⭐ | $7/月起 | 稳定运行 |
| [阿里云/腾讯云](#方案四阿里云腾讯云) | ⭐⭐⭐ | ¥100/月起 | 生产环境 |
| [Docker + VPS](#方案五docker--vps) | ⭐⭐⭐⭐ | $5/月起 | 完全控制 |

---

## 方案一：Render（推荐）

**优点**：完全免费、自动部署、支持 Python、配置简单

**缺点**：免费版有休眠机制（15分钟无访问会休眠）

### 步骤

#### 1. 准备项目

创建 `render.yaml`：

```yaml
services:
  - type: web
    name: douban-book-recommender
    env: python
    buildCommand: pip install -r requirements.txt && python knowledge_graph_builder.py
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
      - key: PORT
        value: 5000
```

创建 `gunicorn_config.py`：

```python
bind = "0.0.0.0:5000"
workers = 2
threads = 4
timeout = 120
```

更新 `requirements.txt`，添加：

```
gunicorn==21.2.0
```

#### 2. 上传到 GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/doubanBookComment.git
git push -u origin main
```

#### 3. 部署到 Render

1. 访问 [Render](https://render.com/)
2. 注册/登录账号
3. 点击 "New +" → "Web Service"
4. 连接你的 GitHub 仓库
5. 配置：
   - **Name**: `douban-book-recommender`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python knowledge_graph_builder.py`
   - **Start Command**: `gunicorn app:app`
6. 点击 "Create Web Service"

#### 4. 上传数据文件

由于数据文件较大，需要单独上传：

**方法 A：使用 Render Disk**

1. 在 Render 控制台创建 Disk
2. 通过 SSH 上传数据文件
3. 挂载到服务

**方法 B：使用对象存储**

1. 将数据文件上传到 AWS S3 / 阿里云 OSS
2. 修改 `config.py`，从云存储下载数据

```python
import os
import urllib.request

def download_data_if_needed():
    if not os.path.exists('newBookInformation'):
        print("下载数据文件...")
        urllib.request.urlretrieve(
            'https://your-storage-url/newBookInformation',
            'newBookInformation'
        )
```

#### 5. 访问你的应用

部署完成后，Render 会提供一个 URL：
```
https://douban-book-recommender.onrender.com
```

---

## 方案二：Railway

**优点**：$5 免费额度、无休眠、部署快速

**缺点**：免费额度用完需付费

### 步骤

#### 1. 准备项目

创建 `railway.json`：

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

创建 `Procfile`：

```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

#### 2. 部署

1. 访问 [Railway](https://railway.app/)
2. 使用 GitHub 登录
3. 点击 "New Project" → "Deploy from GitHub repo"
4. 选择你的仓库
5. Railway 会自动检测并部署

#### 3. 配置环境变量

在 Railway 控制台设置：
- `PYTHON_VERSION`: `3.9`
- `PORT`: `5000`

#### 4. 访问

Railway 会提供一个域名：
```
https://douban-book-recommender.up.railway.app
```

---

## 方案三：Heroku

**优点**：稳定可靠、生态完善

**缺点**：需要付费（$7/月起）

### 步骤

#### 1. 安装 Heroku CLI

```bash
# Windows
choco install heroku-cli

# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2. 准备项目

创建 `Procfile`：

```
web: gunicorn app:app
```

创建 `runtime.txt`：

```
python-3.9.18
```

#### 3. 部署

```bash
# 登录 Heroku
heroku login

# 创建应用
heroku create douban-book-recommender

# 推送代码
git push heroku main

# 查看日志
heroku logs --tail
```

#### 4. 访问

```
https://douban-book-recommender.herokuapp.com
```

---

## 方案四：阿里云/腾讯云

**优点**：国内访问快、稳定、可备案

**缺点**：需要服务器运维知识

### 步骤

#### 1. 购买服务器

- **阿里云 ECS**: 2核4G，约 ¥100/月
- **腾讯云 CVM**: 2核4G，约 ¥100/月

#### 2. 配置服务器

```bash
# SSH 连接服务器
ssh root@your-server-ip

# 安装 Python
sudo apt update
sudo apt install python3.9 python3-pip

# 安装 Nginx
sudo apt install nginx

# 克隆项目
git clone https://github.com/yourusername/doubanBookComment.git
cd doubanBookComment

# 安装依赖
pip3 install -r requirements.txt

# 上传数据文件（使用 scp 或 FTP）
scp newBookInformation root@your-server-ip:/path/to/project/
scp newCommentdata root@your-server-ip:/path/to/project/

# 构建知识图谱
python3 knowledge_graph_builder.py
```

#### 3. 配置 Nginx

创建 `/etc/nginx/sites-available/douban-recommender`：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/project/static;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/douban-recommender /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 4. 使用 Supervisor 管理进程

安装 Supervisor：

```bash
sudo apt install supervisor
```

创建 `/etc/supervisor/conf.d/douban-recommender.conf`：

```ini
[program:douban-recommender]
directory=/path/to/project
command=gunicorn app:app -w 4 -b 127.0.0.1:5000
user=root
autostart=true
autorestart=true
stderr_logfile=/var/log/douban-recommender.err.log
stdout_logfile=/var/log/douban-recommender.out.log
```

启动服务：

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start douban-recommender
```

#### 5. 配置域名

1. 在域名服务商添加 A 记录，指向服务器 IP
2. 等待 DNS 生效（通常几分钟到几小时）
3. 访问 `http://your-domain.com`

#### 6. 配置 HTTPS（可选但推荐）

使用 Let's Encrypt 免费证书：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 方案五：Docker + VPS

**优点**：环境隔离、易于迁移、完全控制

**缺点**：需要 Docker 知识

### 步骤

#### 1. 创建 Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "app:app", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120"]
```

#### 2. 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./newBookInformation:/app/newBookInformation
      - ./newCommentdata:/app/newCommentdata
      - ./knowledge_graph:/app/knowledge_graph
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

#### 3. 创建 .dockerignore

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.git
.gitignore
*.md
.vscode
.idea
```

#### 4. 构建和运行

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

#### 5. 部署到 VPS

```bash
# 在 VPS 上安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 上传项目
scp -r doubanBookComment root@your-vps-ip:/root/

# SSH 到 VPS
ssh root@your-vps-ip

# 启动服务
cd /root/doubanBookComment
docker-compose up -d
```

---

## 📊 性能优化建议

### 1. 使用 CDN

将静态文件（CSS、JS）托管到 CDN：

- **国内**: 阿里云 CDN、腾讯云 CDN
- **国际**: Cloudflare、AWS CloudFront

### 2. 数据库优化

如果数据量继续增长，考虑：

- 使用 PostgreSQL 替代 pickle 文件
- 使用 Redis 缓存热门推荐结果
- 使用 Neo4j 存储知识图谱

### 3. 负载均衡

使用多个 worker 进程：

```python
# gunicorn_config.py
workers = 4  # CPU 核心数 * 2 + 1
threads = 2
worker_class = 'gthread'
```

### 4. 监控和日志

- 使用 Sentry 监控错误
- 使用 Prometheus + Grafana 监控性能
- 配置日志轮转

---

## 🔒 安全建议

### 1. 环境变量

不要在代码中硬编码敏感信息，使用环境变量：

```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
DATABASE_URL = os.environ.get('DATABASE_URL')
```

### 2. HTTPS

生产环境必须使用 HTTPS：

```bash
# 使用 Let's Encrypt
sudo certbot --nginx -d your-domain.com
```

### 3. 防火墙

只开放必要的端口：

```bash
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 4. 限流

防止 API 滥用：

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)
```

---

## 📱 域名配置

### 免费域名

- [Freenom](https://www.freenom.com/) - 免费 .tk, .ml, .ga 域名
- [eu.org](https://nic.eu.org/) - 免费 .eu.org 二级域名

### 付费域名

- [阿里云](https://wanwang.aliyun.com/) - .com 约 ¥55/年
- [腾讯云](https://dnspod.cloud.tencent.com/) - .com 约 ¥55/年
- [Namecheap](https://www.namecheap.com/) - .com 约 $10/年

---

## 🎯 推荐方案

### 个人学习/演示
→ **Render 免费版** 或 **Railway**

### 小型项目
→ **Railway** ($5/月) 或 **Heroku** ($7/月)

### 生产环境
→ **阿里云/腾讯云** + **Docker** + **Nginx**

### 国际用户
→ **AWS** 或 **DigitalOcean** + **Docker**

---

## 📞 需要帮助？

- 查看 [常见问题](FAQ.md)
- 提交 [Issue](https://github.com/yourusername/doubanBookComment/issues)
- 联系邮箱: your.email@example.com

---

## English

This guide provides multiple deployment options to make your book recommendation system accessible via the internet.

### 🚀 Deployment Options Comparison

| Option | Difficulty | Cost | Use Case |
|--------|-----------|------|----------|
| [Render](#option-1-render-recommended) | ⭐ | Free | Personal projects, demos |
| [Railway](#option-2-railway) | ⭐ | Free/$5/mo | Small projects |
| [Heroku](#option-3-heroku) | ⭐⭐ | $7/mo+ | Stable operation |
| [AWS/GCP](#option-4-awsgcp) | ⭐⭐⭐ | $20/mo+ | Production |
| [Docker + VPS](#option-5-docker--vps) | ⭐⭐⭐⭐ | $5/mo+ | Full control |

---

## Option 1: Render (Recommended)

**Pros**: Completely free, auto-deploy, Python support, simple setup

**Cons**: Free tier has sleep mechanism (sleeps after 15 min of inactivity)

### Steps

#### 1. Prepare Project

Create `render.yaml`:

```yaml
services:
  - type: web
    name: douban-book-recommender
    env: python
    buildCommand: pip install -r requirements.txt && python knowledge_graph_builder.py
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
      - key: PORT
        value: 5000
```

Update `requirements.txt`, add:

```
gunicorn==21.2.0
```

#### 2. Deploy to Render

1. Visit [Render](https://render.com/)
2. Sign up/Login
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure and deploy

#### 3. Access Your App

After deployment, Render provides a URL:
```
https://douban-book-recommender.onrender.com
```

---

## 🎯 Recommended Solution

### For Learning/Demo
→ **Render Free Tier** or **Railway**

### For Small Projects
→ **Railway** ($5/mo) or **Heroku** ($7/mo)

### For Production
→ **AWS/GCP** + **Docker** + **Nginx**

---

**Good luck with your deployment! 🚀**

