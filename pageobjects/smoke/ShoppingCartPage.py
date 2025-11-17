"""
ShoppingCartPage
职责：
-（可选）断言购物车页已显示（这里留一个轻量断言接口）
- 进入结算页 -> 返回 CheckoutPage
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ShoppingCartPage:
    GO_CHECKOUT = (By.XPATH, "//a[@href='flow.php?step=checkout']")

    def __init__(self, driver: WebDriver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def assert_in_cart(self):
        # 可扩展：比如检查“您的购物车”字样；目前轻量化
        return self

    def go_to_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.GO_CHECKOUT)).click()
        from pageobjects.smoke.CheckoutPage import CheckoutPage
        return CheckoutPage(self.driver)