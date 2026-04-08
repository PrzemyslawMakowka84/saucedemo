import allure
from playwright.sync_api import Page

from pom.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page, credentials):
        super().__init__(page)
        self._credentials = credentials
        self._username = self.page.get_by_test_id("username")
        self._password = self.page.get_by_test_id("password")
        self._login_button = self.page.get_by_test_id("login-button")
        self.error_message_container = self.page.get_by_test_id("error")

    @allure.step("Input username")
    def input_username(self, username: str) -> None:
        self.element_fill(self._username, username)

    def input_password(self, password: str) -> None:
        with allure.step("Input password"):  # To hide password in Allure Report
            self.element_fill(self._password, password, is_password_fill=True)

    @allure.step("Click login button")
    def click_login_button(self) -> None:
        self.element_click(self._login_button)

    @allure.step("Navigate to login page")
    def navigate(self) -> None:
        self.navigate_to_page(self.URL)

    def login(self, username: str, password: str) -> None:
        self.navigate()
        self.input_username(username)
        self.input_password(password)
        self.click_login_button()

    def assert_error_message_container_should_have_text(self, expected_text: str):
        self.assert_element_should_have_text(locator=self.error_message_container, expected_text=expected_text)

    def assert_access_to_inventory_was_denied(self, expected_text: str):
        self.assert_page_has_url(self.URL)
        self.assert_error_message_container_should_have_text(expected_text=expected_text)
