import os
import subprocess
import sys

# 检查PATH环境变量
print("当前PATH环境变量:")
for path in os.environ.get('PATH', '').split(os.pathsep):
    print(f"  {path}")

# 检查allure是否在PATH中
allure_in_path = any('allure' in path.lower() for path in os.environ.get('PATH', '').split(os.pathsep))
print(f"\nAllure路径是否在PATH中: {allure_in_path}")

# 尝试使用where命令查找allure
try:
    result = subprocess.run(["where", "allure"], capture_output=True, text=True, shell=True)
    if result.returncode == 0:
        print(f"\n找到Allure路径: {result.stdout.strip()}")
    else:
        print("\n使用where命令未找到Allure")
except Exception as e:
    print(f"\n执行where命令出错: {e}")

# 尝试直接运行allure --version
try:
    print("\n尝试运行allure --version...")
    result = subprocess.run(["allure", "--version"], capture_output=True, text=True, check=True, shell=True)
    print(f"成功! Allure版本: {result.stdout.strip()}")
except subprocess.CalledProcessError as e:
    print(f"运行allure --version失败: {e}")
    print(f"返回码: {e.returncode}")
    print(f"错误输出: {e.stderr}")
except FileNotFoundError:
    print("错误: 找不到allure命令")
except Exception as e:
    print(f"未知错误: {e}")