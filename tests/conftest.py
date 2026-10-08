import pytest
from playwright.sync_api import Page

import pytest
from playwright.sync_api import Page

# To maximize browser (incomplete)
def pytest_addoption(parser):
    parser.addoption(
        "--maximize",
        action="store_true",
        default=False,
        help="Maximize the browser window"
    )


@pytest.fixture
def maximize(request):
    return request.config.getoption("--maximize")

@pytest.fixture
def sauce_demo(page: Page) -> Page:
    page.goto("https://www.saucedemo.com/")
    return page

@pytest.fixture
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
         "viewport": None,
        #"viewport": {"width": 1920, "height": 1080},
    }

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")

        if page:
            page.screenshot(
                path=f"test-results/{item.name}-failure.png",
                full_page=True
            )