import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from pom.inventory_page import InventoryPage
from pom.login_page import LoginPage


@pytest.fixture(scope="session")
def playwright(playwright):
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
