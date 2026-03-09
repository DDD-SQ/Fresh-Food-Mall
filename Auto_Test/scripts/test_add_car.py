import unittest
import allure
from page.add_car_page import Add
from utils import *


class TestAddCar():
    @classmethod
    def tearDownClass(cls):
        DriverTools.quit_driver()

    @allure.step("执行添加商品到购物车测试")
    def test_add_car(self):
        result = Add().add()
        assert result is not None
