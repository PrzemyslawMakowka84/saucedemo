
from pom.inventory_page import InventoryPage
from pom.login_page import LoginPage

def test_add_product_to_basket(login_page: LoginPage, inventory_page: InventoryPage, credentials):
    login_page.login(credentials["standard_user"], credentials["password"])
    inventory_page.add_article_to_basket("Sauce Labs Backpack")
    inventory_page.add_article_to_basket("Sauce Labs Bolt T-Shirt")
    inventory_page.go_to_basket()