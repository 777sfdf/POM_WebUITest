# from pathlib import Path
# import pytest
# import yaml
# import allure
#
# # from pageobjects.checkout import CheckoutPage, PaymentPage
# # from pageobjects.cart import CartPage
#
# PROJECT_ROOT = Path(__file__).resolve().parents[2]
# DATA_DIR = PROJECT_ROOT / "data"
#
# def _load_cases(yaml_file: Path):
#     cases = yaml.safe_load(yaml_file.read_text(encoding="utf-8")) or []
#     params = []
#     for c in cases:
#         marks = [getattr(pytest.mark, m) for m in c.get("marks", [])]
#         params.append(pytest.param(c, id=c["id"], marks=marks))
#     return params
#
# @allure.feature("Checkout")
# @allure.story("Summary")
# @pytest.mark.smoke
# @pytest.mark.parametrize("case", _load_cases(DATA_DIR / "checkout" / "summary.yaml"))
# def test_checkout_summary_p0(case, driver, base_url):
#     allure.dynamic.title(f'{case["id"]} {case["title"]}')
#     # 预置：购物车中至少有1件商品（可使用 CartPage 保证前置）
#     # cart = CartPage(driver, base_url).ensure_any_item_in_cart()
#     # page = CheckoutPage(driver, base_url).open()
#     # with allure.step("选择地址/配送/支付方式"):
#     #     page.select_address(case["input"]["use_address"])
#     #     page.select_shipping(case["input"]["shipping_method"])
#     #     page.select_payment(case["input"]["payment_method"])
#     # with allure.step("断言价格汇总展示"):
#     #     page.assert_summary_loaded()
#     #     if case["expected"]["total_positive"]:
#     #         page.assert_total_positive()
#     assert True, "TODO: 实现结算页核心断言"
#
# @allure.feature("Payment")
# @allure.story("Pay Success")
# @pytest.mark.smoke
# @pytest.mark.parametrize("case", _load_cases(DATA_DIR / "payment" / "success.yaml"))
# def test_payment_success_p0(case, driver, base_url):
#     allure.dynamic.title(f'{case["id"]} {case["title"]}')
#     # 前置：提交订单到支付页
#     # checkout = CheckoutPage(driver, base_url).submit_order()
#     # pay = PaymentPage(driver, base_url)
#     # with allure.step("模拟第三方支付成功回调"):
#     #     pay.pay_success(method=case["input"]["payment_method"])
#     # with allure.step("断言订单状态为已支付"):
#     #     pay.assert_order_status(case["expected"]["order_status"])
#     assert True, "TODO: 实现支付成功与断言"