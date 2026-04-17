from dataclasses import dataclass

from playwright.sync_api import Page

from pom.base_page import BasePage

@dataclass
class Article:
    product_name: str
    description: str
    price: float


class ProductsSection(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._primary_header = self._page.get_by_test_id("primary-header")
        self._app_logo = self._primary_header.locator(".app_logo")
        self._inventory_items = self._page.get_by_test_id("inventory-item")
        self._product_names = self._page.get_by_test_id("inventory-item-name")
        self._product_descriptions = self._page.get_by_test_id("inventory-item-desc")
        self._product_prices = self._page.get_by_test_id("inventory-item-price")
        self._basket = self._page.get_by_test_id("shopping-cart-link")

    def _get_all_prices_from_products(self) -> list[float]:
        return [
            float(price.replace("$", "")) for price in self._get_all_text_from_locators(self._product_prices)
        ]

    def _get_all_names_from_products(self) -> list[str]:
        return self._get_all_text_from_locators(self._product_names)

    def _get_price_from_product(self, product_name: str) -> float:
        index = self._get_product_index(product_name)
        price = self._get_text_from_element(self._product_prices.nth(index))
        return float(price.replace("$", ""))

    def _get_description_from_product(self, product_name: str) -> str:
        index = self._get_product_index(product_name)
        description = self._get_text_from_element(self._product_descriptions.nth(index))
        return description

    def _get_product_name(self, product_name: str) -> str:
        index = self._get_product_index(product_name)
        name = self._get_text_from_element(self._product_names.nth(index))
        return name

    def _get_product_index(self, product_name: str) -> int:
        product_names = self._get_all_texts_from_element(self._product_names)
        if product_name in product_names:
            return product_names.index(product_name)
        else:
            raise ValueError(f"Product {product_name} not found!")

    def get_product_data(self, product_name: str) -> Article:
        return Article(
            product_name= self._get_product_name(product_name),
            description = self._get_description_from_product(product_name),
            price = self._get_price_from_product(product_name),
        )