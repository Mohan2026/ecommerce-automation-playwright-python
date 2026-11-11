
from playwright.sync_api import Page


class InventoryPage:

    def __init__(self, page: Page):
        self.page = page

        # Page locators
        self.page_title = page.get_by_text("Swag Labs")
        self.products = page.locator(".inventory_item")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")
        self.cart_link = page.locator("[data-test='shopping-cart-link']")

    def get_product(self, product_name):
        return self.products.filter(has_text=product_name)

    def get_product_price(self, product_name):
        product = self.get_product(product_name)

        price = product.locator(".inventory_item_price").inner_text()

        return float(price.replace("$", ""))

    def add_product_to_cart(self, product_name):
        product = self.get_product(product_name)

        product.get_by_role("button", name="Add to cart").click()

    def get_cart_quantity(self):
        return int(self.cart_badge.inner_text())

    def open_cart(self):
        self.cart_link.click()
