# from pathlib import Path
# import pytest
# import yaml
# import allure
#
# # from pageobjects.catalog import SearchPage, ProductPage
# # from pageobjects.cart import CartPage
#
# PROJECT_ROOT = Path(__file__).resolve().parents[2]
# DATA_DIR = PROJECT_ROOT / "data" / "cart"
#
# def _load_cases(yaml_file: Path):
#     cases = yaml.safe_load(yaml_file.read_text(encoding="utf-8")) or []
#     params = []
#     for c in cases:
#         marks = [getattr(pytest.mark, m) for m in c.get("marks", [])]
#         params.append(pytest.param(c, id=c["id"], marks=marks))
#     return params
#
# @allure.feature("Cart")
# @allure.story("Add To Cart")
# @pytest.mark.smoke
# @pytest.mark.parametrize("case", _load_cases(DATA_DIR / "basic.yaml"))
# def test_add_to_cart_p0(case, driver, base_url):
#     if case["id"] != "CART-ADD-001":
#         pytest.skip("非本用例数据")
#     allure.dynamic.title(f'{case["id"]} {case["title"]}')
#     # TODO: 搜索商品 -> 进入详情 -> 加入购物车 -> 断言购物车商品数量/金额
#     # cart = CartPage(driver, base_url)
#     # before = cart.get_cart_count()
#     # cart.add(product_keyword=case["input"]["product_keyword"],
#     #          sku=case["input"]["sku"], quantity=case["input"]["quantity"])
#     # after = cart.get_cart_count()
#     # assert after - before == case["expected"]["cart_count_delta"]
#     assert True, "TODO: 实现加入购物车与断言"
#
# @allure.feature("Cart")
# @allure.story("Update Quantity")
# @pytest.mark.smoke
# @pytest.mark.parametrize("case", _load_cases(DATA_DIR / "basic.yaml"))
# def test_cart_update_quantity_p0(case, driver, base_url):
#     if case["id"] != "CART-UPDATE-002":
#         pytest.skip("非本用例数据")
#     allure.dynamic.title(f'{case["id"]} {case["title"]}')
#     # TODO: 将商品加入购物车后，修改数量为 change_to 并断言最终数量
#     # cart = CartPage(driver, base_url)
#     # cart.ensure_item(product_keyword=case["input"]["product_keyword"])
#     # cart.change_quantity(to=case["input"]["change_to"])
#     # cart.assert_quantity(case["expected"]["final_qty"])
#     assert True, "TODO: 实现数量更新与断言"