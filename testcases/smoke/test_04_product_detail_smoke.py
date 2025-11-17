# import pytest
# import allure
# from pageobjects.smoke.HomePage import HomePage
# from pageobjects.smoke.SearchResultsPage import SearchResultsPage
#
# pytestmark = [pytest.mark.session_login, pytest.mark.usefixtures("session_logged_in")]
# KEYWORD = "P806"
#
# @allure.epic("ECSHOP Smoke")
# @allure.feature("Product")
# @allure.story("Detail Page Basic Info")
# @allure.severity(allure.severity_level.CRITICAL)
# @pytest.mark.smoke
# def test_product_detail_smoke(driver, base_url):
#     HomePage(driver, base_url).open().assert_search_ready().search_and_assert_results(KEYWORD)
#     product = SearchResultsPage(driver).open_first()
#     product.assert_basic_info()