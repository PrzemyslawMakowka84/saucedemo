# Swag Labs

## Introduction

This project is a test automation framework for [SauceDemo](https://www.saucedemo.com/) built using Python and Playwright.

The main goal of this framework is to cover as many test scenarios as possible, including both positive and negative cases.

The framework is designed based on the Page Object Model (POM) to ensure maintainability, readability, and scalability, following industry best practices.

Tests are designed to be stable and reliable, with a focus on minimizing flakiness.

The project demonstrates a clean test architecture and can serve as a reference for building modern E2E test automation frameworks.

The project is actively developed and continuously improved with new test cases, features, and best practices.

This project reflects my approach to test automation: clean architecture, reliability, and long-term maintainability over quick solutions.

---

## What this project demonstrates

- Designing a scalable test automation framework from scratch
- Applying Page Object Model (POM) in real-world scenarios
- Writing stable and maintainable E2E tests using Playwright
- Handling test data and environment configuration securely
- Implementing parallel test execution for faster feedback
- Using Allure for clear and structured reporting

---

## Test Coverage

The framework includes automated tests for:

- Login functionality with valid and invalid users
- Locked user scenarios
- Error message validation
- Navigation and UI elements verification
- Basic inventory interactions

---

## Architecture

The project is structured using the Page Object Model (POM):

- `pom/` – page classes with locators and actions
- `tests/` – test cases
- `conftest.py` – shared fixtures and configuration
- `tools/` – helper methods and utilities

This structure ensures separation of concerns and improves maintainability.

---

## Configuration

This project uses environment variables to manage sensitive data such as credentials.

1. Copy the example file:

```bash
cp .env_example .env
```

2. Fill in your own values in the `.env` file.

The `.env` file is not committed to the repository for security reasons.

---

## Installation

1. Install the required Python packages:

```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:

```bash
playwright install
```

---

## Run tests

To execute all tests:

```bash
pytest
```

To run tests in parallel:

```bash
pytest -n auto
```

---

## Reporting

Test results are automatically saved to the `allure-results` directory.

To view reports locally, make sure Allure Commandline is installed:
https://allurereport.org/docs/install/

Generate and open the report with:

```bash
allure serve allure-results
```

---

## Tech Stack

- Python
- Playwright
- Pytest
- Allure Report
- pytest-xdist

---

## Future Improvements

- CI/CD integration (e.g. GitHub Actions)
- Test execution in Docker environment
- Visual regression testing
- API test integration
- Test data management improvements

---

## Notes

- The framework follows the Page Object Model (POM) design pattern
- Environment variables are used to keep sensitive data secure
- The project is designed with scalability and maintainability in mind
- The framework is under continuous development and regularly extended with new functionalities