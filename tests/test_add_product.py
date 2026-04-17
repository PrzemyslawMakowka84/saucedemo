from pom.cart_page import CartPage
from pom.inventory_page import InventoryPage
from pom.login_page import LoginPage

def test_add_product_to_basket(login_page: LoginPage, inventory_page:  InventoryPage, cart_page: CartPage, credentials):
    login_page.login(credentials["standard_user"], credentials["password"])
    products_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
    expected_articles = []
    for product in products_to_add:
        expected_product = inventory_page.get_product_data(product)
        inventory_page.add_article_to_basket(product)
        expected_articles.append(expected_product)
    inventory_page.go_to_basket()
    actual_articles = cart_page.get_articles_from_cart()
    assert actual_articles == expected_articles, \
        f"Products are in basket are different on the cart. Actual: {actual_articles}, Expected: {expected_articles}"