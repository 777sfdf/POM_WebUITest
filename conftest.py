# # conftest.py (只展示 browser fixture 相关部分)
# import os
# import pytest
# import allure
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from common.config_utils import ConfigUtils
# from common.logger import log
# from common.screenshot import take_screenshot
#
# def pytest_addoption(parser):
#     parser.addoption("--env", action="store", default="dev", help="test environment")
#     parser.addoption("--browser", action="store", default="chrome", help="browser: chrome or firefox")
#     parser.addoption("--headless", action="store_true", help="run in headless mode")
#     parser.addoption("--use-local-driver", action="store_true", help="use driver from ./drivers folder if present")
#
# @pytest.fixture(scope="session")
# def config(request):
#     env = request.config.getoption("--env")
#     cfg = ConfigUtils()
#     env_config = cfg.get_environment(env)
#     log.info(f"Loaded environment config for: {env}")
#     return env_config
#
# @pytest.fixture(scope="session")
# def browser(request, config):
#     browser_name = request.config.getoption("--browser").lower()
#     headless = request.config.getoption("--headless")
#     # 优先使用项目 drivers 下的 chromedriver.exe（如果存在），不再需要额外参数
#     project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
#
#     # project_root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     print(f"driver路径如下: {project_root}")
#     print('-' * 50)
#     print(project_root)
#     local_driver_path = os.path.join(project_root, "drivers", "chromedriver.exe")
#
#     options = Options()
#     if headless:
#         options.add_argument("--headless=new")
#     options.add_argument("--window-size=1920,1080")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#
#     driver_path_to_use = None
#     if os.path.isfile(local_driver_path):
#         log.info(f"Using project local chromedriver at: {local_driver_path}")
#         driver_path_to_use = local_driver_path
#     else:
#         # 回退到 webdriver_manager（并对返回结果做简单校验）
#         log.info("Local chromedriver not found, using webdriver_manager")
#         driver_bin = ChromeDriverManager().install()
#         log.info(f"webdriver_manager returned: {driver_bin}")
#         if os.path.isfile(driver_bin):
#             driver_path_to_use = driver_bin
#         else:
#             # 尝试在 webdriver_manager 缓存目录查找实际的可执行chromedriver
#             wdm_root = os.path.expanduser("~/.wdm")
#             found = None
#             for root, dirs, files in os.walk(wdm_root):
#                 for f in files:
#                     if f.lower().startswith("chromedriver"):
#                         cand = os.path.join(root, f)
#                         if os.path.isfile(cand):
#                             found = cand
#                             break
#                 if found:
#                     break
#             driver_path_to_use = found
#
#     if not driver_path_to_use or not os.path.isfile(driver_path_to_use):
#         log.error(f"No valid chromedriver executable found. Tried local: {local_driver_path}. Candidate: {driver_path_to_use}")
#         raise FileNotFoundError("chromedriver executable not found or is not a valid Windows executable. See logs for scanned paths.")
#
#     log.info(f"Final chromedriver executable: {driver_path_to_use}")
#     # 这里创建了 webdriver 实例
#     service = ChromeService(executable_path=driver_path_to_use)
#     driver = webdriver.Chrome(service=service, options=options)
#     driver.implicitly_wait(5)
#     try:
#         driver.maximize_window()
#     except Exception:
#         pass
#
#     yield driver
#     driver.quit()

