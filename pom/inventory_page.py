from enum import StrEnum

import allure
from playwright.sync_api import Page, Locator

from pom.base_page import BasePage


class FilterOptions(StrEnum):
    LOW_TO_HIGH = "lohi"
    HIGH_TO_LOW = "hilo"
    A_TO_Z = "az"
    Z_TO_A = "za"

class InventoryPage(BasePage):
    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self._page = page
        self._primary_header = page.get_by_test_id("primary-header")
        self._app_logo = self._primary_header.locator(".app_logo")
        self._product_prices = page.get_by_test_id("inventory-item-price")
        self._product_names = page.get_by_test_id("inventory-item-name")
        self._select_filter_container = page.get_by_test_id("product-sort-container")

    def get_all_prices_from_products(self) -> list[float]:
        prices = self._get_all_text_from_locators(self._product_prices)
        prices_float = [float(price.replace("$", "")) for price in prices]
        return prices_float

    def get_all_names_from_products(self) -> list[str]:
        products = self._get_all_text_from_locators(self._product_names)
        return products

    def _get_all_text_from_locators(self, locator: Locator) -> list[str]:
        locator_count = locator.count()
        texts = []
        for i in range(locator_count):
            texts.append(self.get_text_from_element(locator.nth(i)))

        return texts

    def select_filter_option(self, filter_option: FilterOptions) -> None:
        log_msg = f"Select filter option {filter_option.value}"
        with allure.step(log_msg):
            self._select_filter_container.select_option(filter_option)
            self.log.info(log_msg)

    def assert_user_logged_on_inventory_page(self, expected_title_page_text: str) -> None:
        with allure.step(f"Assert that user logged into the shop"):
            self.assert_element_should_have_text(locator=self._app_logo, expected_text=expected_title_page_text)
            self.assert_page_has_url(expected_url=self.URL)

    def assert_sorting(self, filter_option: FilterOptions) -> None:
        with allure.step(f"Assert item sorting for filter option: {filter_option.value}"):
            match filter_option:
                case FilterOptions.LOW_TO_HIGH:
                    actual = self.get_all_prices_from_products()
                    expected = sorted(actual)
                case FilterOptions.HIGH_TO_LOW:
                    actual = self.get_all_prices_from_products()
                    expected = sorted(actual, reverse=True)
                case FilterOptions.A_TO_Z:
                    actual = self.get_all_names_from_products()
                    expected = sorted(actual)
                case FilterOptions.Z_TO_A:
                    actual = self.get_all_names_from_products()
                    expected = sorted(actual, reverse=True)
            assert actual == expected, f"Items are not the same. Actual values: {actual}\nExpected values: {expected}"
