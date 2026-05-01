#!/usr/bin/env python3
"""
修复 embedding_client.py 以支持 NVIDIA 模型的 input_type 参数
NVIDIA nv-embedqa-e5-v5 等模型需要 input_type 参数 ("query" 或 "passage")
"""

import re
import sys


def fix_embedding_client(file_path: str = "/app/src/embedding_client.py"):
    """修复 embedding_client.py 文件以支持 NVIDIA embedding 的 input_type 参数"""

    with open(file_path, "r") as f:
        content = f.read()

    # 修复1: embed 方法中的单个查询 - 用于搜索查询
    # 匹配：response = await self.client.embeddings.create(
    #                 model=self.model, input=[query]
    #             )
    old_pattern1 = r"""(
            else:  # openai
                response = await self\.client\.embeddings\.create\(\n                model=self\.model, input=\[query\]\n            \))"""

    new_code1 = """else:  # openai
                response = await self.client.embeddings.create(
                model=self.model, input=[query],
                extra_body={"input_type": "query"}
            )"""

    content = re.sub(old_pattern1, new_code1, content, flags=re.VERBOSE)

    # 修复2: simple_batch_embed 方法中的批量嵌入 - 用于文档/段落
    old_pattern2 = r"""(else:  # openai
                    response = await self\.client\.embeddings\.create\(\n                        input=batch,
                        model=self\.model,
                    \))"""

    new_code2 = """else:  # openai
                    response = await self.client.embeddings.create(
                        input=batch,
                        model=self.model,
                        extra_body={"input_type": "passage"}
                    )"""

    content = re.sub(old_pattern2, new_code2, content, flags=re.VERBOSE)

    # 修复3: _process_batch 方法中的批量处理
    old_pattern3 = r"""(else:  # openai
                    response = await self\.client\.embeddings\.create\(\n                        model=self\.model, input=\[item\.text for item in batch\]
                    \))"""

    new_code3 = """else:  # openai
                    response = await self.client.embeddings.create(
                        model=self.model, input=[item.text for item in batch],
                        extra_body={"input_type": "passage"}
                    )"""

    content = re.sub(old_pattern3, new_code3, content, flags=re.VERBOSE)

    with open(file_path, "w") as f:
        f.write(content)

    print("✅ Fixed embedding_client.py for NVIDIA input_type support")

    # 验证修复结果
    with open(file_path, "r") as f:
        fixed_content = f.read()

    if 'extra_body={"input_type": "query"}' in fixed_content:
        print("✅ embed() method fixed for query input_type")
    else:
        print("❌ embed() method not properly fixed")

    if 'extra_body={"input_type": "passage"}' in fixed_content:
        print("✅ batch methods fixed for passage input_type")
    else:
        print("❌ batch methods not properly fixed")


if __name__ == "__main__":
    fix_embedding_client()
