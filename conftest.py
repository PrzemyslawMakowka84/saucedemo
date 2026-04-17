import os
from typing import Generator, Any

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, Playwright, ConsoleMessage

from pom.cart_page import CartPage
from pom.inventory_page import InventoryPage
from pom.login_page import LoginPage
from tools.allure_attachments import attach_screenshot_to_allure, attach_dom_to_allure, attach_browser_logs_to_allure


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    is_failed = report.when == "call" and report.failed
    is_xfail = report.when == "call" and getattr(report, "wasxfail", None) is not None
    if is_failed or is_xfail:
        page = item.funcargs.get("page")
        browser_logs = item.funcargs.get("browser_logs")
        test_name = item.name
        if page:
            attach_screenshot_to_allure(page=page, name=f"Failed: {test_name}")
            attach_dom_to_allure(page=page, name=f"Dom page {page.url}")
            if browser_logs:
                attach_browser_logs_to_allure(logs=browser_logs, name=f"Browser logs in fail {test_name}")

@pytest.fixture(autouse=True)
def browser_logs(page: Page) -> Generator[list[str], Any, None]:
    logs = []

    def handle_console(msg: ConsoleMessage):
        logs.append(f"[console:{msg.type}] {msg.text}")

    def handle_page_error(error):
        logs.append(f"[pageerror] {str(error)}")

    page.on("console", handle_console)
    page.on("pageerror", handle_page_error)

    yield logs

@pytest.fixture(scope="session")
def playwright(playwright: Playwright) -> Playwright:
    playwright.selectors.set_test_id_attribute("data-test")
    return playwright


@pytest.fixture(scope="session")
def credentials() -> dict[str, str]:
    user_names = [
        "STANDARD_USER",
        "LOCKED_OUT_USER",
        "PROBLEM_USER",
        "PERFORMANCE_GLITCH_USER",
        "ERROR_USER",
        "VISUAL_USER"
    ]
    load_dotenv()
    credentials = {}
    for user_name in user_names:
        credentials[user_name.lower()] = os.getenv(user_name)
    credentials["password"] = os.getenv("PASSWORD")
    if not all(credentials.values()):
        raise ValueError("Invalid Credentials!, Check the .env file or user_names list!")
    return credentials


@pytest.fixture
def login_page(page: Page, credentials) -> LoginPage:
    return LoginPage(page, credentials)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)
