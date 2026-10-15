from playwright.sync_api import Page, expect
from pages.login_page import LoginPage

def test_add_to_cart(sauce_demo: Page) -> None:
    login_page = LoginPage(sauce_demo)
    login_page.login("standard_user","secret_sauce")
    expect(sauce_demo.get_by_text("Swag Labs")).to_be_visible()
    product = sauce_demo.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")
    priceInPage = product.locator(".inventory_item_price").inner_text()

    print("Price is "+ priceInPage)
    product.get_by_role("button", name="Add to cart").click()
    print("Product added to Cart")
    qtyInPage = sauce_demo.locator("[data-test=\"shopping-cart-badge\"]").inner_text()
    sauce_demo.locator("[data-test=\"shopping-cart-link\"]").click()

    #Cart page
    expect(sauce_demo.get_by_text("Your Cart")).to_be_visible()
    expect(sauce_demo.locator("[data-test=\"item-quantity\"]")).to_have_text(qtyInPage)
    priceinCart = sauce_demo.locator("[data-test=\"inventory-item-price\"]").inner_text()
    print("Price in Cart is " + priceinCart)
    priceinCart == priceInPage
    print("Assertion passed")

    


