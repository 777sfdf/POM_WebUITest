from __future__ import annotations

import re
from typing import Iterable, Tuple, Optional

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

Locator = Tuple[str, str]


class LoginPage:
    """
    ECShop 登录页 Page Object

    方法:
      - open(): 打开首页并进入登录入口（点击登录图片或直接访问 /user.php?act=login）
      - login(username, password, remember=False): 填写并提交登录表单
      - logout(): 如果存在退出链接则点击退出
      - assert_login_success(landing=None): 断言登录成功（检查常见欢迎文案，可选校验 landing 路径）
      - assert_error_contains(expected_substring, selector=None, timeout=5): 断言错误提示包含期望文案（可传自定义定位器）
    """

    SUCCESS_TEXTS = [
        "欢迎您回来",
        "欢迎您",
        "用户中心",
        "退出",
    ]

    ERROR_ZONES: Iterable[Locator] = (
        (By.CSS_SELECTOR, ".error, .msg, .message, .tips, .prompt"),
        (By.XPATH, "//div[contains(@class,'error') or contains(@class,'msg') or contains(@class,'message')]"),
        (By.XPATH, "//font[contains(@color,'red') or @class='f_red']"),
    )

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 15):
        self.driver = driver
        self.base_url = base_url.rstrip("/") if base_url else ""
        self.wait = WebDriverWait(driver, timeout)

    # ---------- 基础工具 ----------
    def _wait_present(self, locator: Locator, timeout: Optional[int] = None):
        w = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return w.until(EC.presence_of_element_located(locator))

    def _wait_clickable(self, locator: Locator, timeout: Optional[int] = None):
        w = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return w.until(EC.element_to_be_clickable(locator))

    def _try_first_present(self, locators: Iterable[Locator], timeout: Optional[int] = None):
        last_exc = None
        for loc in locators:
            try:
                return self._wait_present(loc, timeout=timeout)
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

    def _attach_screenshot(self, name: str = "screenshot"):
        try:
            allure.attach(self.driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass

    def _attach_source(self, name: str = "page-source"):
        try:
            allure.attach(self.driver.page_source, name=name, attachment_type=allure.attachment_type.TEXT)
        except Exception:
            pass

    # ---------- 页面行为 ----------
    @allure.step("打开登录入口")
    def open(self) -> "LoginPage":
        self.driver.get(self.base_url)
        try:
            img_locator = (By.CSS_SELECTOR, 'img[src="themes/default/images/bnt_log.gif"]')
            img = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(img_locator))
            a = img.find_element(By.XPATH, "./parent::a")
            a.click()
        except Exception:
            self.driver.get(f"{self.base_url}/user.php?act=login")

        self._try_first_present(self._locators_username())
        return self

    @allure.step("填写并提交登录表单")
    def login(self, username: str, password: str, remember: bool = False) -> "LoginPage":
        username = username or ""
        password = password or ""
        self._type(self._try_first(self._locators_username()), username)
        self._type(self._try_first(self._locators_password()), password)

        if remember:
            try:
                self._click(self._try_first(self._locators_remember()))
            except Exception:
                pass

        self._click(self._try_first(self._locators_submit()))
        return self

    @allure.step("退出登录（若存在）")
    def logout(self):
        locators = [
            (By.LINK_TEXT, "退出"),
            (By.PARTIAL_LINK_TEXT, "退出"),
            (By.LINK_TEXT, "Logout"),
            (By.PARTIAL_LINK_TEXT, "Logout"),
        ]
        for loc in locators:
            try:
                el = self._wait_clickable(loc, timeout=5)
                el.click()
                return
            except Exception:
                continue

    # ---------- 断言 ----------
    @allure.step("断言登录成功")
    def assert_login_success(self, landing: Optional[str] = None):
        def has_success(driver):
            src = driver.page_source or ""
            return any(t in src for t in self.SUCCESS_TEXTS)

        try:
            WebDriverWait(self.driver, 10).until(has_success)
            hit = next((t for t in self.SUCCESS_TEXTS if t in self.driver.page_source), "")
            allure.attach(hit or "N/A", name="login-success-hit", attachment_type=allure.attachment_type.TEXT)
            if landing:
                # landing 可以是路径片段或完整 URL
                current = self.driver.current_url
                ok_url = (landing in current) or current.endswith(landing.lstrip("/"))
                allure.attach(current, name="current-url", attachment_type=allure.attachment_type.TEXT)
                if not ok_url:
                    raise AssertionError(f"登录后未到达期望页面: {landing} 当前: {current}")
        except Exception as e:
            self._attach_screenshot("login-failed")
            self._attach_source()
            raise AssertionError("未检测到登录成功的页面文案，请检查页面或定位器是否正确") from e

    @allure.step("断言错误提示包含期望文案")
    def assert_error_contains(
        self,
        expected_substring: str,
        selector: Optional[str] = None,
        timeout: int = 5
    ):
        expected_substring = (expected_substring or "").strip()
        found_text = ""

        # 优先使用自定义 selector
        if selector:
            try:
                loc = self._parse_selector(selector)
                el = self._wait_present(loc, timeout=timeout)
                found_text = el.text.strip()
            except Exception:
                # 进入回退逻辑
                pass

        # 如果没获取到文本，则尝试 ERROR_ZONES
        if not found_text:
            try:
                el = self._try_first_present(self.ERROR_ZONES, timeout=timeout)
                found_text = el.text.strip()
            except Exception:
                # 最后从源码里做正则近似匹配
                found_text = self._find_error_text_from_source(expected_substring)

        self._attach_screenshot("login-error-screenshot")
        self._attach_source()
        allure.attach(found_text or "EMPTY", name="login-error-text", attachment_type=allure.attachment_type.TEXT)

        if expected_substring and expected_substring not in found_text:
            raise AssertionError(
                f"未匹配到错误提示。期望包含: '{expected_substring}' 实际: '{found_text}'"
            )

    # ---------- 定位集合 ----------
    @staticmethod
    def _locators_username() -> Iterable[Locator]:
        return (
            (By.NAME, "username"),
            (By.XPATH, "//input[@name='username']"),
            (By.ID, "username"),
            (By.CSS_SELECTOR, "input[name='username']"),
        )

    @staticmethod
    def _locators_password() -> Iterable[Locator]:
        return (
            (By.NAME, "password"),
            (By.XPATH, "//input[@name='password']"),
            (By.ID, "password"),
            (By.CSS_SELECTOR, "input[type='password']"),
        )

    @staticmethod
    def _locators_remember() -> Iterable[Locator]:
        return (
            (By.NAME, "remember"),
            (By.XPATH, "//input[@type='checkbox' and (contains(@name,'remember') or contains(@id,'remember'))]"),
        )

    @staticmethod
    def _locators_submit() -> Iterable[Locator]:
        return (
            (By.NAME, "submit"),
            (By.CSS_SELECTOR, "input[type='submit']"),
            (By.XPATH, "//input[@name='submit']"),
            (By.XPATH, "//button[contains(.,'登录') or contains(.,'立刻登录') or contains(.,'立即登入') or contains(.,'立即登录')]"),
        )

    # ---------- 私有辅助 ----------
    def _try_first(self, locators: Iterable[Locator]) -> Locator:
        for loc in locators:
            try:
                self.driver.find_element(*loc)
                return loc
            except Exception:
                continue
        return next(iter(locators))

    def _find_error_text_from_source(self, expected: str) -> str:
        src = self.driver.page_source or ""
        patterns = [
            rf"[^<>]{{0,50}}{re.escape(expected)}[^<>]{{0,50}}",
            r"(?:错误|失败|密码|账号|不存在|为空)[^<>]{0,80}",
        ]
        for p in patterns:
            m = re.search(p, src)
            if m:
                return m.group(0).strip()
        return ""

    def _parse_selector(self, selector: str) -> Locator:
        """
        支持格式:
          - xpath=...
          - css=...
          - id=...
          - name=...
          - link= (完全匹配链接文字)
          - partial_link=
        若无法识别前缀，默认按 XPath 处理（如果以 // 开头），否则按 CSS。
        """
        selector = selector.strip()
        lowered = selector.lower()
        if lowered.startswith("xpath="):
            return By.XPATH, selector[len("xpath="):]
        if lowered.startswith("css="):
            return By.CSS_SELECTOR, selector[len("css="):]
        if lowered.startswith("id="):
            return By.ID, selector[len("id="):]
        if lowered.startswith("name="):
            return By.NAME, selector[len("name="):]
        if lowered.startswith("link="):
            return By.LINK_TEXT, selector[len("link="):]
        if lowered.startswith("partial_link="):
            return By.PARTIAL_LINK_TEXT, selector[len("partial_link="):]

        # 自动推断
        if selector.startswith("//"):
            return By.XPATH, selector
        return By.CSS_SELECTOR, selector