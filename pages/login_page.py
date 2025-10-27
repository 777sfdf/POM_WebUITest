from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.CSS_SELECTOR, "button.radius")
    FLASH = (By.ID, "flash")

    def go_to_login(self, base_url: str):
        self.driver.get(base_url + "/login")

    def login(self, username: str, password: str):
        self.send_keys(self.USERNAME, username)
        self.send_keys(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def get_flash_message(self) -> str:
        return self.get_text(self.FLASH)
