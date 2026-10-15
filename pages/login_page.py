from playwright.sync_api import Page


class LoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("[data-test='username']")
        self.password = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")

    def login(self, username, password):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    def emptyLogin(self,username):
         self.username.fill(username)
         self.login_button.click()