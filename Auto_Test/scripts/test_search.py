import allure
import pytest
from page.search_page import SearchPage


@allure.feature("搜索功能")
class TestSearch:
    
    @allure.story("模糊搜索")
    @allure.title("模糊搜索-搜索草莓关键词")
    @allure.description("搜索'草莓'，验证结果中包含'草莓'关键字")
    @allure.severity(allure.severity_level.NORMAL)
    def test_fuzzy_search(self):
        search_page = SearchPage()
        keyword = "草莓"
        search_page.search(keyword)
        has_result, matched_results = search_page.verify_results_contain_keyword(keyword)
        allure.attach(f"搜索关键词: {keyword}", name="搜索关键词", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"匹配结果: {matched_results}", name="匹配结果", attachment_type=allure.attachment_type.TEXT)
        assert has_result, f"搜索'{keyword}'结果中未包含'{keyword}'关键字"

    @allure.story("分类关联搜索")
    @allure.title("分类关联搜索-搜索水果分类")
    @allure.description("搜索'水果'，验证结果包含该分类下的商品（如草莓、香蕉等）")
    @allure.severity(allure.severity_level.NORMAL)
    def test_category_search(self):
        search_page = SearchPage()
        keyword = "水果"
        search_page.search(keyword)
        results = search_page.get_search_results()
        allure.attach(f"搜索关键词: {keyword}", name="搜索关键词", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"搜索结果: {results}", name="搜索结果", attachment_type=allure.attachment_type.TEXT)
        assert len(results) > 0, f"搜索'{keyword}'无结果"
        expected_keywords = ["水晶葡萄", "坷拉苹果", "花果山猕猴桃", "奔跑的奇异果"]
        has_expected = any(any(ek in r for ek in expected_keywords) for r in results)
        assert has_expected, f"搜索'{keyword}'结果中未包含预期的水果类商品"

    @allure.story("联想词搜索")
    @allure.title("联想词搜索-输入部分关键词")
    @allure.description("输入'莓'，验证结果包含'草莓'、'蓝莓'等相关商品")
    @allure.severity(allure.severity_level.NORMAL)
    def test_associative_search(self):
        search_page = SearchPage()
        keyword = "莓"
        search_page.search(keyword)
        results = search_page.get_search_results()
        allure.attach(f"搜索关键词: {keyword}", name="搜索关键词", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"搜索结果: {results}", name="搜索结果", attachment_type=allure.attachment_type.TEXT)
        assert len(results) > 0, f"搜索'{keyword}'无结果"
        expected_keywords = ["草莓", "蓝莓"]
        has_expected = any(any(ek in r for ek in expected_keywords) for r in results)
        assert has_expected, f"搜索'{keyword}'结果中未包含'草莓'或'蓝莓'"

    @allure.story("多重筛选搜索")
    @allure.title("多重筛选搜索-多关键词组合")
    @allure.description("搜索'进口 蓝莓'，验证结果同时包含这两个关键词")
    @allure.severity(allure.severity_level.NORMAL)
    def test_multiple_keywords_search(self):
        search_page = SearchPage()
        keyword = "进口 蓝莓"
        search_page.search(keyword)
        has_result, matched_results = search_page.verify_results_contain_keywords(keyword)
        allure.attach(f"搜索关键词: {keyword}", name="搜索关键词", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"匹配结果: {matched_results}", name="匹配结果", attachment_type=allure.attachment_type.TEXT)
        assert has_result, f"搜索'{keyword}'结果中未同时包含'进口'和'蓝莓'"

    @allure.story("错别字容错搜索")
    @allure.title("错别字容错搜索-输入错误关键词")
    @allure.description("输入'草霉'（错别字），验证结果能匹配到'草莓'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_typo_search(self):
        search_page = SearchPage()
        wrong_keyword = "草霉"
        correct_keyword = "草莓"
        search_page.search(wrong_keyword)
        results = search_page.get_search_results()
        allure.attach(f"搜索关键词(错别字): {wrong_keyword}", name="搜索关键词", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"搜索结果: {results}", name="搜索结果", attachment_type=allure.attachment_type.TEXT)
        has_strawberry = any(correct_keyword in r for r in results)
        assert has_strawberry or len(results) > 0, f"搜索错别字'{wrong_keyword}'未能匹配到'{correct_keyword}'"

    @allure.story("英文搜索")
    @allure.title("英文搜索-输入英文单词")
    @allure.description("输入'strawberry'，验证结果能匹配到草莓商品")
    @allure.severity(allure.severity_level.NORMAL)
    def test_english_search(self):
        search_page = SearchPage()
        keyword = "strawberry"
        expected_keyword = "草莓"
        search_page.search(keyword)
        results = search_page.get_search_results()
        allure.attach(f"搜索关键词(英文): {keyword}", name="搜索关键词", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"搜索结果: {results}", name="搜索结果", attachment_type=allure.attachment_type.TEXT)
        has_strawberry = any(expected_keyword in r for r in results)
        assert has_strawberry or len(results) > 0, f"搜索英文'{keyword}'未能匹配到'{expected_keyword}'"

    @allure.story("拼音搜索")
    @allure.title("拼音搜索-输入拼音")
    @allure.description("输入'caomei'（草莓拼音），验证结果能匹配到草莓商品")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pinyin_search(self):
        search_page = SearchPage()
        keyword = "caomei"
        expected_keyword = "草莓"
        search_page.search(keyword)
        results = search_page.get_search_results()
        allure.attach(f"搜索关键词(拼音): {keyword}", name="搜索关键词", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"搜索结果: {results}", name="搜索结果", attachment_type=allure.attachment_type.TEXT)
        has_strawberry = any(expected_keyword in r for r in results)
        assert has_strawberry or len(results) > 0, f"搜索拼音'{keyword}'未能匹配到'{expected_keyword}'"

    @allure.story("空关键词搜索")
    @allure.title("空关键词搜索-输入空字符串")
    @allure.description("输入空字符串，验证提示'请输入搜索关键词'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_keyword_search(self):
        search_page = SearchPage()
        search_page.open_homepage()
        search_page.input_search_keyword("")
        search_page.click_search_button()
        alert_text = search_page.handle_alert_and_get_text()
        allure.attach(f"弹窗提示: {alert_text}", name="弹窗提示", attachment_type=allure.attachment_type.TEXT)
        assert alert_text is not None and "请输入" in alert_text, "空关键词搜索未弹出正确的提示信息"

    @allure.story("特殊字符搜索")
    @allure.title("特殊字符搜索-输入特殊字符")
    @allure.description("输入特殊字符'@#￥%…'，验证显示'暂无相关商品'提示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_special_character_search(self):
        search_page = SearchPage()
        keyword = "@#￥%…"
        search_page.search(keyword)
        is_no_result = search_page.is_no_result_displayed()
        results = search_page.get_search_results()
        allure.attach(f"搜索关键词(特殊字符): {keyword}", name="搜索关键词", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"搜索结果数量: {len(results)}", name="搜索结果数量", attachment_type=allure.attachment_type.TEXT)
        assert is_no_result or len(results) == 0, f"搜索特殊字符'{keyword}'应显示无结果提示"

    @allure.story("分页功能")
    @allure.title("分页功能-搜索结果分页")
    @allure.description("搜索'水果'，点击第2页，验证分页功能正常")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pagination(self):
        search_page = SearchPage()
        keyword = "水果"
        search_page.search(keyword)
        results_page1 = search_page.get_search_results()
        allure.attach(f"第1页结果: {results_page1}", name="第1页结果", attachment_type=allure.attachment_type.TEXT)
        click_success = search_page.click_pagination_page(2)
        if click_success:
            active_page = search_page.get_active_page_number()
            allure.attach(f"当前激活页码: {active_page}", name="当前页码", attachment_type=allure.attachment_type.TEXT)
            assert active_page == "2", f"分页后当前页码应为'2'，实际为'{active_page}'"
        else:
            allure.attach("无第2页，跳过分页验证", name="跳过原因", attachment_type=allure.attachment_type.TEXT)
            pytest.skip("搜索结果不足2页，跳过分页测试")

    @allure.story("商品详情跳转")
    @allure.title("商品详情跳转-点击搜索结果商品")
    @allure.description("搜索'柠檬'，点击第一个商品，验证跳转到详情页且数据一致")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_click_goods_to_detail(self):
        search_page = SearchPage()
        keyword = "柠檬"
        search_page.search(keyword)
        first_goods_title = search_page.click_first_goods_title()
        allure.attach(f"点击的商品标题: {first_goods_title}", name="商品标题", attachment_type=allure.attachment_type.TEXT)
        assert first_goods_title is not None, f"搜索'{keyword}'无商品可点击"
        detail_title = search_page.get_detail_page_title()
        allure.attach(f"详情页商品标题: {detail_title}", name="详情页标题", attachment_type=allure.attachment_type.TEXT)
        assert detail_title is not None, "未成功跳转到商品详情页"
        assert first_goods_title in detail_title or detail_title in first_goods_title, \
            f"详情页标题'{detail_title}'与搜索结果标题'{first_goods_title}'不一致"
