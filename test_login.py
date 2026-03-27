import allure
import pytest

from pom.login_page import LoginPage
from pom.inventory_page import InventoryPage

@allure.parent_suite("Saucedemo tests")
@allure.suite("Login tests")

@pytest.mark.parametrize(
    "user_key, is_success",
    [
        pytest.param("standard_user", True, id="Standard user"),
        pytest.param("locked_out_user", False, id="Locked out user"),
        pytest.param("problem_user", True, id="Problem user"),
        pytest.param("performance_glitch_user", True, id="Performance glitch_user"),
        pytest.param("error_user", True, id="Error user"),
        pytest.param("visual_user", True, id="Visual user"),
    ]
)
def test_login(
        login_page: LoginPage,
        inventory_page: InventoryPage,
        credentials: dict[str, str],
        user_key: str,
        is_success: bool
):
    username = credentials[user_key]
    password = credentials["password"]
    login_page.navigate_to_login_page()
    login_page.login(username=username, password=password)
    if is_success:
        expected_text = "Swag Labs"
        inventory_page.assert_app_logo_should_have_text(expected_text)
    else:
        expected_text = "Epic sadface: Sorry, this user has been locked out."
        login_page.assert_message_container_should_have_text(expected_text)
