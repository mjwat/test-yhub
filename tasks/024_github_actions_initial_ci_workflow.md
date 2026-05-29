# Task 024: Initial GitHub Actions workflow for pytest + Playwright

## Goal

Introduce the first minimal and stable GitHub Actions workflow for this project so tests can run remotely in CI.

## Scope

- Add `.github/workflows/tests.yml`
- Support manual execution from the GitHub UI
- Support automatic execution on push and pull request
- Install Python dependencies from `requirements.txt`
- Install Playwright browser binaries and Linux dependencies
- Run a conservative default pytest selection
- Upload useful CI artifacts

## Constraints

- Keep the workflow simple and readable
- Do not add GitHub Pages publishing
- Do not add Allure history publishing
- Do not add scheduled runs
- Do not add notifications
- Do not add deployment logic

## CI strategy

- Use `ubuntu-latest`
- Use `actions/setup-python` with pip cache enabled
- Install only Chromium for Playwright in CI
- Export required runtime variables from GitHub Actions secrets
- Write Allure raw results to `allure/results`
- Write JUnit XML to `test-results/pytest.xml`

## Default test selection

Run only the authentication smoke coverage by default:

- `tests/api/test_auth_login.py`
- `tests/e2e/test_auth.py`

Reason:

- The current suite does not yet define dedicated `manual` or `destructive` markers in `pytest.ini`
- Site creation coverage currently performs remote create/delete flows and should not be part of the first default CI lane

## Required GitHub secrets

- `BASE_URL`
- `ADMIN_BASE_URL`
- `TEST_USER_EMAIL`
- `TEST_USER_PASSWORD`
- `GIT_REP_URL`

## Expected result

A first CI workflow exists and can be triggered manually or on code changes, installs the required Python and Playwright dependencies on Linux, runs a stable smoke subset, and preserves useful artifacts for debugging.
