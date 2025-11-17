"""
SearchResultsPage
职责：
- 列出搜索结果
- 判断是否有结果
- 打开第一条结果 -> 返回 ProductDetailPage
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
        out: List[Dict] = []
        for el in elems:
            title = (el.text or "").strip()
            href = el.get_attribute("href") or ""
            out.append({"title": title, "link": href, "element": el})
        return out

    def has_any(self) -> bool:
        return len(self.list_results()) > 0

    def open_first(self):
        elems = self.driver.find_elements(*self.RESULT_LINKS)
        assert elems, "搜索结果为空，无法打开商品详情"
        elems[0].click()
        from pageobjects.smoke.ProductDetailPage import ProductDetailPage
        return ProductDetailPage(self.driver)