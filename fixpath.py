import os
import glob
import sys
import re

# --- 配置 ---
# 您的GitHub Pages仓库名称 (子目录名)
# 请确保与您的仓库名称 'BeyondcanonCN' 一致。
REPO_NAME = "BeyondcanonCN"
# --- 结束配置 ---

def fix_github_pages_paths(repo_name):
    print(f"GitHub Pages 路径修正脚本 v1.0")
    print(f"仓库名 (Base Path): /{repo_name}")
    print("-" * 40)

    # 定义要执行的搜索和替换对 (元组: (搜索字符串, 替换字符串))
    # 策略：将所有指向网站根目录的资源链接 (无论是相对还是绝对) 修正为带 repo_name 的绝对路径
    
    # 注意：这里使用正则表达式来更精确地捕获 src/href 属性中的路径。
    # 匹配模式: (属性名=引号) (可能是相对路径../或绝对路径/) (后跟需要修正的目录名)
    replacements = [
        # 1. 修正 Next.js 静态资源链接 (_next/static/)
        (re.compile(r'([src|href]=["\'])(?:\.\.\/)*?(_next/static/)'), fr'\1/{repo_name}/\2'),
        (re.compile(r'([src|href]=["\'])/(_next/static/)'), fr'\1/{repo_name}/\2'),

        # 2. 修正 cdn-cgi 链接 (用于 Cloudflare 脚本加载)
        (re.compile(r'([src|href]=["\'])(?:\.\.\/)*?(cdn-cgi/)'), fr'\1/{repo_name}/\2'),
        (re.compile(r'([src|href]=["\'])/(cdn-cgi/)'), fr'\1/{repo_name}/\2'),
        
        # 3. 修正 assets 链接
        (re.compile(r'([src|href]=["\'])(?:\.\.\/)*?(assets/)'), fr'\1/{repo_name}/\2'),
        (re.compile(r'([src|href]=["\'])/(assets/)'), fr'\1/{repo_name}/\2'),

        # 4. 修正根目录文件链接
        (re.compile(r'([src|href]=["\'])(?:\.\.\/)*?(favicon\.ico|manifest\.webmanifest)'), fr'\1/{repo_name}/\2'),
        (re.compile(r'([src|href]=["\'])/(favicon\.ico|manifest\.webmanifest)'), fr'\1/{repo_name}/\2'),
    ]

    modified_files = 0
    
    # 递归查找所有 .html 和 .htm 文件
    file_list = glob.glob('**/*.html', recursive=True) + glob.glob('**/*.htm', recursive=True)
    total_files = len(file_list)
    
    print(f"共找到 {total_files} 个 HTML/HTM 文件...")

    for i, file_path in enumerate(file_list):
        # 打印进度
        print(f"[{i+1}/{total_files}] 正在处理: {file_path}", end='\r', flush=True)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            except Exception:
                print(f"\n[错误] 无法读取文件 {file_path} (编码问题)")
                continue
        except Exception as e:
            print(f"\n[错误] 读取文件 {file_path} 时发生错误: {e}")
            continue

        original_content = content
        
        # 执行所有替换
        for search_re, replace_str in replacements:
            content = search_re.sub(replace_str, content)
        
        if content != original_content:
            try:
                # 以 UTF-8 编码写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                modified_files += 1
            except Exception as e:
                print(f"\n[错误] 写入文件 {file_path} 时发生错误: {e}")

    # 清除进度信息，打印总结
    sys.stdout.write('\r' + ' ' * 60 + '\r')
    print("-" * 40)
    print(f"✔ 路径修正完成。")
    print(f"✔ 检查了 {total_files} 个文件，修正了 {modified_files} 个文件中的路径。")
    print(f"请将修改后的文件推送到您的 GitHub 仓库以查看效果。")

if __name__ == "__main__":
    fix_github_pages_paths(REPO_NAME)