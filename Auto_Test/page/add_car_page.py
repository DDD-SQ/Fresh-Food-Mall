import time
import allure
from base.base_page import BasePage
from config.add_car_config import *
from utils import DriverTools


class Add(BasePage):
    @allure.step("打开首页")
    def open_homepage(self):
        self.get_url("http://127.0.0.1:8000/")

    @allure.step("搜索商品")
    def search_product(self):
        self.element_send_keys(*SEARCH_INPUT)
        self.element_click(*SEARCH_CLICK)
        time.sleep(3)

    @allure.step("添加第一个商品到购物车")
    def add_to_cart(self):
        self.element_click(*ADD_CAR_CLICK)

    @allure.step("获取商品信息")
    def get_product_info(self):
        return self.get_element_text_by_index(*CAR_TEXT, 1)

    @allure.step("验证商品信息")
    def verify_product_contains(self):
        product_text = self.get_product_info()
        assert "草莓" in product_text, f"商品信息中不包含草莓"
        return product_text

    def add(self):
        self.open_homepage()
        self.search_product()
        self.add_to_cart()
        return self.verify_product_contains()



if __name__ == "__main__":
    Add().add()
    DriverTools.quit_driver()
