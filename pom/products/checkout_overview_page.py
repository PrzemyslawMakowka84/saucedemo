import re
from playwright.sync_api import Page

from pom.products.products_section import ProductsSection


class CheckOutOverviewPage(ProductsSection):
    def __init__(self, page: Page):
        super().__init__(page)

        self._subtotal_label = self._page.get_by_test_id("subtotal-label")

    def get_actual_subtotal_price(self) -> float:
        text = self._get_text_from_element(self._subtotal_label)
        match = re.search(r"\d+[,.]?\d*", text)
        if not match:
            raise ValueError(f"Price not found in {text}")
        return float(match.group().replace(",", "."))
