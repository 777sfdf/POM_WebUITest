from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, self.timeout)

    def find(self, by, locator):
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def click(self, by, locator):
        el = self.find(by, locator)
        el.click()
        return el

    def send_keys(self, by, locator, keys):
        el = self.find(by, locator)
        el.clear()
        el.send_keys(keys)
        return el

    def get_text(self, by, locator):
        el = self.find(by, locator)
        return el.text

    def open(self, url):
        self.driver.get(url)