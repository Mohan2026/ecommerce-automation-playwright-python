from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from utils.csv_reader import load_csv

# Load test data from CSV
login_data = load_csv("test_data/saucedemo_login.csv")


def get_test_data(test_id):
    """Retrieve a specific test scenario from CSV."""
    for row in login_data:
        if row["test_id"] == test_id:
            return row

    raise ValueError(f"Test data not found: {test_id}")

def test_valid_login(sauce_demo: Page) -> None:
    """Verify a valid user can log in successfully."""
    data = get_test_data("TC_LOGIN_001")    
    login_page = LoginPage(sauce_demo)
    login_page.login(data["username"], data["password"])
    expect(sauce_demo).to_have_url("https://www.saucedemo.com/inventory.html")
    #expect(sauce_demo.get_by_text("Swag Labs")).to_be_visible()
    print("Login Passed")


def test_invalid_login(sauce_demo: Page) -> None:
    """Verify invalid credentials display an authentication error."""
    data = get_test_data("TC_LOGIN_002")
    login_page = LoginPage(sauce_demo)
    login_page.login(data["username"], data["password"])
    expect(login_page.get_error_message()).to_be_visible()
    expect(login_page.get_error_message()).to_contain_text("Username and password do not match any user in this service")
    expect(login_page.get_error_button()).to_be_enabled()
    print("Login Failed")

    
def test_locked_out_user(sauce_demo: Page) -> None:
    """Verify a locked-out user is shown the lockout error."""
    data = get_test_data("TC_LOGIN_003")
    login_page = LoginPage(sauce_demo)
    login_page.login(data["username"], data["password"])
    expect(login_page.get_error_message()).to_be_visible()
    expect(login_page.get_error_message()).to_contain_text("Sorry, this user has been locked out.")
    expect(login_page.get_error_button()).to_be_enabled()
    print("Login Failed with Locked Out User")

def test_empty_user(sauce_demo: Page) -> None:
    """Verify submitting without a password displays a validation error."""
    data = get_test_data("TC_LOGIN_006")
    login_page = LoginPage(sauce_demo)
    login_page.emptyLogin(data["username"])
    expect(login_page.get_error_message()).to_be_visible()
    expect(login_page.get_error_message()).to_contain_text("Password is required")
    print("Login Failed without password")







