# Task 026: GitHub Actions Allure HTML report artifact

## Goal

Generate a downloadable Allure HTML report artifact directly in the existing GitHub Actions workflow from the CI test results.

## Scope

- Update `.github/workflows/tests.yml`
- Keep writing raw Allure results to `allure/results`
- Generate static HTML output in `allure/report`
- Upload the generated HTML report as a GitHub Actions artifact
- Preserve the existing `allure-results` and `test-results` artifacts

## Constraints

- Keep the workflow simple and readable
- Do not change the current pytest selection
- Do not change the existing screenshot attachment behavior
- Do not add GitHub Pages publishing
- Do not add Allure history publishing
- Do not add scheduled runs
- Do not add notifications

## CI report strategy

- Install Java only for Allure CLI usage
- Install the external Allure CLI in the runner
- Generate the report from `allure/results` into `allure/report`
- Use `if: always()` so setup, report generation, and artifact upload still run after test failures
- Skip report generation cleanly when `allure/results` is missing or empty
- Keep artifact naming minimal and readable with `allure-report`

## Expected result

The existing CI workflow continues to run the same pytest smoke selection, preserves raw Allure results and JUnit XML, and additionally uploads a generated static Allure HTML report that can be downloaded and opened locally after the workflow run.
