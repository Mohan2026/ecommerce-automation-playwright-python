
from playwright.sync_api import Page, expect

def test_valid_login(page: Page) -> None:
    page.goto("https://www.saucedemo.com/")
    expect(page.locator("#login_button_container")).to_be_visible()
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    expect(page.locator("[data-test=\"login-button\"]")).to_be_enabled
    page.locator("[data-test=\"login-button\"]").click()
    print("Login Clicked")
    page.get_by_text("Swag Labs").click()
    expect(page.get_by_text("Swag Labs")).to_be_visible()
    expect(page.locator("[data-test=\"primary-header\"]")).to_contain_text("Swag Labs")
    print("Login Passed")
