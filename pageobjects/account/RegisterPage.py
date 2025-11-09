from __future__ import annotations

import time
import re
from typing import Iterable, Optional, Tuple

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

Locator = Tuple[str, str]

class RegisterPage:
    """
    ECShop 注册页 Page Object 模版
    使用方式：
        RegisterPage(driver, base_url).open().register(...).assert_register_success()
    """

    SUCCESS_TEXTS = [
        "注册成功",
        "欢迎您成为本站会员",
        "用户中心",
        "欢迎您回来",
    ]

    ERROR_ZONES: Iterable[Locator] = (
        (By.CSS_SELECTOR, ".error, .msg, .message, .tips, .prompt"),
        (By.XPATH, "//div[contains(@class,'error') or contains(@class,'msg') or contains(@class,'message')]"),
        (By.XPATH, "//*[@id='msg' or contains(@id,'message')]"),
        (By.XPATH, "//font[contains(@color,'red') or @class='f_red']"),
    )

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 15):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, timeout)

    # 基础等待/操作
    def _wait_present(self, locator: Locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def _wait_clickable(self, locator: Locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def _try_first_present(self, locators: Iterable[Locator]):
        last_exc = None
        for loc in locators:
            try:
                return self._wait_present(loc)
            except Exception as e:
                last_exc = e
        if last_exc:
            raise last_exc

    def _type(self, locator: Locator, text: str):
        el = self._wait_present(locator)
        el.clear()
        el.send_keys(text)
        return el

    def _click(self, locator: Locator):
        el = self._wait_clickable(locator)
        el.click()
        return el

    def _attach_screenshot(self, name: str):
        try:
            allure.attach(self.driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass

    def _attach_source(self, name: str = "page-source"):
        try:
            allure.attach(self.driver.page_source, name=name, attachment_type=allure.attachment_type.TEXT)
        except Exception:
            pass

    @staticmethod
    def _with_rand(v: Optional[str]) -> Optional[str]:
        if isinstance(v, str) and "${rand}" in v:
            suffix = str(int(time.time() * 1000))[-6:]
            return v.replace("${rand}", suffix)
        return v

    # 页面行为
    @allure.step("打开注册页")
    def open(self) -> "RegisterPage":
        self.driver.get(self.base_url)
        try:
            self._click((By.LINK_TEXT, "注册"))
        except Exception:
            try:
                self._click((By.PARTIAL_LINK_TEXT, "注册"))
            except Exception:
                self.driver.get(f"{self.base_url}/user.php?act=register")
        self._try_first_present(self._locators_username())
        return self

    @allure.step("填写注册信息并提交")
    def register(self, email: str, username: str, password: str, confirm_password: str, agree: bool = True, submit: bool = True) -> "RegisterPage":
        email = self._with_rand(email) or ""
        username = self._with_rand(username) or ""
        password = password or ""
        confirm_password = confirm_password or password

        self._type(self._try_first(self._locators_username()), username)
        self._type(self._try_first(self._locators_email()), email)
        self._type(self._try_first(self._locators_password()), password)
        self._type(self._try_first(self._locators_confirm_password()), confirm_password)

        if agree:
            try:
                self._click(self._try_first(self._locators_agreement()))
            except Exception:
                pass

        if submit:
            self._click(self._try_first(self._locators_submit()))
        return self

    # 断言
    @allure.step("断言注册成功")
    def assert_register_success(self):
        def has_success_text(driver: WebDriver):
            src = driver.page_source
            return any(t in src for t in self.SUCCESS_TEXTS)
        try:
            WebDriverWait(self.driver, 10).until(has_success_text)
            hit = next((t for t in self.SUCCESS_TEXTS if t in self.driver.page_source), "")
            allure.attach(hit or "N/A", name="success-text", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            self._attach_screenshot("register-failed")
            self._attach_source()
            raise AssertionError("未检测到注册成功提示，请核对页面元素与成功文案") from e

    @allure.step("断言错误提示包含期望文案")
    def assert_error_contains(self, expected_substring: str):
        expected_substring = (expected_substring or "").strip()
        found_text = ""
        try:
            el = self._try_first_present(self.ERROR_ZONES)
            found_text = el.text.strip()
        except Exception:
            found_text = self._find_error_text_from_source(expected_substring)
        self._attach_screenshot("error-screenshot")
        self._attach_source()
        if expected_substring and expected_substring not in found_text:
            raise AssertionError(f"未匹配到错误提示。期望包含: '{expected_substring}' 实际: '{found_text}'")

    # 定位集合
    @staticmethod
    def _locators_username() -> Iterable[Locator]:
        return (
            (By.NAME, "username"),
            (By.ID, "username"),
            (By.CSS_SELECTOR, "input[name='username']"),
        )

    @staticmethod
    def _locators_email() -> Iterable[Locator]:
        return (
            (By.NAME, "email"),
            (By.ID, "email"),
            (By.CSS_SELECTOR, "input[type='email']"),
        )

    @staticmethod
    def _locators_password() -> Iterable[Locator]:
        return (
            (By.NAME, "password"),
            (By.ID, "password1"),
            (By.XPATH, "//input[@type='password' and (contains(@name,'password') or contains(@id,'password'))][1]"),
        )

    @staticmethod
    def _locators_confirm_password() -> Iterable[Locator]:
        return (
            (By.NAME, "confirm_password"),
            (By.ID, "conform_password"),
            (By.XPATH, "//input[@type='password' and (contains(@name,'confirm') or contains(@id,'confirm'))]"),
        )

    @staticmethod
    def _locators_agreement() -> Iterable[Locator]:
        return (
            (By.NAME, "agreement"),
            (By.ID, "agreement"),
            (By.XPATH, "//input[@type='checkbox' and (contains(@name,'agree') or contains(@id,'agree'))]"),
        )

    @staticmethod
    def _locators_submit() -> Iterable[Locator]:
        return (
            (By.NAME, "Submit"),
            (By.CSS_SELECTOR, "input[type='submit']"),
            (By.XPATH, "//input[@type='submit' or @name='Submit']"),
            (By.XPATH, "//input[@type='image' and contains(@src,'bnt_reg')]"),
            (By.XPATH, "//button[contains(.,'注册') or contains(.,'提交')]"),
        )

    def _try_first(self, locators: Iterable[Locator]) -> Locator:
        for loc in locators:
            try:
                self.driver.find_element(*loc)
                return loc
            except Exception:
                continue
        return next(iter(locators))

    def _find_error_text_from_source(self, expected: str) -> str:
        src = self.driver.page_source
        patterns = [
            rf"[^<>]{{0,50}}{re.escape(expected)}[^<>]{{0,50}}",
            r"(?:错误|失败|已存在|格式|不能为空)[^<>]{0,80}",
        ]
        for p in patterns:
            m = re.search(p, src)
            if m:
                return m.group(0)
        return ""