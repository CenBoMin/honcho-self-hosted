# 快速修复指南

## 问题总结

您的应用遇到了两个主要问题：

1. **NVIDIA 嵌入模型错误**：`input_type` 参数缺失
2. **Telemetry 警告**：缺少 `cloudevents` 模块

## 已修复内容

✅ **修复1**: 添加 NVIDIA embedding 的 `input_type` 参数支持

- 在 `embed()` 方法中：`input_type="query"` (用于搜索查询)
- 在 `batch_embed()` 方法中：`input_type="passage"` (用于文档嵌入)

✅ **修复2**: 添加 `cloudevents` 模块依赖，消除 telemetry 警告

## 如何应用修复

### 方式1：使用 docker-compose (推荐)

```bash
cd honcho-self-hosted
# 确保 .env 文件已正确配置
cp env.example .env  # 如果需要，复制示例配置文件
# 编辑 .env 文件设置您的 API 密钥
nano .env

# 重新构建和启动
docker-compose build --no-cache
docker-compose up -d
```

### 方式2：使用 Docker build

```bash
cd honcho-self-hosted
docker build -t honcho-self-hosted .
docker run -p 8000:8000 --env-file .env honcho-self-hosted
```

## 配置建议

### NVIDIA Embedding 模型 (当前配置)

```
EMBEDDING_MODEL_CONFIG__TRANSPORT=openai
EMBEDDING_MODEL_CONFIG__MODEL=nvidia/nv-embedqa-e5-v5
EMBEDDING_MODEL_CONFIG__OVERRIDES__BASE_URL=https://integrate.api.nvidia.com/v1
LLM_EMBEDDING_API_KEY=你的NVIDIA_API_Key
```

### 替代方案：使用 LongCat 嵌入模型

```
EMBEDDING_MODEL_CONFIG__TRANSPORT=openai
EMBEDDING_MODEL_CONFIG__MODEL=text-embedding-004
EMBEDDING_MODEL_CONFIG__OVERRIDES__BASE_URL=https://api.longcat.chat/openai/v1
LLM_EMBEDDING_API_KEY=你的LongCat_API_Key
```

## 验证修复

1. 检查 Docker 构建日志是否有错误
2. 检查应用启动后日志中是否还有 `input_type` 错误
3. 确认 telemetry 警告消失

## 文件变更说明

- `Dockerfile` - 添加了修复脚本和 cloudevents 依赖
- `patches/fix_embedding_input_type.py` - 修复脚本，添加 input_type 参数
- `BUGFIXES.md` - 详细修复文档
- `QUICK_FIX.md` - 本文件，快速指南

## 故障排除

### 如果仍然看到 input_type 错误

- 确保重新构建了 Docker 镜像（使用 `--no-cache` 参数）
- 检查 NVIDIA API 密钥是否正确配置

### 如果 cloudevents 错误仍然存在

- 确认 Dockerfile 中的 `pip install cloudevents` 行已添加
- 重新构建镜像

## 需要帮助？

如果您遇到任何问题，请提供：

1. Docker 构建日志
2. 应用启动日志
3. 您的 .env 配置（隐藏敏感信息）
