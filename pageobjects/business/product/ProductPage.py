"""
ProductPage 页面对象
职责：商品详情页上的数量、规格、配件选择与加入购物车。
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductPage:
    QTY_INPUT = (By.ID, "number")
    SPEC_COLOR = (By.ID, "spec_value_242")
    SPEC_MEMORY = (By.ID, "spec_value_245")
    SPEC_ACCESSORY_1 = (By.ID, "spec_value_243")
    SPEC_ACCESSORY_2 = (By.ID, "spec_value_168")
    ADD_TO_CART_BTN = (By.XPATH, "//a[@href='javascript:addToCart(24)']")
    PROCEED_TO_CHECKOUT = (By.XPATH, "//a[@href='flow.php?step=checkout']")

    PRICE_LOCATORS = [
        (By.CSS_SELECTOR, ".shop_price"),  # 如果模板里有
        (By.XPATH, "//font[contains(@class,'shop')]"),
    ]
    STOCK_LOCATORS = [
        (By.XPATH, "//*[contains(text(),'库存')]"),
        (By.CSS_SELECTOR, ".goods_number"),
    ]

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def set_quantity(self, qty: str):
        el = self.wait.until(EC.presence_of_element_located(self.QTY_INPUT))
        el.clear()
        el.send_keys(qty)

    def choose_specs(self):
        # 颜色
        try:
            self.wait.until(EC.element_to_be_clickable(self.SPEC_COLOR)).click()
        except Exception:
            pass
        # 内存
        try:
            self.wait.until(EC.element_to_be_clickable(self.SPEC_MEMORY)).click()
        except Exception:
            pass
        # 配件
        for acc in (self.SPEC_ACCESSORY_1, self.SPEC_ACCESSORY_2):
            try:
                self.wait.until(EC.element_to_be_clickable(acc)).click()
            except Exception:
                pass

    def assert_basic_info_visible(self):
        # 价格
        price_visible = False
        for loc in self.PRICE_LOCATORS:
            try:
                el = self.driver.find_element(*loc)
                if el.is_displayed():
                    price_visible = True
                    break
            except Exception:
                continue
        assert price_visible, "商品价格未显示"

        # 库存（可选，如需要可加强）
        stock_visible = False
        for loc in self.STOCK_LOCATORS:
            try:
                el = self.driver.find_element(*loc)
                if el.is_displayed():
                    stock_visible = True
                    break
            except Exception:
                continue
        # 不强制库存一定有文本（部分模板可能隐藏），可根据需要断言：
        # assert stock_visible, "库存信息未显示"

    def add_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BTN)).click()

    def proceed_to_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.PROCEED_TO_CHECKOUT)).click()
        from pageobjects.business.checkout.CheckoutPage import CheckoutPage
        return CheckoutPage(self.driver)