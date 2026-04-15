import logging

import allure
from playwright.sync_api import Page, Locator, expect


class BasePage:
    def __init__(self, page: Page):
        self._page = page
        self._log = logging.getLogger(__name__)

    def _element_fill(self, locator: Locator, value: str, is_password_fill=False) -> None:
        input_value = "******" if is_password_fill else value
        element_name = self._get_element_name(locator)
        log_msg = f"Fill element {element_name}. Value: {input_value}"
        with allure.step(log_msg):
            locator.fill(value)
            self._log.info(log_msg)

    def _element_click(self, locator: Locator) -> None:
        element_name = self._get_element_name(locator)
        log_msg = f"Click element {element_name}"
        with allure.step(log_msg):
            locator.click()
            self._log.info(log_msg)

    def _get_all_text_from_locators(self, locator: Locator) -> list[str]:
        locator_count = locator.count()
        texts = []
        for i in range(locator_count):
            texts.append(self._get_text_from_element(locator.nth(i)))
        return texts

    def _get_text_from_element(self, locator: Locator) -> str:
        element_name = self._get_element_name(locator)
        text = (locator.text_content() or "")
        log_msg = f"Get text from element {element_name}, Value: {text}"
        with allure.step(log_msg):
            self._log.info(log_msg)
            return text

    def _get_all_texts_from_element(self, locator: Locator) -> list[str]:
        all_texts = locator.all_text_contents()
        log_msg = f"Retrieved texts: {all_texts}"
        with allure.step(log_msg):
            self._log.info(log_msg)
            return all_texts

    def _navigate_to_page(self, url: str) -> None:
        self._page.goto(url, wait_until="domcontentloaded")
        self._log.info(f"Navigate to url: {url}")

    @staticmethod
    def _get_element_name(locator: Locator) -> str:
        attributes_priority = [
            "data-test",
            "id",
            "name",
            "aria-label",
            "placeholder",
            "class"
        ]
        for attribute in attributes_priority:
            attribute_value = (locator.get_attribute(attribute) or "")
            if attribute_value:
                return attribute_value

        return "unknown element"

    def _assert_element_should_have_text(self, locator: Locator, expected_text: str):
        element_name = self._get_element_name(locator)
        step_msg = f"Assert that element {element_name}. Should have text: {expected_text}"
        with allure.step(step_msg):
            expect(locator).to_have_text(expected_text)
            actual_text = self._get_text_from_element(locator)
            self._log.info(f"Assert text passed for element {element_name}. "
                          f"Actual text: {actual_text}, expected: {expected_text}")

    def _assert_page_has_url(self, expected_url: str):
        actual_url = self._page.url
        log_msg = f"Assert check page url. Actual: {actual_url}, expected: {expected_url}"
        with allure.step(log_msg):
            expect(self._page).to_have_url(expected_url)
            self._log.info(log_msg)