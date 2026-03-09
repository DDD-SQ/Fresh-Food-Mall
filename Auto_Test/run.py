import os
import sys
import subprocess
import shutil
import time
from datetime import datetime


class TestRunner:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.allure_results_dir = os.path.join(self.project_root, "reports", "allure-results")
        self.allure_report_dir = os.path.join(self.project_root, "reports", "allure-report")
        # 设置Allure报告语言为中文
        os.environ['ALLURE_LOCALE'] = 'zh_CN'

    def create_directories(self):
        """创建必要的目录"""
        directories = [
            os.path.join(self.project_root, "reports"),
            self.allure_results_dir,
            self.allure_report_dir,
            os.path.join(self.project_root, "log")
        ]

        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"创建目录: {directory}")

    def clean_allure_results(self):
        """清理之前的Allure测试结果"""
        if os.path.exists(self.allure_results_dir):
            shutil.rmtree(self.allure_results_dir)
            print(f"清理Allure结果目录: {self.allure_results_dir}")
        os.makedirs(self.allure_results_dir)

    def run_pytest(self, test_module=None):
        """运行pytest测试"""
        # 构建pytest命令
        cmd = [sys.executable, "-m", "pytest"]

        # 添加测试模块参数
        if test_module:
            cmd.append(os.path.join("scripts", test_module))
        else:
            cmd.append("scripts")

        # 添加Allure报告参数
        cmd.extend(["--alluredir", self.allure_results_dir])

        # 添加详细输出
        cmd.append("-v")

        print(f"执行命令: {' '.join(cmd)}")

        # 执行测试
        result = subprocess.run(cmd, cwd=self.project_root)
        return result.returncode

    def generate_allure_report(self):
        """生成Allure报告"""
        # 检查Allure命令行工具是否可用
        try:
            subprocess.run(["allure", "--version"], check=True, capture_output=True, shell=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("警告: 未找到Allure命令行工具，请确保已安装并配置了Allure")
            print("下载地址: https://docs.qameta.io/allure/#_installing_a_commandline")
            return False

        # 生成Allure报告
        cmd = ["allure", "generate", self.allure_results_dir, "-o", self.allure_report_dir, "--clean", "--single-file"]
        print(f"执行命令: {' '.join(cmd)}")

        result = subprocess.run(cmd, shell=True)
        if result.returncode == 0:
            print(f"Allure报告已生成: {self.allure_report_dir}")
            return True
        else:
            print("生成Allure报告失败")
            return False

    def open_allure_report(self):
        """打开Allure报告"""
        if not os.path.exists(self.allure_report_dir):
            print("Allure报告目录不存在")
            return

        os.startfile(os.path.join(self.allure_report_dir, "index.html"))

    def run_all_tests(self):
        """运行所有测试并生成报告"""
        print("=" * 50)
        print("开始运行自动化测试")
        print("=" * 50)

        # 创建必要的目录
        self.create_directories()

        # 清理之前的测试结果
        self.clean_allure_results()

        # 运行测试
        start_time = time.time()
        exit_code = self.run_pytest()
        end_time = time.time()

        print(f"\n测试执行完成，耗时: {end_time - start_time:.2f}秒")

        # 生成Allure报告
        if self.generate_allure_report():
            self.open_allure_report()

        return exit_code

    def run_specific_test(self, test_module):
        """运行特定测试模块"""
        print(f"运行测试模块: {test_module}")

        # 创建必要的目录
        self.create_directories()

        # 清理之前的测试结果
        self.clean_allure_results()

        # 运行测试
        start_time = time.time()
        exit_code = self.run_pytest(test_module)
        end_time = time.time()

        print(f"\n测试执行完成，耗时: {end_time - start_time:.2f}秒")

        # 生成Allure报告
        self.generate_allure_report()

        return exit_code


if __name__ == "__main__":
    runner = TestRunner()

    if len(sys.argv) > 1:
        # 运行指定的测试模块
        test_module = sys.argv[1]
        runner.run_specific_test(test_module)
    else:
        # 运行所有测试
        runner.run_all_tests()
