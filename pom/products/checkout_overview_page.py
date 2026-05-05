import re
from enum import StrEnum

from playwright.sync_api import Page

from pom.products.products_section import ProductsSection


class PriceType(StrEnum):
    SUBTOTAL = "subtotal-label"
    TAX = "tax-label"
    TOTAL = "total-label"

class CheckOutOverviewPage(ProductsSection):
    def __init__(self, page: Page):
        super().__init__(page)

        self._subtotal_label = self._page.get_by_test_id("subtotal-label")
        self._tax_label = self._page.get_by_test_id("tax-label")
        self._total_label = self._page.get_by_test_id("total-label")

    def _get_actual_price(self, price_type: PriceType) -> float:
        price_element = {
            PriceType.SUBTOTAL: self._subtotal_label,
            PriceType.TAX: self._tax_label,
            PriceType.TOTAL: self._total_label
        }

        element = price_element.get(price_type)

        if not element:
            raise ValueError("Wrong type of price!")

        text = self._get_text_from_element(element)

        match = re.search(r"\d+[,.]?\d*", text)
        if not match:
            raise ValueError(f"Price not found in {text}")
        return float(match.group().replace(",", "."))


    def get_actual_subtotal_price(self) -> float:
        return self._get_actual_price(price_type=PriceType.SUBTOTAL)

    def get_actual_tax_price(self) -> float:
        return self._get_actual_price(price_type=PriceType.TAX)

    def get_actual_total_price(self) -> float:
        return self._get_actual_price(price_type=PriceType.TOTAL)
