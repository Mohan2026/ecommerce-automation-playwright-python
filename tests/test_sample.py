import re
from playwright.sync_api import Page, expect


def test_sample(page: Page) -> None:
    from playwright.sync_api import Page, expect


def test_sample(page: Page) -> None:
    page.goto("https://playwright.dev/")

    expect(
        page.get_by_role("link", name="GitHub repository")
    ).to_be_visible()

    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Discord server").click()

    page1 = page1_info.value
    page1.close()

    page.get_by_role("link", name="Get started").click()

    expect(
        page.get_by_role("button", name="Search (Control+k)")
    ).to_be_visible()

    page.get_by_role("button", name="Search (Control+k)").click()

    page.get_by_role("searchbox", name="Search").fill("assertion")

    page.get_by_role("option", name="Assertions", exact=True) \
        .get_by_role("link").click()

    page.get_by_role("button", name="Copy code to clipboard").first.click()
