from playwright.sync_api import Page

from pom.base_page import BasePage


class CheckoutPage(BasePage):
    URL = "https://www.saucedemo.com/checkout-step-one.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self._header_page = self._page.get_by_test_id("secondary-header")
        self._first_name = self._page.get_by_test_id("firstName")
        self._last_name = self._page.get_by_test_id("lastName")
        self._postal_code = self._page.get_by_test_id("postalCode")
        self._continue_button = self._page.get_by_test_id("continue")

    def _fill_first_name(self, first_name: str) -> None:
        self._element_fill(self._first_name, first_name)

    def _fill_last_name(self, last_name: str) -> None:
        self._element_fill(self._last_name, last_name)

    def _fill_postal_code(self, postal_code: str) -> None:
        self._element_fill(self._postal_code, postal_code)

    def _click_continue_button(self) -> None:
        self._element_click(self._continue_button)

    def fill_form(self, first_name: str, last_name: str, postal_code: str) -> None:
        self._fill_first_name(first_name)
        self._fill_last_name(last_name)
        self._fill_postal_code(postal_code)

    def assert_user_goto_checkout_page(self):
        self._assert_page_has_url(self.URL)
        self._assert_element_is_visible(self._header_page)
        self._assert_element_should_have_text(self._header_page, expected_text="Checkout: Your Information")