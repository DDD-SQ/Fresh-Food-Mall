# 使用 Python 3.13 轻量级基础镜像
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 1. 更换 apt 源为阿里云镜像（国内加速）并安装 Git
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# 2. 从 GitHub 拉取最新代码
RUN git clone https://github.com/DDD-SQ/Fresh-Food-Mall.git .

# 3. 使用清华源安装 Python 依赖（根目录下的 requirements.txt）
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 安装 Chrome 浏览器及依赖（用于 Selenium 无头模式）
RUN apt-get update && apt-get install -y \
    wget gnupg unzip fonts-liberation \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 \
    libgtk-3-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# 添加 Google Chrome 官方源并安装稳定版（新写法）
RUN set -eux; \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub \
      | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg; \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
      > /etc/apt/sources.list.d/google-chrome.list; \
    apt-get update; \
    apt-get install -y google-chrome-stable; \
    rm -rf /var/lib/apt/lists/*

# 安装 OpenJDK 17（Allure 依赖，Debian Trixie 不支持 OpenJDK 11）
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# 下载并安装 Allure 命令行工具（版本可调整）
ENV ALLURE_VERSION=2.29.0
RUN wget -q https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz \
    && tar -zxvf allure-${ALLURE_VERSION}.tgz -C /opt \
    && ln -s /opt/allure-${ALLURE_VERSION}/bin/allure /usr/local/bin/allure \
    && rm allure-${ALLURE_VERSION}.tgz

# 5. 暴露 Django 默认端口
EXPOSE 8000

# 6. 启动命令：运行 daily-fresh-master 目录下的 Django 项目
CMD ["python", "daily-fresh-master/manage.py", "runserver", "0.0.0.0:8000"]
