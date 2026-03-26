from playwright.sync_api import Page, expect
from pom.base_page import BasePage

class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._primary_header = page.get_by_test_id("primary-header")

    def get_text_from_app_logo(self):
        return self.get_text_from_element(self._primary_header.locator(".app_logo"))

    def assert_app_logo_should_have_text(self, expected_text: str):
        expect(self._primary_header.locator(".app_logo")).to_have_text(expected_text)