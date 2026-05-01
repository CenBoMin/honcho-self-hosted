#!/usr/bin/env python3
"""
验证修复是否成功应用的脚本
"""

import os
import sys


def validate_fixes():
    """验证所有修复是否正确应用"""
    print("🔍 验证修复...")

    # 检查修复脚本是否存在
    fix_script_path = "patches/fix_embedding_input_type.py"
    if os.path.exists(fix_script_path):
        print("✅ 修复脚本存在")
    else:
        print("❌ 修复脚本缺失")
        return False

    # 检查 Dockerfile 是否包含修复步骤
    dockerfile_path = "Dockerfile"
    if os.path.exists(dockerfile_path):
        with open(dockerfile_path, "r") as f:
            dockerfile_content = f.read()

        if (
            "fix_embedding_input_type.py" in dockerfile_content
            and "cloudevents" in dockerfile_content
        ):
            print("✅ Dockerfile 包含所有修复步骤")
        else:
            print("❌ Dockerfile 缺少修复步骤")
            return False

    print("✅ 所有修复已正确配置")
    return True


if __name__ == "__main__":
    success = validate_fixes()
    if success:
        print("\n🎉 修复配置成功！")
        print("\n下一步：")
        print("1. 确保 .env 文件配置正确")
        print("2. 重新构建 Docker 镜像: docker-compose build")
        print("3. 重启服务: docker-compose up -d")
    else:
        print("\n❌ 修复配置有问题，请检查")
        sys.exit(1)
