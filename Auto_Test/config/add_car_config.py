from selenium.webdriver.common.by import By

# 加入购物车流程
SEARCH_INPUT = By.NAME, "q", "草莓"     # 搜索框
SEARCH_CLICK = By.XPATH, "//input[@type='button']"      # 点击搜素
ADD_CAR_CLICK = By.CLASS_NAME, "add_goods"    # 添加搜索出来的第一个商品进入购物车
CAR_TEXT = By.CLASS_NAME, "col03"
