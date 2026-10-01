import pytest
from playwright.sync_api import Page


@pytest.fixture
def sauce_demo(page: Page) -> Page:
    page.goto("https://www.saucedemo.com/")
    return page