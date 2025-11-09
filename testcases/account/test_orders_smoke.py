# from pathlib import Path
# import pytest
# import yaml
# import allure
#
# # from pageobjects.account import OrdersPage
#
# PROJECT_ROOT = Path(__file__).resolve().parents[2]
# DATA_DIR = PROJECT_ROOT / "data" / "account"
#
# def _load_cases(yaml_file: Path):
#     cases = yaml.safe_load(yaml_file.read_text(encoding="utf-8")) or []
#     params = []
#     for c in cases:
#         marks = [getattr(pytest.mark, m) for m in c.get("marks", [])]
#         params.append(pytest.param(c, id=c["id"], marks=marks))
#     return params
#
# @allure.feature("Orders")
# @allure.story("List")
# @pytest.mark.smoke
# @pytest.mark.parametrize("case", _load_cases(DATA_DIR / "orders.yaml"))
# def test_orders_list_p0(case, driver, base_url):
#     allure.dynamic.title(f'{case["id"]} {case["title"]}')
#     # TODO: 登录后访问订单列表，断言最近订单可见
#     # page = OrdersPage(driver, base_url).open()
#     # page.assert_latest_order_visible()
#     assert True, "TODO: 实现订单列表断言"