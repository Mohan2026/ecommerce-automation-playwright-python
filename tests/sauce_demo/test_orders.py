from playwright.sync_api import Page, expect
from pages.login_page import LoginPage

def test_add_to_cart(sauce_demo: Page):
    login_page = LoginPage(sauce_demo)
    login_page.login("standard_user","secret_sauce")
    expect(sauce_demo.get_by_text("Swag Labs")).to_be_visible()

    product_1 = sauce_demo.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")
    priceInPage = product_1.locator(".inventory_item_price").inner_text()
    product_1.get_by_role("button", name="Add to cart").click()

    product_2 = sauce_demo.locator(".inventory_item").filter(has_text="Sauce Labs Bolt T-Shirt")
    product_2.get_by_role("button", name="Add to cart").click()

    product_3 = sauce_demo.locator(".inventory_item").filter(has_text="Sauce Labs Bike Light")
    product_3.get_by_role("button", name="Add to cart").click()

    print("Products added to Cart")
    qtyInPage = sauce_demo.locator("[data-test=\"shopping-cart-badge\"]").inner_text()
    sauce_demo.locator("[data-test=\"shopping-cart-link\"]").click()

    #Cart page
    expect(sauce_demo.get_by_text("Your Cart")).to_be_visible()
    qty_In_Cart = sauce_demo.locator("//div[@class='cart_item']//div[@class='cart_quantity']")
    quantity = 0
    for i in range(qty_In_Cart.count()):
         qty = int(qty_In_Cart.nth(i).inner_text())
         quantity += qty

    assert int(qtyInPage) == quantity

    priceinCart = sauce_demo.locator("[data-test=\"inventory-item-price\"]")
    total = 0
    for i in range(priceinCart.count()):
        price = priceinCart.nth(i).inner_text()
        price = float(price.replace(("$"),""))
        total += price
    print(f"Total in Cart Page is {total}")

    sauce_demo.get_by_role("button", name ="checkout").click()

    #Checkout: Info
    expect(sauce_demo.locator("[data-test=\"header-container\"]")).to_be_visible()
    sauce_demo.locator("[data-test=\"firstName\"]").fill("John")
    sauce_demo.locator("[data-test=\"lastName\"]").fill("Test")
    sauce_demo.locator("[data-test=\"postalCode\"]").fill("N2J2K2")
    sauce_demo.locator("#continue").click()

    #Checkout: Overview
    expect(sauce_demo.locator(".title")).to_have_text("Checkout: Overview")

    product_checkout = sauce_demo.locator("//div[@class='cart_item']//a")
    #product_price = sauce_demo.locator("[data-test='inventory-item-price']")
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
        productRate = float(productRate.replace("$","")) 
        print(productRate)
        total_in_cart += productRate

    print(f"Total in Checkout page is {total_in_cart}")

    sub_total = float(sauce_demo.locator("[data-test=\"subtotal-label\"]").inner_text().replace("Item total: $",""))
    tax = float(sauce_demo.locator("[data-test=\"tax-label\"]").inner_text().replace("Tax: $",""))
    totalValue = float(sauce_demo.locator("[data-test=\"total-label\"]").inner_text().replace("Total: $",""))

    #Assertion for prices between Cart & Checkout
    assert totalValue == sub_total + tax, "Total within Overview is NOT matching"
    assert total_in_cart == totalValue - tax, " Total in Cart & Overview is NOT matching"

    #Click Finish
    sauce_demo.get_by_role("button", name = "finish").click()

    #Verify Order Confirmation
    expect(sauce_demo.locator("[data-test=\"title\"]").filter(has_text="Checkout: Complete!"))
    expect(sauce_demo.locator("[data-test=\"complete-header\"]").filter(has_text="Thank you for your order!"))
    expect(sauce_demo.locator("[data-test=\"complete-text\"]").filter(has_text="Your order has been dispatched"))
    expect(sauce_demo.locator("[data-test='back-to-products']")).to_be_enabled()
    expect(sauce_demo.locator("[data-test='generate-pdf-order']")).to_be_enabled()
    print("Order Placed Successfully")
    sauce_demo.screenshot(path = "test-results/order-placed.png")

    
        