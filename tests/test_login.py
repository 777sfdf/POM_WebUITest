import pytest
from pages.login_page import LoginPage
from pages.secure_page import SecurePage
import allure

@allure.feature("Login")
@allure.story("Valid login")
@pytest.mark.ui
def test_valid_login(driver, config):
    lp = LoginPage(driver)
    sp = SecurePage(driver)
    base_url = config.get("base_url")
    user = config["credentials"]["username"]
    pwd = config["credentials"]["password"]

    with allure.step("Open login page"):
        lp.go_to_login(base_url)

    with allure.step("Perform login"):
        lp.login(user, pwd)

    with allure.step("Verify secure page is displayed"):
        assert sp.is_logout_visible(), "Logout button should be visible after login"
        header = sp.get_header_text()
        assert "Secure Area" in header
