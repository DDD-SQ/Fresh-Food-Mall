from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select

from utils import *


class BasePage:
    def __init__(self):
        self.driver = DriverTools.get_driver()
        self.log = LogTools()

    def get_url(self, url):
        self.driver.get(url)

    def get_element(self, by, element_name):
        wait = WebDriverWait(self.driver, 5, 0.5)  # 最大等待时间10秒，每隔1s定位一次元素
        try:
            return wait.until(lambda x: x.find_element(by, element_name))
        except TimeoutException:
            self.log.log_info("%s 没有找到", element_name)
            return None

    def get_elements(self, by, element_name):
        wait = WebDriverWait(self.driver, 5, 0.5)  # 最大等待时间10秒，每隔1s定位一次元素
        try:
            return wait.until(lambda x: x.find_elements(by, element_name))
        except TimeoutException:
            self.log.log_info("%s 没有找到", element_name)
            return None

    def element_send_keys(self, by, element_name, key):
        element = self.get_element(by, element_name)
        if element is not None:
            element.clear()
            return element.send_keys(key)

    def element_click(self, by, element_name):
        element = self.get_element(by, element_name)
        if element is not None:
            return element.click()

    def get_element_text(self, by, element_name):
        element = self.get_element(by, element_name)
        if element is not None:
            return self.get_element(by, element_name).text

    # 在BasePage类中添加以下方法
    def get_element_text_by_index(self, by, element_name, index):
        elements = self.get_elements(by, element_name)
        if elements and len(elements) > index:
            return elements[index].text
        return None

    def switch_frame(self, by, element_name):
        element = self.get_element(by, element_name)
        if element is not None:
            self.driver.switch_to.frame(self.get_element(by, element_name))

    def switch_window(self):
        return self.driver.switch_to.window(self.driver.window_handles[-1])     # 切换到最新打开的窗口

    def action_move_to(self, by, element_name):
        element = self.get_element(by, element_name)
        if element is not None:
            action = ActionChains(self.driver)
            action.move_to_element(self.get_element(by, element_name))
            action.perform()

    def select_by_index(self, by, element_name, index):
        element = self.get_element(by, element_name)
        if element is not None:
            Select(self.get_element(by, element_name)).select_by_index(index)

    def select_by_value(self, by, element_name, value):
        element = self.get_element(by, element_name)
        if element is not None:
            Select(self.get_element(by, element_name)).select_by_value(value)

    def select_by_text(self, by, element_name, text):
        element = self.get_element(by, element_name)
        if element is not None:
            Select(self.get_element(by, element_name)).select_by_visible_text(text)

    def window_scroll(self, x, y):
        js = f"window.scrollTo({x},{y})"
        self.driver.execute_script(js)

    def document_scroll(self, get, element_name, x, y):
        js = f"document.{get}({element_name}).scrollTo({x},{y})"
        self.driver.execute_script(js)
