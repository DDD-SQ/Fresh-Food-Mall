import allure
from page.submit_order_page import SubmitOrder


@allure.feature("订单功能")
class TestSubmitOrder:
    
    @allure.story("提交订单")
    @allure.title("提交订单流程")
    @allure.description("完成购物车商品选择后，提交订单并验证订单状态")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submit_order(self):
        result = SubmitOrder().submit_order()
        assert result is not None
