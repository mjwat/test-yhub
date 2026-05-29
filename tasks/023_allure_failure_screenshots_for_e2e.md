# 023: Allure Failure Screenshots for E2E Tests

## Task summary
Automatically capture and attach Playwright screenshots to Allure reports for failed E2E tests only.

## Scope
- Use a centralized pytest hook-based approach
- Limit the behavior to Playwright E2E tests
- Attach screenshots to Allure only for failed tests
- Ignore tests without a Playwright `page` fixture safely
- Keep existing Allure steps, history, and categories behavior unchanged
- Do not add videos, traces, or CI changes

## Repository findings
- The Playwright `page` fixture is provided by `pytest-playwright`
- E2E-specific Playwright configuration lives in `tests/e2e/conftest.py`
- Shared authenticated UI setup lives in `tests/fixtures/auth.py`
- There is no existing shared failure screenshot or attachment hook

## Implementation plan
- Add `pytest_runtest_makereport` in `tests/e2e/conftest.py` to persist test phase results on the item
- Add an E2E `autouse` fixture that runs after each test and checks whether `setup` or `call` failed
- If a failure occurred and a Playwright `page` fixture is available, capture screenshot bytes and attach them to Allure as PNG
- Skip attachment safely when no `page` fixture exists or the page is no longer available

## Deliverables
- `tasks/023_allure_failure_screenshots_for_e2e.md`
- `tests/e2e/conftest.py`

## Implementation status
- [x] Added the task document
- [x] Added centralized failed-test report tracking for E2E pytest items
- [x] Added automatic Allure screenshot attachment for failed Playwright page-based tests
- [x] Ignored tests without a Playwright `page` fixture safely
- [x] Validate pytest collection
- [x] Updated screenshot teardown ordering so attachments can be captured before the page closes
- [x] Moved screenshot attachment into the pytest report hook so Allure records it on the failed test result
