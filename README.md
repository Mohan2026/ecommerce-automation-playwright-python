# E-Commerce Automation Framework

UI automation framework built with **Python, Playwright, and pytest**, using SauceDemo as the application under test.

## Tech Stack

* Python
* Playwright
* pytest
* GitHub

## Current Coverage

* Login scenarios
* Product selection
* Add to cart
* Cart validation
* Checkout
* Order placement
* Price and total validation
* Failure screenshots

## Project Structure

```text
ecommerce-automation-playwright-python/
├── pages/
├── tests/
│   ├── conftest.py
│   └── sauce_demo/
├── test-results/
├── requirements.txt
└── README.md
```

## Run Tests

```bash
pytest
```

Run with browser:

```bash
pytest --headed
```

Run with slow motion:

```bash
pytest --headed --slowmo 1000
```

This project is being continuously enhanced to demonstrate modern **SDET / QA automation framework practices**.
