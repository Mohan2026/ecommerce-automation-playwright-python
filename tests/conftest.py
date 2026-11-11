import json
import os
import subprocess
import sys
import time
from datetime import datetime
from html import escape
from pathlib import Path

import pytest
from playwright.sync_api import Page
from ai_analyzer.failure_writer import save_failure_data

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"


def pytest_addoption(parser):
    parser.addoption(
        "--maximize",
        action="store_true",
        default=False,
        help="Maximize the browser window",
    )
    parser.addoption(
        "--ai-analyze",
        action="store_true",
        default=False,
        help="Analyze test failures using AI",
    )

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from utils.csv_reader import load_csv


@pytest.fixture
def logged_in_sauce_demo(sauce_demo: Page) -> Page:
    login_data = load_csv("test_data/saucedemo_login.csv")

    credentials = next(
        row for row in login_data
        if row["test_id"] == "TC_LOGIN_001"
    )

    login_page = LoginPage(sauce_demo)
    login_page.login(
        credentials["username"],
        credentials["password"]
    )

    expect(sauce_demo).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    return sauce_demo

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

    setattr(item, f"rep_{report.when}", report)

    if report.failed:
        error_type = (
            type(call.excinfo.value).__name__
            if call.excinfo
            else "Unknown"
        )

        failure_path = save_failure_data(
            test_name=item.name,
            phase=report.when,
            error_message=str(report.longrepr),
            traceback_text=str(report.longrepr),
        )

        failure_data = json.loads(
            failure_path.read_text(encoding="utf-8")
        )
        failure_data["error_type"] = error_type

        failure_path.write_text(
            json.dumps(failure_data, indent=2),
            encoding="utf-8",
        )

        print(f"\nFailure data saved: {failure_path}")


@pytest.fixture(autouse=True)
def capture_failure_evidence(request, page: Page):
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

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

        screenshot_path = (
            ARTIFACTS_DIR / f"{test_name}-{timestamp}-failure.png"
        )
        trace_path = (
            ARTIFACTS_DIR / f"{test_name}-{timestamp}-trace.zip"
        )

        page.screenshot(
            path=str(screenshot_path),
            full_page=True,
        )

        page.context.tracing.stop(path=str(trace_path))
    else:
        page.context.tracing.stop()


def pytest_sessionstart(session):
    if not hasattr(session.config, "workerinput"):
        session.config._ai_analysis_start_time = time.time()


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    config = session.config

    # AI analysis must run only in the main pytest process.
    if hasattr(config, "workerinput"):
        return

    if not config.getoption("--ai-analyze"):
        return

    failures_dir = ARTIFACTS_DIR / "failures"

    if not failures_dir.exists():
        print("\nNo failure data directory found.")
        return

    start_time = config._ai_analysis_start_time

    failure_files = sorted(
        [
            path
            for path in failures_dir.glob("*.json")
            if path.stat().st_mtime >= start_time
        ],
        key=lambda path: path.stat().st_mtime,
    )

    if not failure_files:
        print("\nNo new failure JSON files found.")
        return

    print(f"\nAnalyzing {len(failure_files)} failure(s)...")

    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")

    env["PYTHONPATH"] = (
        str(PROJECT_ROOT)
        + (
            os.pathsep + existing_pythonpath
            if existing_pythonpath
            else ""
        )
    )

    analysis_files = []

    for failure_file in failure_files:
        print(f"\nAnalyzing: {failure_file.name}")

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ai_analyzer.analyze_failure",
                "--file",
                str(failure_file.resolve()),
            ],
            cwd=PROJECT_ROOT,
            env=env,
            check=False,
        )

        if result.returncode == 0:
            analysis_file = (
                ARTIFACTS_DIR
                / "ai-analysis"
                / f"{failure_file.stem}-analysis.json"
            )

            if analysis_file.exists():
                analysis_files.append(analysis_file)
        else:
            print(f"AI analysis failed: {failure_file.name}")

    config._ai_analysis_files = analysis_files


def pytest_html_results_summary(prefix, summary, postfix):
    from markupsafe import Markup

    config = getattr(pytest_html_results_summary, "_config", None)

    if config is None:
        return

    analysis_files = getattr(config, "_ai_analysis_files", [])

    if not analysis_files:
        return

    sections = [
        "<div style='padding:15px;margin:15px 0;"
        "background:#f8f9fa;border:1px solid #ddd;"
        "border-radius:8px;color:#222;'>",
        "<h2 style='color:#222;'>AI Failure Analysis Summary</h2>",
    ]

    for analysis_file in analysis_files:
        try:
            data = json.loads(
                analysis_file.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError):
            continue

        category = data.get("failure_category", "unknown")
        category_label = category.replace("_", " ").title()

        sections.append(
            "<div style='margin-bottom:15px;color:#222;'>"
            f"<h3 style='color:#222;'>{escape(analysis_file.stem)}</h3>"
            f"<p><strong>Category:</strong> {escape(category_label)}</p>"
            f"<p><strong>Summary:</strong> "
            f"{escape(data.get('failure_summary', ''))}</p>"
            "</div>"
        )

    sections.append("</div>")

    postfix.append(Markup("".join(sections)))

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    pytest_html_results_summary._config = config