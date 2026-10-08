from playwright.sync_api import Page, expect

def test_add_to_cart(sauce_demo: Page):
    page = sauce_demo
    expect(page.locator("#login_button_container")).to_be_visible()
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.get_by_text("Swag Labs")).to_be_visible()

    product_1 = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")
    priceInPage = product_1.locator(".inventory_item_price").inner_text()
    product_1.get_by_role("button", name="Add to cart").click()

    product_2 = page.locator(".inventory_item").filter(has_text="Sauce Labs Bolt T-Shirt")
    product_2.get_by_role("button", name="Add to cart").click()

    product_3 = page.locator(".inventory_item").filter(has_text="Sauce Labs Bike Light")
    product_3.get_by_role("button", name="Add to cart").click()

    print("Products added to Cart")
    qtyInPage = page.locator("[data-test=\"shopping-cart-badge\"]").inner_text()
    page.locator("[data-test=\"shopping-cart-link\"]").click()

    #Cart page
    expect(page.get_by_text("Your Cart")).to_be_visible()
    qty_In_Cart = page.locator("//div[@class='cart_item']//div[@class='cart_quantity']")
    quantity = 0
    for i in range(qty_In_Cart.count()):
         qty = int(qty_In_Cart.nth(i).inner_text())
         quantity += qty

    assert int(qtyInPage) == quantity

    priceinCart = page.locator("[data-test=\"inventory-item-price\"]")
    total = 0
    for i in range(priceinCart.count()):
        price = priceinCart.nth(i).inner_text()
        price = float(price.replace(("$"),""))
        total += price
    print(f"Total in Cart Page is {total}")

    page.get_by_role("button", name ="checkout").click()

    #Checkout: Info
    expect(page.locator("[data-test=\"header-container\"]")).to_be_visible()
    page.locator("[data-test=\"firstName\"]").fill("John")
    page.locator("[data-test=\"lastName\"]").fill("Test")
    page.locator("[data-test=\"postalCode\"]").fill("N2J2K2")
    page.locator("#continue").click()

    #Checkout: Overview
    expect(page.locator("[data-test=\"title\"]")).to_be_visible()

    product_checkout = page.locator("//div[@class='cart_item']//a")
    product_price = page.locator("[data-test='inventory-item-price']")
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

    sub_total = float(page.locator("[data-test=\"subtotal-label\"]").inner_text().replace("Item total: $",""))
    tax = float(page.locator("[data-test=\"tax-label\"]").inner_text().replace("Tax: $",""))
    totalValue = float(page.locator("[data-test=\"total-label\"]").inner_text().replace("Total: $",""))

    #Assertion for prices between Cart & Checkout
    assert totalValue == sub_total + tax, "Total within Overview is NOT matching"
    assert total_in_cart == totalValue - tax, " Total in Cart & Overview is NOT matching"

    #Click Finish
    page.get_by_role("button", name = "finish").click()

    #Verify Order Confirmation
    expect(page.locator("[data-test=\"title\"]").filter(has_text="Checkout: Complete!"))
    expect(page.locator("[data-test=\"complete-header\"]").filter(has_text="Thank you for your order!"))
    expect(page.locator("[data-test=\"complete-text\"]").filter(has_text="Your order has been dispatched"))
    expect(page.locator("[data-test='back-to-products']")).to_be_enabled()
    expect(page.locator("[data-test='generate-pdf-order']")).to_be_enabled()
    print("Order Placed Successfully")
    page.screenshot(path = "test-results/order-placed.png")

    
        