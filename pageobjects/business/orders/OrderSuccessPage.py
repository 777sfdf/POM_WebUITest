"""
OrderSuccessPage 页面对象
职责：断言订单成功提示，并提取订单号。
"""

from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OrderSuccessPage:
    SUCCESS_HINT = (By.XPATH, '//h6[contains(text(),"感谢您在本店购物")]')

    def __init__(self, driver: WebDriver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def assert_success(self) -> str:
        el = self.wait.until(EC.presence_of_element_located(self.SUCCESS_HINT))
        text = (el.text or "").strip()
        assert "感谢您在本店购物" in text, f"订单成功提示缺失，实际: {text}"
        return text

    def extract_order_number(self, success_text: Optional[str] = None) -> Optional[str]:
        if success_text is None:
            success_text = self.assert_success()
        if "订单号:" in success_text:
            return success_text.split("订单号:")[-1].strip()
        return None