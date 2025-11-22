import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from common.config_utils import ConfigUtils
from common.logger import log
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", help="test environment")
    parser.addoption("--browser", action="store", default="chrome", help="browser: chrome or firefox")
    parser.addoption("--headless", action="store_true", help="run in headless mode")
    parser.addoption("--use-local-driver", action="store_true", help="use driver from ./drivers folder if present")

@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")
    cfg = ConfigUtils()
    env_config = cfg.get_environment(env)
    log.info(f"Loaded environment config for: {env}")
    return env_config

@pytest.fixture(scope="session")
def browser(request, config):
    browser_name = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
    local_driver_path = os.path.join(project_root, "drivers", "chromedriver.exe")

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver_path_to_use = None
    if os.path.isfile(local_driver_path):
        log.info(f"Using project local chromedriver at: {local_driver_path}")
        driver_path_to_use = local_driver_path
    else:
        log.info("Local chromedriver not found, using webdriver_manager")
        driver_bin = ChromeDriverManager().install()
        log.info(f"webdriver_manager returned: {driver_bin}")
        if os.path.isfile(driver_bin):
            driver_path_to_use = driver_bin
        else:
            wdm_root = os.path.expanduser("~/.wdm")
            found = None
            for root, dirs, files in os.walk(wdm_root):
                for f in files:
                    if f.lower().startswith("chromedriver"):
                        cand = os.path.join(root, f)
                        if os.path.isfile(cand):
                            found = cand
                            break
                if found:
                    break
            driver_path_to_use = found

    if not driver_path_to_use or not os.path.isfile(driver_path_to_use):
        log.error(f"No valid chromedriver executable found. Tried local: {local_driver_path}. Candidate: {driver_path_to_use}")
        raise FileNotFoundError("chromedriver executable not found or is not a valid Windows executable. See logs for scanned paths.")

    log.info(f"Final chromedriver executable: {driver_path_to_use}")
    service = ChromeService(executable_path=driver_path_to_use)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    try:
        driver.maximize_window()
    except Exception:
        pass

    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def driver(browser):
    yield browser

@pytest.fixture(scope="session")
def base_url(config):
    url = config.get("base_url") or config.get("url")
    if not url:
        raise RuntimeError("base_url not found in environment config (config/environment.yaml).")
    return url.rstrip("/")

# --------- 状态清理与登出工具 ---------
def _try_logout(driver, timeout: int = 2):
    from selenium.webdriver.common.by import By
    candidates = [
        (By.CSS_SELECTOR, '#ECS_MEMBERZONE a[href*="user.php?act=logout"]'),
        (By.XPATH, "//a[contains(@href,'user.php') and contains(@href,'act=logout')]"),
        (By.LINK_TEXT, "退出"),
        (By.PARTIAL_LINK_TEXT, "退出"),
    ]
    try:
        for by, sel in candidates:
            els = driver.find_elements(by, sel)
            for el in els:
                try:
                    if el.is_displayed():
                        el.click()
                        try:
                            WebDriverWait(driver, 1).until(EC.alert_is_present()).accept()
                        except Exception:
                            pass
                        return True
                except Exception:
                    continue
    except Exception:
        pass
    return False

def _ensure_clean_state(driver, base_url):
    """退出（若已登录）+ 清 Cookie + 回到首页并刷新"""
    try:
        _try_logout(driver)
    except Exception:
        pass
    try:
        driver.delete_all_cookies()
    except Exception:
        pass
    try:
        driver.get(base_url)
        driver.refresh()
    except Exception:
        pass

# --------- 全局 autouse 清理：默认每条用例结束清场；带 session_login 标记的模块内跳过 ---------
@pytest.fixture(autouse=True, scope="function")
def _reset_state_after_each_test(request, driver, base_url):
    """
    默认每条测试用例结束后：
      1) 退出登录（若已登录）
      2) 清理 Cookie
      3) 回到首页并刷新
    但若用例（或其上层模块）带有 @pytest.mark.session_login，则跳过（该模块内复用登录态）。
    """
    yield
    if request.node.get_closest_marker("session_login"):
        return
    _ensure_clean_state(driver, base_url)

# --------- 登录后业务链路：模块级复用登录态 ---------
from pageobjects.smoke.HomePage import HomePage
@pytest.fixture(scope="module")
def session_logged_in(driver, base_url, config):
    """
    登录后链路模块使用：
      - 模块开始前，清场一次；UI 登录一次
      - 模块内各用例复用同一登录会话
      - 模块结束统一登出清理
    """
    from pageobjects.smoke.LoginPage import LoginPage
    username = config.get("username") or os.environ.get("TEST_USER")
    password = config.get("password") or os.environ.get("TEST_PASS")
    if not username or not password:
        raise RuntimeError("未找到登录凭据，请在配置或环境变量 TEST_USER/TEST_PASS 中提供。")

    # 模块开始前清场
    _ensure_clean_state(driver, base_url)

    # 登录一次
    HomePage(driver, base_url).open().assert_welcome_visible().go_to_login()
    LoginPage(driver, base_url).login(username, password).assert_login_success()

    yield

    # 模块结束清场
    _ensure_clean_state(driver, base_url)