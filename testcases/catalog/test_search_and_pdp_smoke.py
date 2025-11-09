# from pathlib import Path
# import pytest
# import yaml
# import allure
#
# # from pageobjects.home import HomePage
# # from pageobjects.catalog import SearchPage, ProductPage
#
# PROJECT_ROOT = Path(__file__).resolve().parents[2]
# DATA_DIR = PROJECT_ROOT / "data" / "catalog"
#
# def _load_cases(yaml_file: Path):
#     cases = yaml.safe_load(yaml_file.read_text(encoding="utf-8")) or []
#     params = []
#     for c in cases:
#         marks = [getattr(pytest.mark, m) for m in c.get("marks", [])]
#         params.append(pytest.param(c, id=c["id"], marks=marks))
#     return params
#
# @allure.feature("Catalog")
# @allure.story("Search")
# @pytest.mark.smoke
# @pytest.mark.parametrize("case", _load_cases(DATA_DIR / "search.yaml"))
# def test_search_p0(case, driver, base_url):
#     allure.dynamic.title(f'{case["id"]} {case["title"]}')
#     # TODO: 使用 SearchPage 实现搜索并断言结果数量 >= expected_min_results
#     # page = SearchPage(driver, base_url).open()
#     # results = page.search(keyword=case["input"]["keyword"], category=case["input"]["category"])
#     # assert len(results) >= case["input"]["expected_min_results"]
#     assert True, "TODO: 实现搜索与断言"
#
# @allure.feature("Catalog")
# @allure.story("Product Detail")
# @pytest.mark.smoke
# @pytest.mark.parametrize("case", _load_cases(DATA_DIR / "product_basic.yaml"))
# def test_product_detail_p0(case, driver, base_url):
#     allure.dynamic.title(f'{case["id"]} {case["title"]}')
#     # TODO: 搜索进入第一个商品详情，断言名称/价格/库存展示
#     # p = ProductPage(driver, base_url).open_by_search(case["input"]["product_keyword"])
#     # p.assert_basic_info(name_contains=case["expected"]["name_contains"],
#     #                     price_min=case["expected"]["price_min"],
#     #                     in_stock=case["expected"]["in_stock"])
#     assert True, "TODO: 实现商品详情断言"