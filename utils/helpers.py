import os
from pathlib import Path
import allure
from selenium.webdriver.remote.webdriver import WebDriver

SCREENSHOT_DIR = Path("tmp_screens")
SCREENSHOT_DIR.mkdir(exist_ok=True)

def take_screenshot(driver: WebDriver, name: str = "screenshot") -> str:
    path = SCREENSHOT_DIR / f"{name}.png"
    driver.save_screenshot(str(path))
    return str(path)

def attach_screenshot_to_allure(driver: WebDriver, name: str = "screenshot"):
    png = driver.get_screenshot_as_png()
    allure.attach(png, name=name, attachment_type=allure.attachment_type.PNG)
