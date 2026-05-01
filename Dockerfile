FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 克隆 Honcho 官方源码
RUN git clone --depth 1 https://github.com/plastic-labs/honcho.git /tmp/honcho && \
  cp -r /tmp/honcho/. /app && \
  rm -rf /tmp/honcho

# 安装 Python 依赖
RUN pip install --no-cache-dir -e .

# 安装 cloudevents 依赖（修复 telemetry 错误）
RUN pip install --no-cache-dir cloudevents

# 复制修复脚本
COPY patches/fix_embedding_input_type.py /tmp/fix_embedding_input_type.py

# 运行修复脚本
RUN python3 /tmp/fix_embedding_input_type.py

# 复制自定义配置
COPY config.toml /app/config.toml
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000

CMD ["/app/docker-entrypoint.sh"]
