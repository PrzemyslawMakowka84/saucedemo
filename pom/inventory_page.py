from enum import StrEnum

import allure
from playwright.sync_api import Page, Locator

from pom.products_section import ProductsSection


class FilterOptions(StrEnum):
    LOW_TO_HIGH = "lohi"
    HIGH_TO_LOW = "hilo"
    A_TO_Z = "az"
    Z_TO_A = "za"


class InventoryPage(ProductsSection):
    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self._select_filter_container = self._page.get_by_test_id("product-sort-container")


    def add_article_to_basket(self, product_name: str):
        log_msg = f"Add article {product_name} to basket"
        with allure.step(log_msg):
            self._click_add_to_cart(product_name)
            self._log.info(log_msg)

    def _click_add_to_cart(self, product_name: str):
        add_to_card_locator = self._get_button_add_to_cart_locator(product_name)
        self._element_click(add_to_card_locator)

    def go_to_basket(self):
        self._element_click(self._basket)

    def _get_button_add_to_cart_locator(self, product_name: str) -> Locator:
        formated_product_name = product_name.replace(" ", "-").lower()
        return self._page.get_by_test_id(f"add-to-cart-{formated_product_name}")

    def select_filter_option(self, filter_option: FilterOptions) -> None:
        element_name = self._get_element_name(locator=self._select_filter_container)
        log_msg = f"Select filter option {filter_option.value} from {element_name}"
        with allure.step(log_msg):
            self._select_filter_container.select_option(filter_option)
            self._log.info(log_msg)

    @allure.step("Navigate to inventory page")
    def navigate(self):
        self._navigate_to_page(self.URL)

    def assert_user_logged_on_inventory_page(self, expected_title_page_text: str) -> None:
        with allure.step(f"Assert that user logged into the shop"):
            self._assert_element_should_have_text(locator=self._app_logo, expected_text=expected_title_page_text)
            self._assert_page_has_url(expected_url=self.URL)

    def get_actual_data(self, filter_option: FilterOptions) -> list[str | float]:
        actual = []
        match filter_option:
            case FilterOptions.LOW_TO_HIGH:
                actual = self._get_all_prices_from_products()
            case FilterOptions.HIGH_TO_LOW:
                actual = self._get_all_prices_from_products()
            case FilterOptions.A_TO_Z:
                actual = self._get_all_names_from_products()
            case FilterOptions.Z_TO_A:
                actual = self._get_all_names_from_products()
        return actual
