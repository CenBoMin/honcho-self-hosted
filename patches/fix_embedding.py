#!/usr/bin/env python3
"""
可靠修复 embedding_client.py 以支持 NVIDIA 模型的 input_type 参数
"""

import re

def fix_embedding_client():
    file_path = '/app/src/embedding_client.py'

    with open(file_path, 'r') as f:
        content = f.read()

    fixes_applied = 0

    # 修复1: embed() 方法 - 用于查询 (input_type="query")
    # 匹配模式：else:  # openai 后跟 embeddings.create 调用
    old_pattern1 = r'(else:  # openai\n                response = await self\.client\.embeddings\.create\(\n                model=self\.model, input=\[query\]\n            \))'

    new_code1 = '''else:  # openai
                response = await self.client.embeddings.create(
                model=self.model, input=[query],
                extra_body={"input_type": "query"}
            )'''

    content, count1 = re.subn(old_pattern1, new_code1, content)
    fixes_applied += count1

    # 修复2: simple_batch_embed() 方法 - 用于文档 (input_type="passage")
    old_pattern2 = r'(else:  # openai\n                    response = await self\.client\.embeddings\.create\(\n                        input=batch,\n                        model=self\.model,\n                    \))'

    new_code2 = '''else:  # openai
                    response = await self.client.embeddings.create(
                        input=batch,
                        model=self.model,
                        extra_body={"input_type": "passage"}
                    )'''

    content, count2 = re.subn(old_pattern2, new_code2, content)
    fixes_applied += count2

    # 修复3: _process_batch() 方法 - 用于批量处理 (input_type="passage")
    old_pattern3 = r'(else:  # openai\n                    response = await self\.client\.embeddings\.create\(\n                        model=self\.model, input=\[item\.text for item in batch\]\n                    \))'

    new_code3 = '''else:  # openai
                    response = await self.client.embeddings.create(
                        model=self.model, input=[item.text for item in batch],
                        extra_body={"input_type": "passage"}
                    )'''

    content, count3 = re.subn(old_pattern3, new_code3, content)
    fixes_applied += count3

    with open(file_path, 'w') as f:
        f.write(content)

    if fixes_applied == 3:
        print(f"✅ All {fixes_applied} fixes applied successfully!")
    else:
        print(f"⚠️ Only {fixes_applied} fixes applied (expected 3)")
        exit(1)

if __name__ == '__main__':
    fix_embedding_client()
