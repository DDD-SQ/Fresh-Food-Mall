import allure
from page.check_detail_page import Detail


@allure.feature("商品详情功能")
class TestCheckDetail:
    
    @allure.story("查看商品详情")
    @allure.title("查看商品详情页")
    @allure.description("进入商品详情页，验证商品信息正确显示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_check_detail(self):
        result = Detail().check_detail()
        assert result is not None
