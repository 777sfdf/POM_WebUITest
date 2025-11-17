"""
CheckoutPage 页面对象
职责：配送方式/支付方式/包装/贺卡/缺货处理选择与提交订单。
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
    SUBMIT_ORDER_BTN = (By.XPATH, '//input[@type="image" and @src="themes/default/images/bnt_subOrder.gif"]')

    def __init__(self, driver: WebDriver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def select_shipping(self):
        self.wait.until(EC.element_to_be_clickable(self.SHIPPING_OPTION)).click()

    def select_payment(self):
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_OPTION)).click()

    def select_pack(self):
        try:
            self.wait.until(EC.element_to_be_clickable(self.PACK_OPTION)).click()
        except Exception:
            pass

    def select_card(self):
        try:
            self.wait.until(EC.element_to_be_clickable(self.CARD_OPTION)).click()
        except Exception:
            pass

    def select_how_oos(self):
        try:
            self.wait.until(EC.element_to_be_clickable(self.HOW_OOS_OPTION)).click()
        except Exception:
            pass

    def submit_order(self):
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_ORDER_BTN)).click()
        from pageobjects.order.OrderSuccessPage import OrderSuccessPage
        return OrderSuccessPage(self.driver)

    def complete_checkout(self):
        """
        组合操作：依次选择必要项目并提交订单。
        """
        self.select_shipping()
        self.select_payment()
        self.select_pack()
        self.select_card()
        self.select_how_oos()
        return self.submit_order()