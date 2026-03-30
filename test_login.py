import allure
import pytest

from pom.inventory_page import InventoryPage
from pom.login_page import LoginPage


@allure.parent_suite("Saucedemo tests")
@allure.suite("Login tests")
@pytest.mark.parametrize(
    "user_key",
    [
        pytest.param("standard_user", id="Standard user"),
        pytest.param("problem_user", id="Problem user"),
        pytest.param("performance_glitch_user", id="Performance glitch_user"),
        pytest.param("error_user", id="Error user"),
        pytest.param("visual_user", id="Visual user"),
    ]
)
def test_login_positive_cases(
        login_page: LoginPage,
        inventory_page: InventoryPage,
        credentials: dict[str, str],
        user_key: str,
):
    username = credentials[user_key]
    password = credentials["password"]
    login_page.login(username=username, password=password)
    expected_text = "Swag Labs"
    inventory_page.assert_user_logged_on_inventory_page(expected_title_page_text=expected_text)


@allure.parent_suite("Saucedemo tests")
@allure.suite("Login tests")
@allure.title("Locked out user")
def test_login_locked_user(login_page: LoginPage, credentials: dict[str, str]):
    username = credentials["locked_out_user"]
    password = credentials["password"]
    login_page.login(username=username, password=password)
    expected_error_message = "Epic sadface: Sorry, this user has been locked out."
    login_page.assert_error_message_container_should_have_text(expected_error_message)


@allure.parent_suite("Saucedemo tests")
@allure.suite("Login tests")
@pytest.mark.parametrize(
    "username, password, expected_error_message",
    [
        pytest.param("", "", "Epic sadface: Username is required", id="Empty username and password"),
        pytest.param("wrong_user", "", "Epic sadface: Password is required", id="Username and empty password"),
        pytest.param("", "wrong_password", "Epic sadface: Username is required", id="Performance glitch_user"),
        pytest.param(
            "wrong_user",
            "wrong_password",
            "Epic sadface: Username and password do not match any user in this service",
            id="Error user"
        ),
    ]
)
def test_login_negative_cases(login_page: LoginPage, username: str, password: str, expected_error_message: str):
    login_page.login(username=username, password=password)
    login_page.assert_error_message_container_should_have_text(expected_error_message)
