import unittest
import allure
from page.submit_order_page import SubmitOrder
from utils import *


class TestSubmitOrder():
    @classmethod
    def tearDownClass(cls):
        DriverTools.quit_driver()

    @allure.step("执行查看商品详情测试")
    def test_submit_order(self):
        result = SubmitOrder().submit_order()
        assert result is not None
