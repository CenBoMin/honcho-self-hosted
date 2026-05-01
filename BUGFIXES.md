# Bug Fixes for honcho-self-hosted

## Fixed Issues

### 1. NVIDIA Embedding Model input_type Parameter Error

**Problem**: 使用 NVIDIA 嵌入模型 (如 `nvidia/nv-embedqa-e5-v5`) 时出现错误：

```
openai.BadRequestError: Error code: 400 - {'error': "'input_type' parameter is required for asymmetric models"}
```

**Root Cause**: NVIDIA 的嵌入模型需要 `input_type` 参数来指定输入类型：

- `"query"` - 用于搜索查询
- `"passage"` - 用于文档/段落

**Solution**: 已修改 `/app/src/embedding_client.py`，在所有 OpenAI embeddings API 调用中添加 `extra_body={"input_type": "..."}` 参数。

**Files Modified**:

- `Dockerfile` - 添加了修复脚本的执行
- `patches/fix_embedding_input_type.py` - 修复脚本

### 2. Missing cloudevents Module

**Problem**: 日志中出现警告：

```
Failed to emit telemetry event DialecticCompletedEvent: No module named 'cloudevents.conversion'
```

**Solution**: 在 Dockerfile 中添加了 `pip install cloudevents` 依赖。

## 配置说明

### 推荐的嵌入模型配置

对于 NVIDIA 嵌入模型，确保在 `.env` 文件中使用以下配置：

```
EMBEDDING_MODEL_CONFIG__TRANSPORT=openai
EMBEDDING_MODEL_CONFIG__MODEL=nvidia/nv-embedqa-e5-v5
EMBEDDING_MODEL_CONFIG__OVERRIDES__BASE_URL=https://integrate.api.nvidia.com/v1
EMBEDDING_MODEL_CONFIG__OVERRIDES__API_KEY_ENV=LLM_EMBEDDING_API_KEY
LLM_EMBEDDING_API_KEY=你的NVIDIA_API_Key
```

### 其他推荐的嵌入模型

如果不想使用 NVIDIA 模型，可以考虑以下替代方案：

#### 1. OpenAI 原生模型

```
EMBEDDING_MODEL_CONFIG__TRANSPORT=openai
EMBEDDING_MODEL_CONFIG__MODEL=text-embedding-3-small
EMBEDDING_MODEL_CONFIG__OVERRIDES__BASE_URL=  # 留空使用默认 OpenAI API
```

#### 2. LongCat 提供的模型

```
EMBEDDING_MODEL_CONFIG__TRANSPORT=openai
EMBEDDING_MODEL_CONFIG__MODEL=text-embedding-004  # 或其他 LongCat 嵌入模型
EMBEDDING_MODEL_CONFIG__OVERRIDES__BASE_URL=https://api.longcat.chat/openai/v1
```

## 重新构建

要应用这些修复，需要重新构建 Docker 镜像：

```bash
docker-compose build
docker-compose up -d
```

或（如果使用 docker build）：

```bash
docker build -t honcho-self-hosted .
docker run -p 8000:8000 --env-file .env honcho-self-hosted
```
