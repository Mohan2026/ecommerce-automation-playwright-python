
from playwright.sync_api import Page


class CartPage:

    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.page_title = page.locator(".title")
        self.cart_items = page.locator(".cart_item")
        self.cart_quantities = page.locator(
            ".cart_item .cart_quantity"
        )
        self.cart_prices = page.locator(
            ".cart_item [data-test='inventory-item-price']"
        )
        self.checkout_button = page.get_by_role(
            "button", name="Checkout"
        )

    def get_cart_quantity(self):
        quantity = 0

        for i in range(self.cart_quantities.count()):
            qty = int(
                self.cart_quantities.nth(i).inner_text()
            )
            quantity += qty

        return quantity

    def get_cart_total(self):
        total = 0.0

        for i in range(self.cart_prices.count()):
            price = self.cart_prices.nth(i).inner_text()
            price = float(price.replace("$", ""))
            total += price

        return round(total, 2)

    def get_cart_item_count(self):
        return self.cart_items.count()

    def proceed_to_checkout(self):
        self.checkout_button.click()
