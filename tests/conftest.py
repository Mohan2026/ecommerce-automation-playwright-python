
import pytest
from pathlib import Path
from playwright.sync_api import Page
from datetime import datetime


ARTIFACTS_DIR = Path("artifacts")


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
    }


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Store each test phase's result for fixtures to inspect.
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def capture_failure_evidence(request, page: Page):
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    # Start tracing before the test executes.
    page.context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )

    yield

    test_name = request.node.name
    report = getattr(request.node, "rep_call", None)

    if report and report.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        screenshot_path = ARTIFACTS_DIR / f"{test_name}-{timestamp}-failure.png"
        trace_path = ARTIFACTS_DIR / f"{test_name}-{timestamp}-trace.zip"

        page.screenshot(
            path=str(screenshot_path),
            full_page=True,
        )

        page.context.tracing.stop(path=str(trace_path))
    else:
        page.context.tracing.stop()
