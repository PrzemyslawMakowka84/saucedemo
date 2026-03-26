import allure
from playwright.sync_api import Page, expect
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

    @allure.step("Input password")
    def input_password(self, password: str) -> None:
        self.element_fill(self._password, password, is_password_fill=True)

    @allure.step("Click login button")
    def click_login_button(self) -> None:
        self.element_click(self._login_button)

    @allure.step("Navigate to login page")
    def navigate_to_login_page(self) -> None:
        self.page.goto(self.URL)
        self.log.info(f"Navigate to url: {self.URL}")

    @allure.step("Login to shop")
    def login(self) -> None:
        self.navigate_to_login_page()
        self.input_username()
        self.input_password()
        self.click_login_button()

    def assert_message_container_should_have_text(self, expected_text: str):
        self.assert_element_should_have_text(locator=self.error_message_container, expected_text=expected_text)
