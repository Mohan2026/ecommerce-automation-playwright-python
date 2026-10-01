from playwright.sync_api import Page, expect

def test_valid_login(sauce_demo: Page) -> None:
    page = sauce_demo
    expect(page.locator("#login_button_container")).to_be_visible()
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    expect(page.locator("[data-test=\"login-button\"]")).to_be_enabled
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.get_by_text("Swag Labs")).to_be_visible()
    print("Login Passed")


def test_invalid_login(sauce_demo: Page) -> None:
    page = sauce_demo
    expect(page.locator("#login_button_container")).to_be_visible()
    page.locator("[data-test=\"username\"]").fill("random_user")
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    expect(page.locator("[data-test=\"login-button\"]")).to_be_enabled
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_be_visible()
    expect(page.locator("[data-test=\"error\"]")).to_contain_text("Username and password do not match any user in this service")
    expect(page.locator("[data-test=\"error-button\"]")).to_be_enabled
    print("Login Failed")

    
def test_locked_out_user(sauce_demo: Page) -> None:
    page = sauce_demo
    expect(page.locator("#login_button_container")).to_be_visible()
    page.locator("[data-test=\"username\"]").fill("locked_out_user")
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    expect(page.locator("[data-test=\"login-button\"]")).to_be_enabled
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_be_visible()
    expect(page.locator("[data-test=\"error\"]")).to_contain_text("Sorry, this user has been locked out.")
    expect(page.locator("[data-test=\"error-button\"]")).to_be_enabled
    print("Login Failed with Locked Out User")

def test_empty_user(sauce_demo: Page) -> None:
    page = sauce_demo
    expect(page.locator("#login_button_container")).to_be_visible()
    page.locator("[data-test=\"username\"]").fill("dummy")
    #page.locator("[data-test=\"password\"]").fill("secret_sauce")
    expect(page.locator("[data-test=\"login-button\"]")).to_be_enabled
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_be_visible()
    expect(page.locator("[data-test=\"error\"]")).to_contain_text("Password is required")
    print("Login Failed without password")