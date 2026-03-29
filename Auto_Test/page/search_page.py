import time
import allure
from base.base_page import BasePage
from config.search_config import *
from utils import DriverTools
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert


class SearchPage(BasePage):
    @allure.step("打开首页")
    def open_homepage(self):
        self.get_url("http://127.0.0.1:8000/")

    @allure.step("输入搜索关键词: {keyword}")
    def input_search_keyword(self, keyword):
        self.element_send_keys(*SEARCH_INPUT, keyword)

    @allure.step("点击搜索按钮")
    def click_search_button(self):
        self.element_click(*SEARCH_BUTTON)
        time.sleep(1)

    @allure.step("执行搜索: {keyword}")
    def search(self, keyword):
        self.open_homepage()
        self.input_search_keyword(keyword)
        self.click_search_button()
        time.sleep(2)

    @allure.step("获取搜索结果商品列表")
    def get_search_results(self):
        goods_list = self.get_elements(*GOODS_LIST)
        print("商品列表：",goods_list)
        if goods_list:
            items = goods_list[0].find_elements(*GOODS_ITEM)
            print("商品列表项：",items)
            results = []
            for item in items:
                try:
                    title_element = item.find_element(*GOODS_TITLE)
                    title = title_element.text
                    results.append(title)
                except:
                    continue
            return results
        return []

    @allure.step("获取搜索结果数量")
    def get_search_result_count(self):
        results = self.get_search_results()
        return len(results)

    @allure.step("验证搜索结果包含关键词: {keyword}")
    def verify_results_contain_keyword(self, keyword):
        results = self.get_search_results()
        if not results:
            return False, []
        matched_results = [r for r in results if keyword in r]
        return len(matched_results) > 0, matched_results

    @allure.step("验证搜索结果包含多个关键词: {keywords}")
    def verify_results_contain_keywords(self, keywords):
        results = self.get_search_results()
        if not results:
            return False, []
        keyword_list = keywords.split()
        matched_results = []
        for r in results:
            if all(kw in r for kw in keyword_list):
                matched_results.append(r)
        return len(matched_results) > 0, matched_results

    @allure.step("点击分页按钮: 第{page_num}页")
    def click_pagination_page(self, page_num):
        pagination = self.get_element(*PAGINATION)
        if pagination:
            page_links = pagination.find_elements(*PAGE_LINK)
            for link in page_links:
                if link.text == str(page_num):
                    link.click()
                    time.sleep(2)
                    return True
        return False

    @allure.step("获取当前激活页码")
    def get_active_page_number(self):
        active_element = self.get_element(*ACTIVE_PAGE)
        if active_element:
            return active_element.text
        return None

    @allure.step("点击第一个商品标题")
    def click_first_goods_title(self):
        goods_list = self.get_elements(*GOODS_LIST)
        if goods_list:
            items = goods_list[0].find_elements(*GOODS_ITEM)
            if items:
                title_link = items[0].find_element(*GOODS_LINK)
                first_goods_title = title_link.text
                title_link.click()
                time.sleep(2)
                return first_goods_title
        return None

    @allure.step("获取商品详情页标题")
    def get_detail_page_title(self):
        title_element = self.get_element(*DETAIL_TITLE)
        if title_element:
            return title_element.text
        return None

    @allure.step("获取商品详情页价格")
    def get_detail_page_price(self):
        price_element = self.get_element(*DETAIL_PRICE)
        if price_element:
            return price_element.text
        return None

    @allure.step("验证是否显示无结果提示")
    def is_no_result_displayed(self):
        try:
            alert_text = self.handle_alert_and_get_text()
            if alert_text and "您的查询结果为空" in alert_text:
                return True
            page_source = self.driver.page_source
            return "您的查询结果为空" in page_source or "暂无相关商品" in page_source
        except:
            return False

    @allure.step("处理弹窗并获取提示信息")
    def handle_alert_and_get_text(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            return alert_text
        except:
            return None

    @allure.step("检查是否有弹窗提示")
    def has_alert_prompt(self):
        try:
            alert_text = self.handle_alert_and_get_text()
            return alert_text is not None and "请输入" in alert_text
        except:
            return False

    @allure.step("获取搜索结果页面URL")
    def get_current_url(self):
        return self.driver.current_url


if __name__ == "__main__":
    search_page = SearchPage()
    search_page.search("草莓")
    results = search_page.get_search_results()
    print(f"搜索结果: {results}")
    DriverTools.quit_driver()
