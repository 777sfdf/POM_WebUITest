"""
HomePage（首页）
能力：
1) assert_welcome_visible：断言“欢迎光临本店”（未登录态）
2) assert_search_ready：断言搜索框可用（登录/未登录通用）
3) 登录/注册入口点击（含强断言版本）
4) search_and_assert_results：执行搜索并断言出现结果
5) attach_welcome_text_screenshot：仅截“欢迎光临本店”元素近景
"""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:
    MEMBER_ZONE = (By.CSS_SELECTOR, "font#ECS_MEMBERZONE")
    WELCOME_TEXT = (By.XPATH, "//*[@id='ECS_MEMBERZONE'][contains(normalize-space(.),'欢迎光临本店')]")
    LOGIN_LINK = (By.CSS_SELECTOR, '#ECS_MEMBERZONE a[href="user.php"]')
    REGISTER_LINK = (By.CSS_SELECTOR, '#ECS_MEMBERZONE a[href="user.php?act=register"]')

    SEARCH_INPUT = (By.ID, "keyword")
    SEARCH_BUTTON = (By.NAME, "imageField")
    RESULT_LINKS = (By.XPATH, "//a[contains(@href, 'goods.php?id=')]")

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, timeout)
        self._welcome_element = None

    def open(self):
        self.driver.get(self.base_url)
        return self

    # 未登录态专用：“欢迎光临本店”
    def assert_welcome_visible(self):
        self.wait.until(EC.presence_of_element_located(self.MEMBER_ZONE))
        el = self.wait.until(EC.presence_of_element_located(self.WELCOME_TEXT))
        text = (el.text or "").strip()
        assert "欢迎光临本店" in text, f"首页未检测到欢迎文案，实际文本: {text}"
        self._welcome_element = el
        return self

    # 登录/未登录通用：断言搜索框可用
    def assert_search_ready(self):
        el = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
        assert el.is_displayed(), "搜索输入框不可见"
        return self

    def get_welcome_element(self):
        return self._welcome_element

    def attach_welcome_text_screenshot(self, name: str = "欢迎光临本店_元素截图"):
        el = self._welcome_element
        if el is None:
            self.assert_welcome_visible()
            el = self._welcome_element
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            pass
        try:
            png = el.screenshot_as_png
            allure.attach(png, name=name, attachment_type=allure.attachment_type.PNG)
        except Exception:
            try:
                allure.attach(self.driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)
            except Exception:
                pass

    def go_to_login(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_LINK)).click()
        return self

    def go_to_register(self):
        self.wait.until(EC.element_to_be_clickable(self.REGISTER_LINK)).click()
        return self

    def click_login_and_assert_navigated(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_LINK)).click()
        assert "user.php" in self.driver.current_url, f"未跳转到登录页，当前URL: {self.driver.current_url}"
        return self

    def click_register_and_assert_navigated(self):
        self.wait.until(EC.element_to_be_clickable(self.REGISTER_LINK)).click()
        assert "user.php" in self.driver.current_url and "act=register" in self.driver.current_url, \
            f"未跳转到注册页，当前URL: {self.driver.current_url}"
        return self

    def search_and_assert_results(self, keyword: str):
        inp = self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUT))
        inp.clear()
        inp.send_keys(keyword)
        try:
            self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON)).click()
        except Exception:
            inp.send_keys(Keys.ENTER)
        # 等待出现至少一个结果链接
        self.wait.until(lambda d: len(d.find_elements(*self.RESULT_LINKS)) > 0)
        elems = self.driver.find_elements(*self.RESULT_LINKS)  # 返回新鲜列表以减少 stale 风险
        assert len(elems) > 0, "搜索后未发现商品结果链接"
        return elems