#
# import os
# import pytest
# import allure
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from common.config_utils import ConfigUtils
# from common.logger import log
# from common.screenshot import take_screenshot
#
# def pytest_addoption(parser):
#     parser.addoption("--env", action="store", default="dev", help="test environment")
#     parser.addoption("--browser", action="store", default="chrome", help="browser: chrome or firefox")
#     parser.addoption("--headless", action="store_true", help="run in headless mode")
#     parser.addoption("--use-local-driver", action="store_true", help="use driver from ./drivers folder if present")
#
# @pytest.fixture(scope="session")
# def config(request):
#     env = request.config.getoption("--env")
#     cfg = ConfigUtils()
#     env_config = cfg.get_environment(env)
#     log.info(f"Loaded environment config for: {env}")
#     return env_config
#
# @pytest.fixture(scope="session")
# def browser(request, config):
#     browser_name = request.config.getoption("--browser").lower()
#     headless = request.config.getoption("--headless")
#
#     # 项目根目录（conftest 位于项目根）
#     project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
#     local_driver_path = os.path.join(project_root, "drivers", "chromedriver.exe")
#
#     options = Options()
#     if headless:
#         options.add_argument("--headless=new")
#     options.add_argument("--window-size=1920,1080")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#
#     # 优先使用项目 drivers 下的固定版本
#     driver_path_to_use = None
#     if os.path.isfile(local_driver_path):
#         log.info(f"Using project local chromedriver at: {local_driver_path}")
#         driver_path_to_use = local_driver_path
#     else:
#         log.info("Local chromedriver not found, using webdriver_manager")
#         driver_bin = ChromeDriverManager().install()
#         log.info(f"webdriver_manager returned: {driver_bin}")
#         if os.path.isfile(driver_bin):
#             driver_path_to_use = driver_bin
#         else:
#             # 尝试在 webdriver_manager 缓存目录查找
#             wdm_root = os.path.expanduser("~/.wdm")
#             found = None
#             for root, dirs, files in os.walk(wdm_root):
#                 for f in files:
#                     if f.lower().startswith("chromedriver"):
#                         cand = os.path.join(root, f)
#                         if os.path.isfile(cand):
#                             found = cand
#                             break
#                 if found:
#                     break
#             driver_path_to_use = found
#
#     if not driver_path_to_use or not os.path.isfile(driver_path_to_use):
#         log.error(f"No valid chromedriver executable found. Tried local: {local_driver_path}. Candidate: {driver_path_to_use}")
#         raise FileNotFoundError("chromedriver executable not found or is not a valid Windows executable. See logs for scanned paths.")
#
#     log.info(f"Final chromedriver executable: {driver_path_to_use}")
#     service = ChromeService(executable_path=driver_path_to_use)
#     driver = webdriver.Chrome(service=service, options=options)
#     driver.implicitly_wait(5)
#     try:
#         driver.maximize_window()
#     except Exception:
#         pass
#
#     yield driver
#     driver.quit()
#
# # 新增：别名 fixture，测试里可直接使用 driver（等同于 browser）
# @pytest.fixture(scope="session")
# def driver(browser):
#     yield browser
#
# # 新增：base_url fixture，从 config/environment.yaml 读取
# @pytest.fixture(scope="session")
# def base_url(config):
#     url = config.get("base_url") or config.get("url")
#     if not url:
#         raise RuntimeError("base_url not found in environment config (config/environment.yaml).")
#     return url.rstrip("/")
#
#


import os
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from common.config_utils import ConfigUtils
from common.logger import log
from common.screenshot import take_screenshot
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

    # 项目根目录（conftest 位于项目根）
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
    local_driver_path = os.path.join(project_root, "drivers", "chromedriver.exe")

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # 优先使用项目 drivers 下的固定版本
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
            # 尝试在 webdriver_manager 缓存目录查找
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


# 新增：别名 fixture，测试里可直接使用 driver（等同于 browser）
@pytest.fixture(scope="session")
def driver(browser):
    yield browser


# 新增：base_url fixture，从 config/environment.yaml 读取
@pytest.fixture(scope="session")
def base_url(config):
    url = config.get("base_url") or config.get("url")
    if not url:
        raise RuntimeError("base_url not found in environment config (config/environment.yaml).")
    return url.rstrip("/")


# 新增：每个用例后自动清理状态，满足“退出登录 + 清 Cookie/Storage + 回首页 + 刷新”
@pytest.fixture(autouse=True, scope="function")
def _reset_state_after_each_test(driver, base_url):
    """
    每个测试用例结束后：
      1) 关闭可能遗留的 alert（避免阻塞后续操作）
      2) 若可见则点击退出登录
      3) 清理 localStorage / sessionStorage
      4) 清理 Cookie
      5) 回到首页并刷新，确保下个用例是未登录状态
    """
    yield

    # 1) 关闭遗留 alert
    try:
        alert = WebDriverWait(driver, 1).until(EC.alert_is_present())
        _ = alert.text  # 可记录
        alert.accept()
    except Exception:
        pass

    # 2) 退出登录：使用已有的 LoginPage.logout()
    try:
        from pageobjects.account.LoginPage import LoginPage
        LoginPage(driver, base_url).logout()
    except Exception:
        pass

    # 3) 清理 Storage
    try:
        driver.execute_script("window.localStorage && window.localStorage.clear();")
        driver.execute_script("window.sessionStorage && window.sessionStorage.clear();")
    except Exception:
        pass

    # 4) 清理 Cookie
    try:
        driver.delete_all_cookies()
    except Exception:
        pass

    # 5) 回首页并刷新
    try:
        driver.get(base_url)
    except Exception:
        pass
    try:
        driver.refresh()
    except Exception:
        pass