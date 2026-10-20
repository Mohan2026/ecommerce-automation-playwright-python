
import pytest
import subprocess
import sys
import os
import time
from pathlib import Path
from playwright.sync_api import Page
from datetime import datetime
from ai_analyzer.failure_writer import save_failure_data

ARTIFACTS_DIR = Path("artifacts")


# To maximize browser (incomplete)
def pytest_addoption(parser):
    parser.addoption(
        "--maximize",
        action="store_true",
        default=False,
        help="Maximize the browser window"
    )
    parser.addoption(
        "--ai-analyze",
        action="store_true",
        default=False,
        help="Analyze test failures using AI"
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

    # Save failure details for failed setup, call, or teardown phases.
    if report.failed:
        error_type = type(call.excinfo.value).__name__ if call.excinfo else "Unknown"

        failure_path = save_failure_data(
            test_name=item.name,
            phase=report.when,
            error_message=str(report.longrepr),
            traceback_text=str(report.longrepr),
        )

        # Update the JSON with the actual exception type.
        import json

        failure_data = json.loads(failure_path.read_text(encoding="utf-8"))
        failure_data["error_type"] = error_type
        failure_path.write_text(
            json.dumps(failure_data, indent=2),
            encoding="utf-8",
        )

        print(f"\nFailure data saved: {failure_path}")

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

def pytest_sessionstart(session):
    session.config._ai_analysis_start_time = time.time()


def pytest_sessionfinish(session, exitstatus):
    if not session.config.getoption("--ai-analyze"):
        return

    project_root = Path(__file__).resolve().parent.parent
    failures_dir = project_root / "artifacts" / "failures"

    if not failures_dir.exists():
        print("\nNo failure data directory found.")
        return

    start_time = session.config._ai_analysis_start_time

    failure_files = sorted(
        [
            path
            for path in failures_dir.glob("*.json")
            if path.stat().st_mtime >= start_time
        ],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    if not failure_files:
        print("\nNo new failure JSON files found in this test run.")
        return

    print("\nAI analysis option enabled.")
    print(
        f"Found {len(failure_files)} failure JSON file(s) "
        "from this test run."
    )

    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        str(project_root)
        + (os.pathsep + existing_pythonpath if existing_pythonpath else "")
    )

    for failure_file in failure_files:
        print(f"\nAnalyzing failure: {failure_file.name}")

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ai_analyzer.analyze_failure",
                "--file",
                str(failure_file.resolve()),
            ],
            cwd=project_root,
            env=env,
            check=False,
        )

        if result.returncode != 0:
            print(
                f"AI analysis failed for {failure_file.name}. "
                "Check the error above."
            )

        