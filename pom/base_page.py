import logging

import allure
from playwright.sync_api import Page, Locator


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger(__name__)

    def element_fill(self, locator: Locator, value: str, is_password_fill=False) -> None:
        input_value = "******" if is_password_fill else value
        element_name = self._get_element_name(locator)
        log_msg = f"Fill element {element_name}. Value: {input_value}"
        with allure.step(log_msg):
            locator.fill(value)
            self.log.info(log_msg)

    def element_click(self, locator: Locator) -> None:
        element_name = self._get_element_name(locator)
        log_msg = f"Click element {element_name}"
        with allure.step(log_msg):
            locator.click()
            self.log.info(log_msg)

    def get_text_from_element(self, locator: Locator) -> str:
        element_name = self._get_element_name(locator)
        log_msg = f"Get text from element {element_name}"
        with allure.step(log_msg):
            text = locator.text_content()
            self.log.info(log_msg)
            return text

    @staticmethod
    def _get_element_name(locator: Locator) -> str:
        attributes_priority = [
            "data-test",
            "id",
            "name",
            "aria-label",
            "placeholder"
        ]
        for attribute in attributes_priority:
            if locator.get_attribute(attribute):
                return locator.get_attribute(attribute)

        return "unknown element"