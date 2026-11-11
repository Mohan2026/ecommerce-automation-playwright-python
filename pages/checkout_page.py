
from playwright.sync_api import Page


class CheckoutPage:

    def __init__(self, page: Page):
        self.page = page

        # Checkout: Information
        self.page_title = page.locator(".title")
        self.header_container = page.locator(
            "[data-test='header-container']"
        )
        self.first_name = page.locator(
            "[data-test='firstName']"
        )
        self.last_name = page.locator(
            "[data-test='lastName']"
        )
        self.postal_code = page.locator(
            "[data-test='postalCode']"
        )
        self.continue_button = page.locator("#continue")

        # Checkout: Overview
        self.checkout_items = page.locator(".cart_item")
        self.product_names = page.locator(
            ".cart_item .inventory_item_name"
        )
        self.product_prices = page.locator(
            ".cart_item [data-test='inventory-item-price']"
        )
        self.subtotal_label = page.locator(
            "[data-test='subtotal-label']"
        )
        self.tax_label = page.locator(
            "[data-test='tax-label']"
        )
        self.total_label = page.locator(
            "[data-test='total-label']"
        )
        self.finish_button = page.get_by_role(
            "button", name="Finish"
        )

        # Order Confirmation
        self.confirmation_title = page.locator(
            "[data-test='title']"
        )
        self.confirmation_header = page.locator(
            "[data-test='complete-header']"
        )
        self.confirmation_text = page.locator(
            "[data-test='complete-text']"
        )
        self.back_to_products = page.locator(
            "[data-test='back-to-products']"
        )
        self.generate_pdf_order = page.locator(
            "[data-test='generate-pdf-order']"
        )

    def enter_customer_information(
        self, first_name, last_name, postal_code
    ):
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)
        self.continue_button.click()

    def get_checkout_item_count(self):
        return self.checkout_items.count()

    def get_checkout_total(self):
        total = 0.0

        for i in range(self.product_prices.count()):
            price = self.product_prices.nth(i).inner_text()
            total += float(price.replace("$", ""))

        return round(total, 2)

    def get_subtotal(self):
        text = self.subtotal_label.inner_text()
        return float(text.replace("Item total: $", ""))

    def get_tax(self):
        text = self.tax_label.inner_text()
        return float(text.replace("Tax: $", ""))

    def get_total(self):
        text = self.total_label.inner_text()
        return float(text.replace("Total: $", ""))

    def finish_order(self):
        self.finish_button.click()
