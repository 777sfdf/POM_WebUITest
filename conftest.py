import pytest
from utils.yaml_utils import load_yaml
from utils.logger import get_logger
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import allure
from utils.helpers import attach_screenshot_to_allure

logger = get_logger(__name__)

CONFIG_PATH = Path("config") / "config.yaml"

@pytest.fixture(scope="session")
def config():
    cfg = load_yaml(str(CONFIG_PATH))
    logger.info("Loaded config from %s", CONFIG_PATH)
    return cfg

@pytest.fixture
def driver(config, request):
    browser = config.get("browser", "chrome").lower()
    headless = config.get("headless", False)
    implicit_wait = config.get("implicit_wait", 5)

    if browser == "chrome":
        options = Options()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        service = Service(ChromeDriverManager().install())
        _driver = webdriver.Chrome(service=service, options=options)
    else:
        raise ValueError(f"Browser {browser} not supported in demo")

    _driver.implicitly_wait(implicit_wait)
    logger.info("Started browser: %s (headless=%s)", browser, headless)
    yield _driver
    logger.info("Quitting browser...")
    _driver.quit()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        try:
            drv = item.funcargs.get("driver")
            if drv:
                attach_screenshot_to_allure(drv, name=f"{item.name}_failure")
        except Exception as e:
            logger.exception("Failed to attach screenshot: %s", e)

@pytest.fixture(autouse=True)
def add_base_url_to_allure(config):
    allure.dynamic.label("base_url", config.get("base_url"))
    yield
