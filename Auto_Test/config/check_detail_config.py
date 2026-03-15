from selenium.webdriver.common.by import By

# 查看详情流程
SEARCH_INPUT = By.NAME, "q", "草莓"     # 搜索框
SEARCH_CLICK = By.XPATH, "//input[@type='button']"      # 点击搜素
CLICK_DETAIL = By.XPATH, "//a[@href='/18/']"      # 点击查看详情
GOODS_TEXT = By.XPATH, "//h3[contains(text(),'草莓')]"  # 商品信息
