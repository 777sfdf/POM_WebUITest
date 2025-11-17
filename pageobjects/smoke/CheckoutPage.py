"""
CheckoutPage
- 选择 配送/支付/包装/贺卡/缺货处理
- 组合方法：prepare_order（不提交）、complete_and_submit（提交并跳转成功页）
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    SHIPPING_OPTION = (By.XPATH, "//input[@name='shipping' and @value='5']")
    PAYMENT_OPTION = (By.XPATH, "//input[@name='payment' and @value='3']")
    PACK_OPTION = (By.XPATH, "//input[@name='pack' and @value='1']")
    CARD_OPTION = (By.XPATH, "//input[@name='card' and @value='1']")
    HOW_OOS_OPTION = (By.XPATH, "//input[@name='how_oos' and @value='2']")
    SUBMIT_ORDER = (By.XPATH, '//input[@type="image" and @src="themes/default/images/bnt_subOrder.gif"]')

    def __init__(self, driver: WebDriver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def select_shipping(self):
        self.wait.until(EC.element_to_be_clickable(self.SHIPPING_OPTION)).click()
        return self

    def select_payment(self):
        self.wait.until(EC.presence_of_element_located(self.PAYMENT_OPTION)).click()
        return self

    def select_pack(self):
        self.wait.until(EC.element_to_be_clickable(self.PACK_OPTION)).click()
        return self

    def select_card(self):
        self.wait.until(EC.element_to_be_clickable(self.CARD_OPTION)).click()
        return self

    def select_how_oos(self):
        self.wait.until(EC.element_to_be_clickable(self.HOW_OOS_OPTION)).click()
        return self

    def assert_submit_present(self):
        btn = self.wait.until(EC.presence_of_element_located(self.SUBMIT_ORDER))
        assert btn.is_displayed(), "提交订单按钮不可见"
        return self

    def submit_and_go_success(self):
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_ORDER)).click()
        from pageobjects.smoke.OrderSuccessPage import OrderSuccessPage
        return OrderSuccessPage(self.driver)

    def prepare_order(self):
        return (
            self.select_shipping()
                .select_payment()
                .select_pack()
                .select_card()
                .select_how_oos()
                .assert_submit_present()
        )

    def complete_and_submit(self):
        self.prepare_order()
        return self.submit_and_go_success()