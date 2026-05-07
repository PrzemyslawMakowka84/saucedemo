from decimal import Decimal

from pom.products.cart_page import CartPage
from pom.products.checkout_information_page import CheckoutInformationPage
from pom.products.checkout_overview_page import CheckOutOverviewPage
from pom.products.inventory_page import InventoryPage
from pom.login_page import LoginPage
from pom.products.products_section import QUANTIZE


def test_full_order_flow(
        login_page: LoginPage,
        inventory_page: InventoryPage,
        cart_page: CartPage,
        checkout_information_page: CheckoutInformationPage,
        checkout_overview_page: CheckOutOverviewPage,
        credentials):
    login_page.login(credentials["standard_user"], credentials["password"])
    products_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
    expected_articles = []
    for product in products_to_add:
        expected_product = inventory_page.get_product_data(product)
        inventory_page.add_article_to_basket(product)
        expected_articles.append(expected_product)
    inventory_page.go_to_basket()
    actual_articles = cart_page.get_articles()
    assert actual_articles == expected_articles, \
        f"Products in basket are different on the cart. Actual: {actual_articles}, Expected: {expected_articles}"
    cart_page.goto_checkout()
    expected_title_text = "Checkout: Your Information"
    checkout_information_page.assert_user_goto_checkout_page(expected_text=expected_title_text)
    checkout_information_page.fill_form(first_name="test", last_name="test", postal_code="12345")
    checkout_information_page.click_continue_button()

    actual_articles = checkout_overview_page.get_articles()
    assert actual_articles == expected_articles, \
        f"Products in basket are different on the checkout. Actual: {actual_articles}, Expected: {expected_articles}"

    actual_subtotal_price = checkout_overview_page.get_actual_subtotal_price()
    actual_tax_price = checkout_overview_page.get_actual_tax_price()
    actual_total_price = checkout_overview_page.get_actual_total_price()

    expected_subtotal_price = sum(article.price for article in expected_articles)
    expected_tax_price = (expected_subtotal_price * Decimal("0.08")).quantize(QUANTIZE)
    expected_total_price = (expected_subtotal_price + expected_tax_price).quantize(QUANTIZE)

    assert actual_subtotal_price == expected_subtotal_price, \
        f"Actual subtotal price is different from expected. Actual: {actual_subtotal_price}, Expected: {expected_subtotal_price}"
    assert actual_tax_price == expected_tax_price, \
        f"Actual tax price is different from expected. Actual: {actual_tax_price}, Expected: {expected_tax_price}"
    assert actual_total_price == expected_total_price, \
        f"Actual total price is different from expected. Actual: {actual_total_price}, Expected: {expected_total_price}"

    checkout_overview_page.finish_order()
    checkout_overview_page.back_to_products()

    inventory_page.assert_user_logged_on_inventory_page("Products")