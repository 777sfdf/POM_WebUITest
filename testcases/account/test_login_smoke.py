from pathlib import Path
import pytest
import yaml
import allure

from pageobjects.account.LoginPage import LoginPage

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "account"


def _load_cases(yaml_file: Path):
    cases = yaml.safe_load(yaml_file.read_text(encoding="utf-8")) or []
    params = []
    for c in cases:
        marks = []
        for m in c.get("marks", []):
            mark = getattr(pytest.mark, m, None)
            if mark is not None:
                marks.append(mark)
        params.append(pytest.param(c, id=c["id"], marks=marks))
    return params

#
# @allure.feature("Account")
# @allure.story("Login")
# @pytest.mark.parametrize("case", _load_cases(DATA_DIR / "login.yaml"))
# def test_login(case, driver, base_url, config):
#     """
#     冒烟 + 回归：登录正/反向用例
#     使用 fixtures:
#       - driver: selenium webdriver
#       - base_url: 从 environment.yaml 读取
#       - config: 默认账号配置
#     """
#     allure.dynamic.title(f'{case["id"]} {case["title"]}')
#
#     page = LoginPage(driver, base_url).open()
#
#     # 输入参数兼容
#     username = case["input"].get("username") or config.get("username")
#     password = case["input"].get("password") or config.get("password")
#     remember = case["input"].get("remember", case["input"].get("remember_me", False))
#
#     with allure.step("填写并提交登录"):
#         page.login(username=username, password=password, remember=remember)
#
#     with allure.step("断言登录结果"):
#         if case["expected"].get("ok"):
#             landing = case["expected"].get("landing")
#             try:
#                 if landing:
#                     page.assert_login_success(landing)
#                 else:
#                     page.assert_login_success()
#             except TypeError:
#                 page.assert_login_success()
#         else:
#             expected_msg = case["expected"].get("message_contains", "")
#             selector = case["expected"].get("selector")
#             timeout = case["expected"].get("wait", 3)
#
#             # 先尝试 JS alert，再回退页面元素
#             alert_handled = False
#             try:
#                 page.assert_alert_contains(expected_msg, timeout=timeout)
#                 alert_handled = True
#             except Exception:
#                 # 无 alert 或 alert 文案不匹配则回退
#                 pass
#
#             if not alert_handled:
#                 page.assert_error_contains(expected_msg, selector=selector, timeout=timeout)



@allure.feature("Account")
@allure.story("Login")
@pytest.mark.parametrize("case", _load_cases(DATA_DIR / "login.yaml"))
def test_login(case, driver, base_url, config):
    """
    冒烟 + 回归：登录正/反向用例
    使用 fixtures:
      - driver: selenium webdriver
      - base_url: 从 environment.yaml 读取
      - config: 默认账号配置
    """
    allure.dynamic.title(f'{case["id"]} {case["title"]}')

    page = LoginPage(driver, base_url).open()

    # 仅当键不存在时才回退到 config；若键存在（哪怕是空字符串）就使用用例中的值
    username = case["input"]["username"] if "username" in case["input"] else config.get("username")
    password = case["input"]["password"] if "password" in case["input"] else config.get("password")
    remember = case["input"].get("remember", case["input"].get("remember_me", False))

    with allure.step("填写并提交登录"):
        page.login(username=username, password=password, remember=remember)

    with allure.step("断言登录结果"):
        if case["expected"].get("ok"):
            landing = case["expected"].get("landing")
            try:
                if landing:
                    page.assert_login_success(landing)
                else:
                    page.assert_login_success()
            except TypeError:
                page.assert_login_success()
        else:
            expected_msg = case["expected"].get("message_contains", "")
            selector = case["expected"].get("selector")
            timeout = case["expected"].get("wait", 3)

            # 先尝试 JS alert，再回退页面元素
            alert_handled = False
            try:
                page.assert_alert_contains(expected_msg, timeout=timeout)
                alert_handled = True
            except Exception:
                pass

            if not alert_handled:
                page.assert_error_contains(expected_msg, selector=selector, timeout=timeout)