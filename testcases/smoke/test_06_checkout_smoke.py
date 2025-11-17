import pytest
import allure
from pageobjects.smoke.HomePage import HomePage
from pageobjects.smoke.SearchResultsPage import SearchResultsPage

pytestmark = [pytest.mark.session_login, pytest.mark.usefixtures("session_logged_in")]
KEYWORD = "P806"

@allure.epic("ECSHOP Smoke")
@allure.feature("Checkout")
@allure.story("Prepare And Submit")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.smoke
def test_checkout_smoke(driver, base_url):
    HomePage(driver, base_url).open().assert_search_ready().search_and_assert_results(KEYWORD)
    product = SearchResultsPage(driver).open_first()
    cart = product.configure_all_and_add_to_cart(qty="2")
    checkout = cart.go_to_checkout()
    success_page = checkout.complete_and_submit()
    text = success_page.assert_success(strict=True)
    order_no = success_page.extract_order_number(text)
    allure.attach(text, "成功文案")
    if order_no:
        allure.attach(order_no, "订单号")

    # 在订单提交成功页面截图并作为 Allure 附件
    with allure.step("截图：订单提交成功页面"):
        try:
            png = driver.get_screenshot_as_png()
            allure.attach(png, name="订单提交成功页", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            # 若截图失败，将原因写入附件，方便排查
            allure.attach(str(e), name="截图失败原因", attachment_type=allure.attachment_type.TEXT)