from selenium.webdriver.common.by import By

# 查看详情流程
SEARCH_INPUT = By.NAME, "q", "草莓"     # 搜索框
SEARCH_CLICK = By.XPATH, "//input[@type='button']"      # 点击搜素
CLICK_DETAIL = By.XPATH, "//li/h4//a"      # 点击查看详情
CLICK_BUY = By.ID, "buy_now"      # 点击购买
CLICK_CHECKOUT = By.XPATH, "//a[text()='去结算']"      # 点击去结算
CLICK_SUBMIT = By.XPATH, "//a[text()='提交订单']"      # 点击提交订单
ORDER_INFO = By.XPATH, "//li[text()='新鲜草莓']"
PAY_INFO = By.XPATH, "//td[text()='已付款']"
