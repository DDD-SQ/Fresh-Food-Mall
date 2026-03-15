import time
import allure
from base.base_page import BasePage
from config.submit_order_config import *
from utils import DriverTools


class SubmitOrder(BasePage):
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

    @allure.step("点击立即购买")
    def click_buy(self):
        self.element_click(*CLICK_BUY)

    @allure.step("点击去结算")
    def click_checkout(self):
        self.element_click(*CLICK_CHECKOUT)

    @allure.step("点击提交订单")
    def click_submit(self):
        self.element_click(*CLICK_SUBMIT)

    @allure.step("获取订单信息")
    def get_order_info(self):
        order_info = self.get_element_text(*ORDER_INFO)
        pay_info = self.get_element_text(*PAY_INFO)
        return order_info, pay_info

    @allure.step("验证订单信息")
    def verify_order_contains(self):
        order_info, pay_info = self.get_order_info()
        assert "新鲜草莓" in order_info, f"订单信息中不包含新鲜草莓"
        assert "已付款" == pay_info, f"订单未付款"
        return True

    def submit_order(self):
        self.open_homepage()
        self.search_product()
        self.click_detail()
        self.click_buy()
        time.sleep(1)
        self.click_checkout()
        time.sleep(1)
        self.click_submit()
        time.sleep(3)
        self.get_order_info()
        return self.verify_order_contains()



if __name__ == "__main__":
    Detail().check_detail()
    DriverTools.quit_driver()
