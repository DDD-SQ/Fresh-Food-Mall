from selenium.webdriver.common.by import By

SEARCH_INPUT = By.NAME, "q"                                    # 搜索输入框
SEARCH_BUTTON = By.XPATH, "//input[@type='button']"            # 搜索按钮
GOODS_LIST = By.CLASS_NAME, "goods_type_list"         # 商品列表容器
GOODS_ITEM = By.TAG_NAME, "li"                                 # 商品列表项
GOODS_TITLE = By.TAG_NAME, "h4"                                # 商品标题
GOODS_LINK = By.CSS_SELECTOR, "h4 a"                           # 商品标题链接
PAGINATION = By.CLASS_NAME, "pagenation"                       # 分页容器
PAGE_LINK = By.TAG_NAME, "a"                                   # 分页链接
ACTIVE_PAGE = By.CSS_SELECTOR, ".pagenation a.active"          # 当前激活页码
NO_RESULT_TIP = By.XPATH, "//script[contains(text(), '您的查询结果为空')]"  # 无搜索结果提示
ALERT_TEXT = By.XPATH, "//script[contains(text(), '请输入搜索内容')]"      # 空关键词弹窗提示
GOODS_PRICE = By.CLASS_NAME, "prize"                           # 商品价格
DETAIL_TITLE = By.CSS_SELECTOR, ".goods_detail_list h3"        # 商品详情页标题
DETAIL_PRICE = By.ID, "gprice"                                 # 商品详情页价格
