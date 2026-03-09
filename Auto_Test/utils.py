import json
import logging
from logging import handlers
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class DriverTools:
    __driver = None

    @classmethod
    def get_driver(cls):
        if cls.__driver is None:
            # 指定ChromeDriver路径
            driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")
            service = Service(executable_path=driver_path)
            cls.__driver = webdriver.Chrome(service=service)
            cls.__driver.maximize_window()
        return cls.__driver

    @classmethod
    def quit_driver(cls):
        if cls.__driver is not None:
            cls.__driver.quit()
            cls.__driver = None
        return cls.__driver


class DataTools:
    @classmethod
    def get_Add_data(cls):
        file = open("./data/AddGoods.json", "r", encoding="utf-8")
        dict1 = json.load(file)
        file.close()
        list1 = []
        for n in dict1.values():
            list1.append((n["goods_name"], n["sort"], n["h_price"], n["m_price"]))
        return list1

    @classmethod
    def get_add_data(cls):
        file = open("./data/AddCar.json", "r", encoding="utf-8")
        dict1 = json.load(file)
        file.close()
        list1 = []
        for n in dict1.values():
            list1.append((n["ele1"], n["ele2"], n["expect"]))
        return list1

    @classmethod
    def get_login_data(cls):
        file = open("./data/login.json", "r", encoding="utf-8")
        dict1 = json.load(file)
        list1 = []
        for n in dict1:
            list1.append((dict1[n]["username"],
                          dict1[n]["password"],
                          dict1[n]["verify"],
                          dict1[n]["expect"]))
        return list1


class LogTools:
    __logger = None

    @classmethod
    def init_logger(cls):
        if cls.__logger is None:
            cls.__logger = logging.getLogger()
            cls.__logger.setLevel(logging.INFO)  # 设置日志器对应的日志级别
            # 定义控制台处理器
            sh = logging.StreamHandler()  # 在屏幕输出log信息
            # 定义文件处理器, 下面括号中是log文件的文件名和字符集编码格式
            fh = logging.handlers.TimedRotatingFileHandler("./log/logcat.log", encoding="UTF-8")    # 把log写入到文件
            # 定义格式
            fmt = "%(asctime)s %(levelname)s %(name)s %(filename)s %(lineno)d %(message)s"
            formatter = logging.Formatter(fmt)
            # 设置处理器格式
            sh.setFormatter(formatter)  # 把log的格式设置到屏幕对象中
            fh.setFormatter(formatter)  # 把log的格式设置到文件对象中
            # 把处理器添加到handler中
            cls.__logger.addHandler(sh)
            cls.__logger.addHandler(fh)

    @classmethod
    def log_info(cls, msg):
        logging.info(msg)

    @classmethod
    def log_error(cls, msg):
        logging.error(msg)
