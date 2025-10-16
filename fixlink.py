import os
import re

# =================================================================
# 配置项：请确保项目名正确
# =================================================================
# 您的 GitHub 项目名称
PROJECT_NAME = "BeyondcanonCN"
# 要插入的 <base> 标签内容
BASE_TAG = f'<base href="/{PROJECT_NAME}/">'

# 用于匹配 <head> 和 </head> 的正则表达式（不区分大小写）
HEAD_PATTERN = re.compile(r'<head.*?>', re.IGNORECASE)
BASE_TAG_PATTERN = re.compile(r'<base\s+href=.*?>', re.IGNORECASE)

def insert_base_tag(filepath):
    """
    读取文件内容，在 <head> 标签内插入 <base> 标签。
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  [错误] 无法读取文件 {filepath}: {e}")
        return

    # 1. 检查是否已经存在 <base> 标签
    if BASE_TAG_PATTERN.search(content):
        print(f"  [跳过] 文件已包含 <base> 标签: {filepath}")
        return

    # 2. 查找 <head...> 标签的起始位置
    match = HEAD_PATTERN.search(content)

    if match:
        # 在 <head...> 之后插入 <base> 标签
        insert_index = match.end()
        
        # 插入内容：换行 + base_tag + 换行
        # 我们插入 \nBASE_TAG\n，确保格式正确且易读
        new_content = content[:insert_index] + '\n  ' + BASE_TAG + '\n' + content[insert_index:]
        
        # 3. 写回文件
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  [成功] 插入 <base> 标签: {filepath}")
        except Exception as e:
            print(f"  [错误] 无法写入文件 {filepath}: {e}")
    else:
        print(f"  [警告] 找不到 <head> 标签，已跳过: {filepath}")

def process_directory(root_dir='.'):
    """
    递归遍历目录，处理所有 .html 文件
    """
    print(f"开始处理目录: {os.path.abspath(root_dir)}")
    print(f"将要插入的 Base Path: {BASE_TAG}")
    print("-" * 30)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 忽略 .git 目录以提高效率和安全性
        if '.git' in dirnames:
            dirnames.remove('.git')
        
        for filename in filenames:
            if filename.lower().endswith('.html'):
                filepath = os.path.join(dirpath, filename)
                insert_base_tag(filepath)

    print("-" * 30)
    print("所有 HTML 文件处理完毕。")

if __name__ == "__main__":
    # 确保 Python 环境中安装了 requests 库（虽然本脚本不需要，但良好实践）
    # 运行前，请确保您安装了 Python。
    # 如果不确定是否有 Python，可以先尝试在命令行输入 python --version
    
    # 脚本从当前目录开始执行
    process_directory()