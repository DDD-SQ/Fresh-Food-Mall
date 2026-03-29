import json
import logging
from logging import handlers
import os
import sys
import platform
import requests
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class DriverTools:
    __driver = None
    __driver_path = None

    @classmethod
    def _is_linux(cls):
        """判断是否为Linux系统"""
        return platform.system().lower() == 'linux'

    @classmethod
    def _get_chrome_version(cls):
        """获取Chrome浏览器版本（兼容Windows和Linux）"""
        if cls._is_linux():
            return cls._get_chrome_version_linux()
        else:
            return cls._get_chrome_version_windows()

    @classmethod
    def _get_chrome_version_windows(cls):
        """Windows系统获取Chrome版本"""
        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
            version, _ = winreg.QueryValueEx(key, "version")
            return version
        except:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome")
                version, _ = winreg.QueryValueEx(key, "version")
                return version
            except:
                return None

    @classmethod
    def _get_chrome_version_linux(cls):
        """Linux系统获取Chrome版本"""
        import subprocess
        try:
            result = subprocess.run(
                ['google-chrome', '--version'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.strip().split()[-1]
                return version
        except:
            pass
        try:
            result = subprocess.run(
                ['google-chrome-stable', '--version'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.strip().split()[-1]
                return version
        except:
            pass
        try:
            result = subprocess.run(
                ['chromium', '--version'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.strip().split()[-1]
                return version
        except:
            pass
        return None

    @classmethod
    def _get_driver_filename(cls):
        """获取驱动文件名（根据操作系统）"""
        if cls._is_linux():
            return "chromedriver"
        else:
            return "chromedriver.exe"

    @classmethod
    def _get_driver_zip_name(cls):
        """获取驱动压缩包名称（根据操作系统）"""
        if cls._is_linux():
            return "chromedriver_linux64.zip"
        else:
            return "chromedriver_win32.zip"

    @classmethod
    def _download_chromedriver(cls, version):
        """从淘宝镜像下载chromedriver"""
        cache_dir = os.path.join(os.path.dirname(__file__), "drivers")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        
        driver_filename = cls._get_driver_filename()
        driver_file = os.path.join(cache_dir, driver_filename)
        
        if os.path.exists(driver_file):
            return driver_file
        
        zip_name = cls._get_driver_zip_name()
        mirror_url = f"https://registry.npmmirror.com/-/binary/chromedriver/{version}/{zip_name}"
        print(f"正在从淘宝镜像下载 ChromeDriver: {mirror_url}")
        
        zip_path = os.path.join(cache_dir, "chromedriver.zip")
        response = requests.get(mirror_url, stream=True)
        if response.status_code == 200:
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(cache_dir)
            os.remove(zip_path)
            
            if cls._is_linux():
                os.chmod(driver_file, 0o755)
            
            print(f"ChromeDriver 下载完成: {driver_file}")
            return driver_file
        else:
            raise Exception(f"下载 ChromeDriver 失败，状态码: {response.status_code}")

    @classmethod
    def _get_chrome_options(cls):
        """获取Chrome配置选项（兼容Docker环境）"""
        options = Options()
        
        if cls._is_linux():
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-software-rasterizer')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-translate')
            options.add_argument('--disable-web-security')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--start-maximized')
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            options.binary_location = '/usr/bin/google-chrome'
        else:
            options.add_argument('--start-maximized')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-notifications')
            options.add_argument('--ignore-certificate-errors')
        
        return options

    @classmethod
    def get_driver(cls):
        if cls.__driver is None:
            chrome_version = cls._get_chrome_version()
            if chrome_version:
                print(f"检测到 Chrome 版本: {chrome_version}")
                try:
                    driver_path = cls._download_chromedriver(chrome_version)
                    service = Service(executable_path=driver_path)
                except Exception as e:
                    print(f"自动下载失败: {e}，使用系统 chromedriver")
                    service = Service()
            else:
                print("未检测到 Chrome 版本，使用系统 chromedriver")
                service = Service()
            
            options = cls._get_chrome_options()
            cls.__driver = webdriver.Chrome(service=service, options=options)
            
            if not cls._is_linux():
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
            cls.__logger.setLevel(logging.INFO)
            sh = logging.StreamHandler()
            fh = logging.handlers.TimedRotatingFileHandler("./log/logcat.log", encoding="UTF-8")
            fmt = "%(asctime)s %(levelname)s %(name)s %(filename)s %(lineno)d %(message)s"
            formatter = logging.Formatter(fmt)
            sh.setFormatter(formatter)
            fh.setFormatter(formatter)
            cls.__logger.addHandler(sh)
            cls.__logger.addHandler(fh)

    @classmethod
    def log_info(cls, msg, *args):
        if args:
            logging.info(msg, *args)
        else:
            logging.info(msg)

    @classmethod
    def log_error(cls, msg, *args):
        if args:
            logging.error(msg, *args)
        else:
            logging.error(msg)
