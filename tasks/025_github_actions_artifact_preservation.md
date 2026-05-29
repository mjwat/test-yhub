# Task 025: GitHub Actions artifact preservation for pytest + Playwright CI

## Goal

Preserve useful test artifacts from CI runs so failed workflow executions remain debuggable and ready for future Allure integration work.

## Scope

- Update `.github/workflows/tests.yml`
- Preserve `allure/results` as the primary CI artifact
- Preserve existing test output folders only when they already exist in the current workflow
- Ensure artifact upload still runs when tests fail

## Constraints

- Keep the workflow simple and readable
- Do not change test execution behavior
- Do not change the current screenshot implementation
- Do not introduce a separate screenshot directory
- Do not add new Playwright artifact directories for traces, videos, or screenshots
- Do not add GitHub Pages publishing
- Do not add Allure HTML report publishing
- Do not add scheduled runs
- Do not add notifications

## Artifact strategy

- Upload `allure/results` as the main artifact because failed Playwright screenshots are currently attached directly into Allure results
- Upload existing CI test output only if the workflow already creates it
- Use `if: always()` so artifact upload runs even after test failures
- Keep artifact naming minimal and readable
- Optionally set a short retention window to keep storage lightweight

## Current repository behavior

- The workflow already writes raw Allure results to `allure/results`
- The workflow already writes JUnit XML to `test-results/pytest.xml`
- Playwright failure screenshots are attached directly to Allure from `tests/e2e/conftest.py`
- There is no existing dedicated Playwright screenshot output directory to preserve

## Expected result

The CI workflow continues to run the same pytest selection as before, and failed runs keep their useful raw debugging artifacts available through GitHub Actions downloads without adding reporting or publishing complexity yet.
