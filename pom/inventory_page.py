from dataclasses import dataclass
from enum import StrEnum

import allure
from playwright.sync_api import Page

from pom.base_page import BasePage


class FilterOptions(StrEnum):
    LOW_TO_HIGH = "lohi"
    HIGH_TO_LOW = "hilo"
    A_TO_Z = "az"
    Z_TO_A = "za"

@dataclass
class Article:
    product_name: str
    description: str
    price: float

class InventoryPage(BasePage):
    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self._primary_header = self._page.get_by_test_id("primary-header")
        self._app_logo = self._primary_header.locator(".app_logo")
        self._inventory_itmes = self._page.get_by_test_id("inventory-item")
        self._product_names = self._page.get_by_test_id("inventory-item-name")
        self._product_descriptions = self._page.get_by_test_id("inventory-item-desc")
        self._product_prices = self._page.get_by_test_id("inventory-item-price")
        self._select_filter_container = self._page.get_by_test_id("product-sort-container")
        self._add_article_to_basket_button = self._page.locator("[data-test^='add-to-cart']")
        self._basket = self._page.get_by_test_id("shopping-cart-badge")

        self.articles: list[Article] = []

    def get_all_prices_from_products(self) -> list[float]:
        return [
            float(price.replace("$", "")) for price in self._get_all_text_from_locators(self._product_prices)
        ]

    def get_all_names_from_products(self) -> list[str]:
        products = self._get_all_text_from_locators(self._product_names)
        return products

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

    def add_article_to_basket(self, product_name: str):
        self._click_add_to_cart(product_name)
        name: str = self._get_product_name(product_name)
        description: str = self._get_description_from_product(product_name)
        price: float = self._get_price_from_product(product_name)
        self.articles.append(
            Article(name, description, price)
        )

    def _click_add_to_cart(self, product_name: str):
        index = self._get_product_index(product_name)
        self._element_click(self._add_article_to_basket_button.nth(index))

    def go_to_basket(self):
        self._element_click(self._basket)

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
