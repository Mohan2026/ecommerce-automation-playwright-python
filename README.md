# E-Commerce Automation Framework

UI automation framework built with **Python, Playwright, and pytest**, using SauceDemo as the application under test. The framework demonstrates modern SDET practices, including Page Object Model (POM), cross-browser testing, containerized test execution, and CI automation with GitHub Actions.

## Tech Stack

* Python
* Playwright
* pytest
* pytest-playwright
* pytest-xdist for parallel test execution
* Page Object Model (POM)
* Docker
* Docker Compose
* GitHub Actions
* GitHub Copilot for AI-assisted test development
* pytest-html for test reporting

## Current Coverage

* Login scenarios, including valid and invalid credentials
* Product selection and validation
* Add-to-cart functionality
* Cart validation
* Checkout workflow
* Order placement and confirmation
* Price, subtotal, tax, and total validation
* Cross-browser testing with Chromium, Firefox, and WebKit
* Parallel test execution using pytest-xdist
* Failure screenshots and Playwright trace evidence
* Timestamped failure artifacts for easier debugging
* HTML test reports with self-contained output

## Project Structure

```text
ecommerce-automation-playwright-python/
├── .github/
│   └── workflows/
│       └── playwright-tests.yml
├── pages/
│   ├── __init__.py
│   └── login_page.py
├── tests/
│   └── sauce_demo/
│       ├── test_login.py
│       └── test_orders.py
├── artifacts/
├── conftest.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .gitignore
└── README.md
```

## Run Tests

Install dependencies:

```bash
python -m pip install -r requirements.txt
python -m playwright install
```

Run all tests:

```bash
python -m pytest -v
```

Run tests in a headed browser:

```bash
python -m pytest --headed
```

Run tests with slow motion:

```bash
python -m pytest --headed --slowmo 1000
```

Run tests on a specific browser:

```bash
python -m pytest --browser chromium
```

Run tests across all three browsers:

```bash
python -m pytest --browser chromium --browser firefox --browser webkit
```

Run cross-browser tests in parallel:

```bash
python -m pytest --browser chromium --browser firefox --browser webkit -n 3 -v
```

## Docker & Docker Compose

Build the Docker image:

```bash
docker build -t playwright-automation .
```

Run the test suite inside Docker:

```bash
docker run --rm playwright-automation
```

Run cross-browser tests using Docker Compose:

```bash
docker compose run --build --rm playwright-tests
```

The Docker environment provides a consistent test execution environment with browser dependencies aligned to the installed Playwright version.

## Test Reporting & Failure Evidence

* Generate HTML test reports using pytest-html.
* Save failure screenshots and Playwright trace files for troubleshooting.
* Use timestamped artifacts to help identify and investigate failed tests.
* Store generated reports and evidence in the local `artifacts/` directory when configured.
* Upload test reports and failure evidence from GitHub Actions as workflow artifacts.

## CI/CD Integration

GitHub Actions is configured to run the automation suite on pushes and pull requests targeting the `main` branch.

The Docker-based workflow:

* Checks out the repository.
* Verifies Docker and Docker Compose.
* Builds the test image and runs the suite in Docker.
* Executes the configured cross-browser and parallel tests.
* Uploads test reports and failure evidence, including when tests fail.

## AI-Assisted Test Development

* Use GitHub Copilot to assist with test scaffolding, test data generation, and code suggestions.
* Review and validate AI-generated code before incorporating it into the framework.
* Use test failures, screenshots, and traces to support debugging and root-cause analysis.

## Future Enhancements

* Expand Page Object Model and reusable component abstractions.
* Add API automation and UI/API integration testing.
* Improve test data management and environment configuration.
* Enhance reporting and failure diagnostics.
* Explore cloud-based test execution and Kubernetes fundamentals.
* Develop controlled AI-assisted workflows for test generation and failure analysis.

This project is being continuously enhanced to demonstrate modern **SDET / QA automation framework practices**, with an emphasis on maintainability, cross-browser coverage, containerization, CI/CD, and AI-assisted development.
