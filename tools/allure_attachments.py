import allure
from allure_commons.types import AttachmentType
from playwright.sync_api import Page


def attach_screenshot_to_allure(page: Page, name: str, file_type: AttachmentType = AttachmentType.PNG) -> None:
    screenshot = page.screenshot()
    allure.attach(screenshot, name=name, attachment_type=file_type)


def attach_dom_to_allure(page: Page, name: str) -> None:
    dom = page.content()
    allure.attach(dom, name=name, attachment_type=AttachmentType.TEXT)


def attach_browser_logs_to_allure(logs: list[str], name: str) -> None:
    allure.attach("\n".join(logs), name=name, attachment_type=AttachmentType.TEXT)