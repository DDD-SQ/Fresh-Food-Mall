"""
pytest 配置文件

定义测试夹具和钩子函数，供所有测试文件共享使用。
"""

import allure
import pytest
import os
import pymysql
from utils import DriverTools
from base.base_page import BasePage


def get_db_connection():
    """获取数据库连接"""
    return pymysql.connect(
        host=os.environ.get('MYSQL_HOST', 'localhost'),
        port=int(os.environ.get('MYSQL_PORT', '3306')),
        user=os.environ.get('MYSQL_USER', 'django'),
        password=os.environ.get('MYSQL_PASSWORD', 'Chafferer!'),
        database=os.environ.get('MYSQL_DATABASE', 'daily_fresh'),
        charset='utf8mb4'
    )


def clear_cart():
    """清除指定用户的购物车数据"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM daily_fresh.df_cart_cartinfo WHERE user_id = 32;"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"[前置] 已清除用户购物车数据")
    except Exception as e:
        print(f"[前置] 清除购物车数据失败: {e}")


@pytest.fixture(scope="class", autouse=True)
def driver():
    """
    类级别的浏览器驱动fixture
    
    - scope="class": 每个测试类只初始化一次
    - yield: 返回驱动给测试使用
    - 测试结束后自动退出驱动
    """
    driver = DriverTools.get_driver()
    yield driver
    DriverTools.quit_driver()


@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(request):
    """
    测试完成后自动截图的fixture
    
    无论测试成功或失败，都会截图当前页面
    """
    yield
    if hasattr(request.node, 'rep_call'):
        base_page = BasePage()
        if request.node.rep_call.failed:
            base_page.save_screenshot(f"{request.node.name}_失败")
        else:
            base_page.save_screenshot(f"{request.node.name}_成功")


@pytest.fixture(scope="function", autouse=True)
def clear_cart_before_test():
    """
    每个测试用例执行前清除购物车数据
    
    - autouse=True: 自动执行，无需手动调用
    - scope="function": 每个测试用例执行前都会执行
    """
    clear_cart()
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest钩子函数：生成测试报告
    
    将测试结果附加到request.node，供screenshot_on_failure使用
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    """
    会话级别的初始化fixture
    
    - autouse=True: 自动执行，无需手动调用
    - scope="session": 整个测试会话只执行一次
    """
    print("\n========== 测试会话开始 ==========")
    yield
    print("\n========== 测试会话结束 ==========")
