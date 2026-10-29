from playwright.sync_api import Page, expect
from pages.login_page import LoginPage

def test_valid_login(sauce_demo: Page) -> None:
    """Verify a valid user can log in successfully."""
    login_page = LoginPage(sauce_demo)
    login_page.login("standard_user","secret_sauce")
    expect(sauce_demo.get_by_text("Swag Labs")).to_be_visible()
    print("Login Passed")


def test_invalid_login(sauce_demo: Page) -> None:
    """Verify invalid credentials display an authentication error."""
    login_page = LoginPage(sauce_demo)
    login_page.login("random_user","secret_sauce")
    expect(login_page.get_error_message()).to_be_visible()
    expect(login_page.get_error_message()).to_contain_text("Username and password do not match any user in this service")
    expect(login_page.get_error_button()).to_be_enabled()
    print("Login Failed")

    
def test_locked_out_user(sauce_demo: Page) -> None:
    """Verify a locked-out user is shown the lockout error."""
    login_page = LoginPage(sauce_demo)
    login_page.login("locked_out_user","secret_sauce")
    expect(login_page.get_error_message()).to_be_visible()
    expect(login_page.get_error_message()).to_contain_text("Sorry, this user has been locked out.")
    expect(login_page.get_error_button()).to_be_enabled()
    print("Login Failed with Locked Out User")

def test_empty_user(sauce_demo: Page) -> None:
    """Verify submitting without a password displays a validation error."""
    login_page = LoginPage(sauce_demo)
    login_page.emptyLogin("dummy")
    expect(login_page.get_error_message()).to_be_visible()
    expect(login_page.get_error_message()).to_contain_text("Passwor is required")
    print("Login Failed without password")