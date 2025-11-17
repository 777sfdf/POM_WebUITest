
"""
ProductDetailPage
- 按 masterflow 完整选择：数量、颜色、内存、配件（两个）
- 提供一键方法 configure_all_and_add_to_cart(qty="2")：全部选上并加入购物车
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductDetailPage:
    QTY_INPUT = (By.ID, "number")
    SPEC_COLOR = (By.ID, "spec_value_242")
    SPEC_MEMORY = (By.ID, "spec_value_245")
    SPEC_ACC1 = (By.ID, "spec_value_243")
    SPEC_ACC2 = (By.ID, "spec_value_168")
    ADD_TO_CART = (By.XPATH, "//a[@href='javascript:addToCart(24)']")

    PRICE_LOCATORS = [
        (By.CSS_SELECTOR, ".shop_price"),
        (By.XPATH, "//*[contains(text(),'促销') or contains(text(),'价格') or contains(text(),'￥')]"),
    ]

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def assert_basic_info(self):
        price_ok = False
        for loc in self.PRICE_LOCATORS:
            try:
                el = self.driver.find_element(*loc)
                if el.is_displayed():
                    price_ok = True
                    break
            except Exception:
                continue
        assert price_ok, "未找到商品价格信息"
        return self

    def set_quantity(self, qty: str):
        el = self.wait.until(EC.presence_of_element_located(self.QTY_INPUT))
        el.clear()
        el.send_keys(qty)
        return self

    def choose_all_specs(self):
        for loc in (self.SPEC_COLOR, self.SPEC_MEMORY, self.SPEC_ACC1, self.SPEC_ACC2):
            # 保证元素可点；必要时可以滚动视口（部分模板不需要）
            try:
                self.wait.until(EC.element_to_be_clickable(loc)).click()
            except Exception:
                # 若偶发不可点，可尝试 presence + click
                el = self.wait.until(EC.presence_of_element_located(loc))
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                except Exception:
                    pass
                el.click()
        return self

    def add_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART)).click()
        from pageobjects.smoke.ShoppingCartPage import ShoppingCartPage
        return ShoppingCartPage(self.driver)

    def configure_all_and_add_to_cart(self, qty: str = "2"):
        """
        一键：数量 + 颜色 + 内存 + 配件(2个) 全部选择，并加入购物车。
        """
        self.assert_basic_info()
        self.set_quantity(qty)
        self.choose_all_specs()
        return self.add_to_cart()