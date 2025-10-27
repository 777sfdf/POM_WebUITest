from selenium.webdriver.common.by import By
from .base_page import BasePage

class SecurePage(BasePage):
    LOGOUT_BTN = (By.CSS_SELECTOR, "a.button")
    HEADER = (By.TAG_NAME, "h2")

    def is_logout_visible(self) -> bool:
        return self.is_visible(self.LOGOUT_BTN)

    def get_header_text(self) -> str:
        return self.get_text(self.HEADER)
