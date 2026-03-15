import unittest
import allure
from page.check_detail_page import Detail
from utils import *


class TestCheckDetail():
    @classmethod
    def tearDownClass(cls):
        DriverTools.quit_driver()

    @allure.step("执行查看商品详情测试")
    def test_check_detail(self):
        result = Detail().check_detail()
        assert result is not None
