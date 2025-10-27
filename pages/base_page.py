from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Tuple

class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator: Tuple[By, str]):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator: Tuple[By, str]):
        el = self.find(locator)
        el.click()

    def send_keys(self, locator: Tuple[By, str], text: str):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator: Tuple[By, str]) -> str:
        el = self.find(locator)
        return el.text

    def is_visible(self, locator: Tuple[By, str]) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False
