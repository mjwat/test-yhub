# Task 028: GitHub Actions GitHub Pages publishing for Allure report on manual main runs

## Goal

Allow GitHub Pages deployment of the latest generated Allure HTML report for both push and manual workflow runs from the `main` branch.

## Scope

- Update `.github/workflows/tests.yml`
- Keep the existing pytest execution behavior unchanged
- Keep the existing `allure-results`, `test-results`, and `allure-report` artifact uploads unchanged
- Allow GitHub Pages publishing for `push` and `workflow_dispatch` runs on `main`
- Switch Allure report generation to standard multi-file HTML output in `allure/report`

## Constraints

- Keep the workflow minimal and maintainable
- Do not add Allure history persistence
- Do not add scheduled runs
- Do not add notifications
- Do not modify unrelated workflow logic

## Publishing strategy

- Continue using the native GitHub Pages Actions flow
- Upload `allure/report` with `actions/upload-pages-artifact`
- Deploy with a dedicated `deploy-pages` job using `actions/deploy-pages`
- Restrict publishing to `main` only because the repository does not use `master`
- Allow publishing on both `push` and `workflow_dispatch`

## Expected result

The existing CI workflow continues to run the same tests and preserve the same downloadable artifacts, while `push` and manual `workflow_dispatch` runs on `main` both publish the latest standard multi-file Allure HTML report to GitHub Pages.

## Implementation update

- Updated the GitHub Pages artifact upload condition to allow `push` and `workflow_dispatch` on `main`
- Updated the `deploy-pages` job condition to allow `push` and `workflow_dispatch` on `main`
- Removed `--single-file` from the Allure generation command so CI publishes the standard multi-file report
- Kept the existing `allure-results`, `test-results`, and `allure-report` artifact uploads unchanged
