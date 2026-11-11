
from pathlib import Path

from playwright.sync_api import Page, expect
from pages.inventory_page import InventoryPage
from utils.db_connection import get_test_customer
from utils.db_connection import get_product_price


def test_add_to_cart(logged_in_sauce_demo: Page) -> None:

    customer = get_test_customer("TC_CHECKOUT_002")

    sauce_demo = logged_in_sauce_demo
    inventory = InventoryPage(sauce_demo)

    # -----------------------------
    # Inventory Page
    # -----------------------------

    expect(inventory.page_title).to_be_visible()

    products = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt", "Sauce Labs Bike Light"]

    for product_name in products:

        expected_price = get_product_price(product_name)
        actual_price = inventory.get_product_price(product_name)

        assert round(actual_price, 2) == float(expected_price), (f"Price mismatch for {product_name}: "
        f"DB={expected_price}, UI={actual_price}")

        print(f"DB validation passed: {product_name}")

        inventory.add_product_to_cart(product_name)

    print("All products validated and added to cart")

    print("Products added to Cart")

    qtyInPage = inventory.get_cart_quantity()
    inventory.open_cart()

    # -----------------------------
    # Cart Page
    # -----------------------------

    expect(sauce_demo.get_by_text("Your Cart")).to_be_visible()

    qty_In_Cart = sauce_demo.locator("//div[@class='cart_item']//div[@class='cart_quantity']")

    quantity = 0

    for i in range(qty_In_Cart.count()):
        qty = int(qty_In_Cart.nth(i).inner_text())
        quantity += qty

    assert qtyInPage == quantity

    priceinCart = sauce_demo.locator("[data-test='inventory-item-price']")

    total = 0

    for i in range(priceinCart.count()):
        price = priceinCart.nth(i).inner_text()
        price = float(price.replace("$", ""))
        total += price

    print(f"Total in Cart Page is {total}")

    sauce_demo.get_by_role("button", name="checkout").click()

    # -----------------------------
    # Checkout: Information
    # -----------------------------

    expect(sauce_demo.locator("[data-test='header-container']")).to_be_visible()

    sauce_demo.locator("[data-test='firstName']").fill(customer["FirstName"])
    sauce_demo.locator("[data-test='lastName']").fill(customer["LastName"])
    sauce_demo.locator("[data-test='postalCode']").fill(customer["PostalCode"])

    sauce_demo.locator("#continue").click()

    # -----------------------------
    # Checkout: Overview
    # -----------------------------

    expect(sauce_demo.locator(".title")).to_have_text("Checkout: Overview")
    product_checkout = sauce_demo.locator("//div[@class='cart_item']//a")

    product_price = sauce_demo.locator(".cart_item [data-test='inventory-item-price']")

    print("Page title:", sauce_demo.title())
    print("Page heading:", sauce_demo.locator(".title").inner_text())    
    print("Cart items:", sauce_demo.locator(".cart_item").count())
    print("All item prices:", sauce_demo.locator("[data-test='inventory-item-price']").count())

    total_in_cart = 0

    for i in range(product_checkout.count()):
        productName = product_checkout.nth(i).inner_text()
        print(productName)

    for i in range(product_price.count()):
        productRate = product_price.nth(i).inner_text()
        productRate = float(productRate.replace("$", ""))

        print(productRate)
        total_in_cart += productRate

    print(f"Total in Checkout page is {total_in_cart}")

    sub_total = float(sauce_demo.locator("[data-test='subtotal-label']").inner_text().replace("Item total: $", ""))

    tax = float(sauce_demo.locator("[data-test='tax-label']").inner_text().replace("Tax: $", ""))

    totalValue = float(sauce_demo.locator("[data-test='total-label']").inner_text().replace("Total: $", "")
)

    # -----------------------------
    # Price Assertions
    # -----------------------------

    assert round(totalValue, 2) == round(sub_total + tax, 2), "Total within Overview is NOT matching"
    assert round(total_in_cart, 2) == round(totalValue - tax, 2), "Total in Cart & Overview is NOT matching"
    assert round(total, 2) == round(total_in_cart, 2), "Cart total and checkout subtotal do not match"

    
    # Finish Order
    sauce_demo.get_by_role("button", name="finish").click()


    # Order Confirmation   
    expect(sauce_demo.locator("[data-test='title']")).to_have_text("Checkout: Complete!")
    expect(sauce_demo.locator("[data-test='complete-header']")).to_have_text("Thank you for your order!")
    expect(sauce_demo.locator("[data-test='complete-text']")).to_contain_text("Your order has been dispatched")
    expect(sauce_demo.locator("[data-test='back-to-products']")).to_be_enabled()

    # Optional: Only assert this if your application has the PDF feature
    # expect(
    #     sauce_demo.locator("[data-test='generate-pdf-order']")
    # ).to_be_enabled()

    print("Order Placed Successfully")

    Path("test-results").mkdir(parents=True, exist_ok=True)

    sauce_demo.screenshot(path="test-results/order-placed.png")
