from playwright.sync_api import Page

from pom.products_section import ProductsSection


class CartPage(ProductsSection):
    def __init__(self, page: Page):
        super().__init__(page)
        self._checkout_button = self._page.get_by_test_id("checkout")

    def goto_checkout(self):
        self._element_click(self._checkout_button)
