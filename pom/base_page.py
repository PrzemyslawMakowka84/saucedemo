import logging

import allure
from playwright.sync_api import Page, Locator, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger(__name__)

    def element_fill(self, locator: Locator, value: str, is_password_fill=False) -> None:
        input_value = "******" if is_password_fill else value
        element_name = self.get_element_name(locator)
        log_msg = f"Fill element {element_name}. Value: {input_value}"
        with allure.step(log_msg):
            locator.fill(value)
            self.log.info(log_msg)

    def element_click(self, locator: Locator) -> None:
        element_name = self.get_element_name(locator)
        log_msg = f"Click element {element_name}"
        with allure.step(log_msg):
            locator.click()
            self.log.info(log_msg)

    def get_text_from_element(self, locator: Locator) -> str:
        element_name = self.get_element_name(locator)
        text = locator.text_content()
        log_msg = f"Get text from element {element_name}, Value: {text}"
        with allure.step(log_msg):
            self.log.info(log_msg)
            return text

    def navigate_to_page(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")
        self.log.info(f"Navigate to url: {url}")

    @staticmethod
    def get_element_name(locator: Locator) -> str:
        attributes_priority = [
            "data-test",
            "id",
            "name",
            "aria-label",
            "placeholder",
            "class"
        ]
        for attribute in attributes_priority:
            if locator.get_attribute(attribute):
                return locator.get_attribute(attribute)

        return "unknown element"

    def assert_element_should_have_text(self, locator: Locator, expected_text: str):
        element_name = self.get_element_name(locator)
        step_msg = f"Assert that element {element_name}. Should have text: {expected_text}"
        with allure.step(step_msg):
            expect(locator).to_have_text(expected_text)
            actual_text = self.get_text_from_element(locator)
            self.log.info(f"Assert text passed for element {element_name}. "
                          f"Actual text: {actual_text}, expected: {expected_text}")

    def assert_page_has_url(self, expected_url: str):
        actual_url = self.page.url
        log_msg = f"Assert check page url. Actual: {actual_url}, expected: {expected_url}"
        with allure.step(log_msg):
            expect(self.page).to_have_url(expected_url)
            self.log.info(log_msg)