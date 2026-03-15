import time
import allure
from base.base_page import BasePage
from config.check_detail_config import *
from utils import DriverTools


class Detail(BasePage):
    @allure.step("打开首页")
    def open_homepage(self):
        self.get_url("http://127.0.0.1:8000/")

    @allure.step("搜索商品")
    def search_product(self):
        self.element_send_keys(*SEARCH_INPUT)
        self.element_click(*SEARCH_CLICK)
        time.sleep(3)

    @allure.step("点击商品详情")
    def click_detail(self):
        self.element_click(*CLICK_DETAIL)

    @allure.step("获取商品信息")
    def get_product_info(self):
        return self.get_element_text(*GOODS_TEXT)

    @allure.step("验证商品信息")
    def verify_product_contains(self):
        product_text = self.get_product_info()
        assert "草莓" in product_text, f"商品信息中不包含草莓"
        return product_text

    def check_detail(self):
        self.open_homepage()
        self.search_product()
        self.click_detail()
        return self.verify_product_contains()



if __name__ == "__main__":
    Detail().check_detail()
    DriverTools.quit_driver()
