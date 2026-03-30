import allure
from playwright.sync_api import Page

from pom.base_page import BasePage


class InventoryPage(BasePage):
    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self._primary_header = page.get_by_test_id("primary-header")
        self._app_logo = self._primary_header.locator(".app_logo")

    def assert_user_logged_on_inventory_page(self, expected_title_page_text: str):
        with allure.step(f"Assert that user logged into the shop"):
            self.assert_element_should_have_text(locator=self._app_logo, expected_text=expected_title_page_text)
            self.assert_page_has_url(expected_url=self.URL)
