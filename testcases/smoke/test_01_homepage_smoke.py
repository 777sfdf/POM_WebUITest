import pytest
import allure
from pageobjects.smoke.HomePage import HomePage
from pageobjects.smoke.SearchResultsPage import SearchResultsPage
from common.screenshot_utils import attach_fullscreen

DEFAULT_KEYWORD = "P806"

@allure.epic("ECSHOP Smoke")
@allure.feature("Home")
@allure.story("Welcome Text")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_01_welcome_text(driver, base_url):
    home = HomePage(driver, base_url).open()
    home.assert_welcome_visible()
    # 元素级近景（仅文字）
    home.attach_welcome_text_screenshot("欢迎光临本店_元素截图")
    # 可选：也附一张全屏，便于上下文识别
    # attach_fullscreen("首页_含地址栏_截图")

@allure.epic("ECSHOP Smoke")
@allure.feature("Home")
@allure.story("Login Link")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_home_login_link_navigates(driver, base_url):
    home = HomePage(driver, base_url).open()
    home.assert_welcome_visible().click_login_and_assert_navigated()
    allure.attach(driver.current_url, "登录页URL")
    # 全屏截图（包含地址栏）
    attach_fullscreen("登录页_含地址栏_截图")

@allure.epic("ECSHOP Smoke")
@allure.feature("Home")
@allure.story("Register Link")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_home_register_link_navigates(driver, base_url):
    home = HomePage(driver, base_url).open()
    home.assert_welcome_visible().click_register_and_assert_navigated()
    allure.attach(driver.current_url, "注册页URL")
    # 全屏截图（包含地址栏）
    attach_fullscreen("注册页_含地址栏_截图")

@allure.epic("ECSHOP Smoke")
@allure.feature("Home")
@allure.story("Search Box")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_home_search_navigates(driver, base_url):
    home = HomePage(driver, base_url).open().assert_search_ready()
    home.search_and_assert_results(DEFAULT_KEYWORD)

    # 全屏截图（包含地址栏）
    attach_fullscreen("搜索结果页_含地址栏_截图")

    # 使用 SearchResultsPage 再次读取首条信息，避免直接访问旧元素导致 stale
    sr = SearchResultsPage(driver)
    results = sr.list_results()
    assert results, "搜索结果为空"
    first = results[0]
    # allure.attach(f"结果数: {len(results)}; 首条: {first['title']} | {first['link']}", "搜索结果信息")
    allure.attach(f"{first['link']}", "搜索结果信息")