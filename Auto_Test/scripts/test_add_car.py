import allure
from page.add_car_page import Add


@allure.feature("购物车功能")
class TestAddCar:
    
    @allure.story("添加购物车")
    @allure.title("添加商品到购物车")
    @allure.description("搜索商品后，将第一个商品添加到购物车，验证商品信息正确")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_car(self):
        result = Add().add()
        assert result is not None
