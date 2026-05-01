#!/usr/bin/env python3
"""
可靠修复 embedding_client.py 以支持 NVIDIA 模型的 input_type 参数
"""


def fix_embedding_client():
    file_path = "/app/src/embedding_client.py"

    with open(file_path, "r") as f:
        lines = f.readlines()

    # 找到所有需要修复的位置
    fixes_found = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # 查找 OpenAI embeddings.create 调用
        if "response = await self.client.embeddings.create(" in line:
            # 检查是否在 "else:  # openai" 块中
            # 向前查找最近的 "else:  # openai"
            j = i - 1
            while j >= 0 and "else:  # openai" not in lines[j]:
                j -= 1

            if j >= 0 and "else:  # openai" in lines[j]:
                # 这是需要修复的地方
                # 确定是查询还是批量
                is_query = "input=[query]" in line or any(
                    "input=[query]" in lines[k]
                    for k in range(i, min(i + 5, len(lines)))
                )
                is_batch = (
                    "input=batch" in line
                    or "input=[item.text for item in batch]" in line
                    or any(
                        "input=batch" in lines[k]
                        or "input=[item.text for item in batch]" in lines[k]
                        for k in range(i, min(i + 5, len(lines)))
                    )
                )

                # 找到这一行的结束位置（右括号）
                paren_count = 1
                k = i + 1
                while k < len(lines) and paren_count > 0:
                    paren_count += lines[k].count("(") - lines[k].count(")")
                    if paren_count == 0:
                        break
                    k += 1

                fixes_found.append((i, k, is_query, is_batch))
                i = k + 1
                continue

        i += 1

    # 应用修复（从后往前，避免行号变化）
    fixes_applied = 0
    for start_line, end_line, is_query, is_batch in reversed(fixes_found):
        input_type = "query" if is_query else "passage"

        # 获取原始代码的第一行（包含 embeddings.create）
        first_line = lines[start_line]

        # 检查是否已经有 extra_body
        if "extra_body" in first_line:
            continue

        # 找到右括号前的最后一个逗号位置或插入位置
        # 我们需要在右括号前添加 extra_body 参数

        # 构建新的代码块
        new_lines = []
        for idx in range(start_line, end_line + 1):
            current_line = lines[idx]

            # 如果这行包含 model= 或 input=，添加 extra_body
            if "model=self.model" in current_line and "input=" in current_line:
                # 在这一行的参数后添加 extra_body
                # 找到这行的结尾（可能是 ) 或 ,)
                if current_line.rstrip().endswith(")"):
                    # 替换右括号
                    current_line = (
                        current_line.rstrip()[:-1]
                        + f',\n                        extra_body={{"input_type": "{input_type}"}}\n                    )\n'
                    )
                else:
                    # 在其他地方添加
                    current_line = (
                        current_line.rstrip()
                        + f',\n                        extra_body={{"input_type": "{input_type}"}}\n'
                    )

            new_lines.append(current_line)

        # 替换原始行
        lines[start_line : end_line + 1] = new_lines
        fixes_applied += 1

    with open(file_path, "w") as f:
        f.writelines(lines)

    if fixes_applied >= 3:
        print(f"✅ Applied {fixes_applied} fixes successfully!")
    else:
        print(f"⚠️ Applied {fixes_applied} fixes (expected at least 3)")
        # 不要退出，因为可能有其他修复方式


if __name__ == "__main__":
    fix_embedding_client()
