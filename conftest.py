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
    load_dotenv()
    user = os.getenv("SAUCE_USER")
    password = os.getenv("SAUCE_PASSWORD")
    if user and password:
        return {
            "user": user,
            "password": password
        }
    else:
        raise ValueError("Invalid Credentials!, Check the .env file!")


@pytest.fixture
def login_page(page: Page, credentials) -> LoginPage:
    return LoginPage(page, credentials)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)
