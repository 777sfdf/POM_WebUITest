"""
SearchResultsPage 页面对象
职责：封装搜索结果相关操作（判断是否有结果、打开第一个商品）。
"""

from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class SearchResultsPage:
    RESULT_LINKS = (By.XPATH, "//a[contains(@href, 'goods.php?id=')]")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def list_results(self) -> List[Dict]:
        elems = self.driver.find_elements(*self.RESULT_LINKS)
        results = []
        for el in elems:
            title = (el.text or "").strip()
            href = el.get_attribute("href") or ""
            results.append({"title": title, "link": href, "element": el})
        return results

    def has_any(self) -> bool:
        return len(self.list_results()) > 0

    def open_first(self):
        elems = self.driver.find_elements(*self.RESULT_LINKS)
        if not elems:
            raise AssertionError("搜索结果为空，无法打开第一个商品。")
        elems[0].click()
        from pageobjects.business.product.ProductPage import ProductPage
        return ProductPage(self.driver)