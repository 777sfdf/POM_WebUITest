import pytest
import allure
from pageobjects.smoke.HomePage import HomePage
from pageobjects.smoke.SearchResultsPage import SearchResultsPage

pytestmark = [pytest.mark.session_login, pytest.mark.usefixtures("session_logged_in")]
KEYWORD = "P806"

@allure.epic("ECSHOP Smoke")
@allure.feature("Search")
@allure.story("Search Results Visible")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_search_results_smoke(driver, base_url):
    HomePage(driver, base_url).open().assert_search_ready().search_and_assert_results(KEYWORD)
    sr = SearchResultsPage(driver)
    assert sr.has_any(), "搜索结果为空"
    first = sr.list_results()[0]
    allure.attach(f"{first['title']} | {first['link']}", "首条结果")