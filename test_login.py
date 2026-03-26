import allure

from pom.login_page import LoginPage
from pom.inventory_page import InventoryPage

@allure.parent_suite("Saucedemo tests")
@allure.suite("Login tests")
@allure.title("Login test – correct login and password")
def test_login(login_page: LoginPage, inventory_page: InventoryPage) -> None:
    expected_text = "Swag Labs"
    login_page.navigate_to_login_page()
    login_page.input_username()
    login_page.input_password()
    login_page.click_login_button()
    inventory_page.assert_app_logo_should_have_text(expected_text)
