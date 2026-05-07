import re
from decimal import Decimal
from enum import StrEnum

from playwright.sync_api import Page

from pom.products.products_section import ProductsSection, QUANTIZE


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
        self._finish_button = self._page.get_by_test_id("finish")
        self._back_to_product_button = self._page.get_by_test_id("back-to-products")

    def _get_actual_price(self, price_type: PriceType) -> Decimal:
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
        return Decimal(match.group().replace(",", ".")).quantize(QUANTIZE)

    def get_actual_subtotal_price(self) -> Decimal:
        return self._get_actual_price(price_type=PriceType.SUBTOTAL)

    def get_actual_tax_price(self) -> Decimal:
        return self._get_actual_price(price_type=PriceType.TAX)

    def get_actual_total_price(self) -> Decimal:
        return self._get_actual_price(price_type=PriceType.TOTAL)

    def finish_order(self):
        self._element_click(locator=self._finish_button)

    def back_to_products(self):
        self._element_click(locator=self._back_to_product_button)