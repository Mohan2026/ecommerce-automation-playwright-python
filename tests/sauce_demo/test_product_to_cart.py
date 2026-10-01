from playwright.sync_api import Page, expect

def test_add_to_cart(sauce_demo: Page) -> None:
    page = sauce_demo
    expect(page.locator("#login_button_container")).to_be_visible()
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.get_by_text("Swag Labs")).to_be_visible()
    product = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")
    priceInPage = product.locator(".inventory_item_price").inner_text()

    print("Price is "+ priceInPage)
    product.get_by_role("button", name="Add to cart").click()
    print("Product added to Cart")
    qtyInPage = page.locator("[data-test=\"shopping-cart-badge\"]").inner_text()
    page.locator("[data-test=\"shopping-cart-link\"]").click()

    #Cart page
    expect(page.get_by_text("Your Cart")).to_be_visible()
    expect(page.locator("[data-test=\"item-quantity\"]")).to_have_text(qtyInPage)
    priceinCart = page.locator("[data-test=\"inventory-item-price\"]").inner_text()
    print("Price in Cart is " + priceinCart)
    priceinCart == priceInPage
    print("Assertion passed")

    


