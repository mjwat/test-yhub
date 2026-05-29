# Task 027: GitHub Actions GitHub Pages publishing for Allure HTML report

## Goal

Publish the latest generated Allure HTML report from the existing CI workflow to GitHub Pages.

## Scope

- Update `.github/workflows/tests.yml`
- Keep generating the static Allure HTML report in `allure/report`
- Keep the existing `allure-results`, `test-results`, and `allure-report` artifact uploads
- Publish the generated `allure/report` directory to GitHub Pages
- Run deployment only after report generation completes

## Constraints

- Keep the workflow simple and maintainable
- Do not change pytest execution behavior
- Do not change the current report generation command
- Do not add Allure history persistence
- Do not add scheduled runs
- Do not add notifications

## Publishing strategy

- Use the native GitHub Pages Actions flow
- Upload `allure/report` with `actions/upload-pages-artifact`
- Deploy with a dedicated `deploy-pages` job using `actions/deploy-pages`
- Keep the existing test and artifact work inside the current `pytest` job
- Limit publishing to pushes on `main` or `master` so pull requests still validate without deploying

## Required workflow permissions

- `contents: read`
- `pages: write`
- `id-token: write`

## Repository settings

- GitHub Pages must be configured to deploy from GitHub Actions in repository settings

## Expected result

The CI workflow continues to run the same test selection and preserve the same downloadable artifacts, while successful branch pushes also publish the latest static Allure HTML report to GitHub Pages with minimal extra workflow logic.

## Implementation update

- Added a GitHub Pages artifact upload step for `allure/report`
- Added a dedicated `deploy-pages` job that runs after the existing `pytest` job
- Restricted publishing to `push` events on `main` or `master`
- Kept the existing `allure-results`, `test-results`, and `allure-report` artifact uploads unchanged
- Scoped GitHub Pages permissions to the deployment job
- Skipped Pages artifact upload when `allure/report/index.html` is not present
