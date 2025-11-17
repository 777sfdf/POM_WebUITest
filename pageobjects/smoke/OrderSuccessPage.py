"""
OrderSuccessPage
- 断言“感谢您在本店购物”成功提示
- 提取订单号
- 可附加成功页截图
"""

import re
import allure
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OrderSuccessPage:
    SUCCESS_HINT = (By.XPATH, '//h6[contains(normalize-space(.),"感谢您在本店购物")]')

    def __init__(self, driver: WebDriver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_loaded(self):
        return self.wait.until(EC.presence_of_element_located(self.SUCCESS_HINT))

    def get_success_text(self) -> str:
        el = self.wait_loaded()
        return (el.text or "").strip()

    def assert_success(self, strict: bool = False) -> str:
        text = self.get_success_text()
        assert "感谢您在本店购物" in text, f"未检测到成功提示，实际文本: {text}"
        if strict:
            assert "您的订单已提交成功" in text and "订单号" in text, f"成功页缺少严格文案片段，实际文本: {text}"
        return text

    def extract_order_number(self, text: Optional[str] = None) -> Optional[str]:
        t = text if text is not None else self.get_success_text()
        m = re.search(r"订单号[:：]\s*([A-Za-z0-9\-]+)", t)
        if m:
            return m.group(1).strip()
        if "订单号" in t:
            parts = t.replace("：", ":").split("订单号")
            if len(parts) > 1 and ":" in parts[1]:
                return parts[1].split(":", 1)[1].strip()
        return None

    def attach_screenshot(self, name: str = "订单成功页_截图"):
        try:
            allure.attach(self.driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass