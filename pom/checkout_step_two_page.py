from playwright.sync_api import Page

from pom.products_section import ProductsSection, Article


class CheckOutStepTwoPage(ProductsSection):
    def __init__(self, page: Page):
        super().__init__(page)

