# Task 029: GitHub Actions Allure history persistence for GitHub Pages

## Goal

Persist Allure trend/history data between CI runs while keeping the existing GitHub Actions artifact uploads and GitHub Pages deployment flow unchanged.

## Scope

- Update `.github/workflows/tests.yml`
- Restore the previously published Allure report history before generating the next report
- Copy prior `history/` into `allure/results/history` when it exists
- Keep the existing `allure-results`, `test-results`, `allure-report`, and GitHub Pages artifact uploads
- Keep GitHub Pages deployment based on `actions/upload-pages-artifact` and `actions/deploy-pages`

## Constraints

- Keep the workflow minimal and readable
- Do not change pytest execution behavior
- Do not add scheduled runs
- Do not add notifications
- Keep report generation and Pages deployment eligible to run even when tests fail
- Handle the first run safely when no previous history exists

## Restore strategy

- Keep the current GitHub Pages artifact flow unchanged
- Download previous Allure history files from the published GitHub Pages report before report generation
- Restore the known `history/*.json` files into `allure/results/history` when they exist
- Generate the new report normally so Allure updates trend files into `allure/report/history`

## Expected result

The workflow continues to publish the latest Allure report to GitHub Pages, and trend/history widgets persist across runs whenever a prior retained `allure-report` artifact exists.

## Implementation status

- [x] Added this task document
- [x] Restore the previous `allure-report` artifact before report generation
- [x] Copy previous `history/` into `allure/results/history` when present
- [x] Keep the current Pages upload and deploy flow unchanged
- [x] Keep the workflow safe when no prior history exists
- [x] Verify the workflow file changes for readability and correctness

## Implementation update

- Restored Allure history directly from the published GitHub Pages site with `curl`
- Limited history restore to `main` push and manual `workflow_dispatch` runs
- Downloaded the known Allure history JSON files into `allure/results/history` only when they exist
- Kept the restore safe for first-run and missing-history cases by allowing missing files
- Left pytest execution, Allure generation, artifact uploads, and GitHub Pages deployment flow unchanged
