import allure
from playwright.sync_api import Page

from pom.products_section import ProductsSection, Article


class CartPage(ProductsSection):
    def __init__(self, page: Page):
        super().__init__(page)

    def _get_all_description_from_products(self) -> list[str]:
        descriptions = self._get_all_texts_from_element(self._product_descriptions)
        return descriptions

    def get_articles_from_cart(self) -> list[Article]:
        product_names = self._get_all_names_from_products()
        product_descriptions = self._get_all_description_from_products()
        product_prices = self._get_all_prices_from_products()

        return [
            Article(product_name=name, description=description, price=price)
            for name, description, price in zip(product_names, product_descriptions, product_prices)
        ]
