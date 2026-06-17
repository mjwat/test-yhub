# 032: YH-UI-SC-002 E2E Implementation Plan (Single File + Custom Domain)

## Task summary
Implement UI scenario `YH-UI-SC-002: Create site from single file and with custom domain` using the existing authenticated E2E flow, Page Object Model, API pre-cleanup, file upload support, and post-create domain verification on the sites list.

## Source-of-truth scenarios (must not be modified)
- `tests/e2e/e2e_test_scenarios.md`

## Clarifications applied
1. Custom domain test data:
   - Keep the domain value as a local constant inside the test.
   - Use `my-test-domain` for this scenario.
2. Site creation form behavior:
   - Domain input is visible on the default single-file upload form.
   - No tab switch is required before uploading the file.
3. Post-create domain assertion:
   - The created domain is visible as plain text in the site row.
4. File source:
   - Use the existing `data/index.html` file as the uploaded artifact.

## Implementation plan

### 1. Test data wiring
- [x] Keep the custom domain value as a local constant in the test body:
  - [x] `custom_domain = "my-test-domain"`
- [x] Keep the upload file path as a local variable in the test body:
  - [x] Resolve `data/index.html` inside the test without adding a shared fixture.

### 2. POM updates for single-file creation
- [x] Extend `tests/e2e/pages/site_create_page.py`:
  - [x] Add locator for the custom domain input.
  - [x] Add locator for the single-file upload input.
  - [x] Keep the existing create button reuse intact.
  - [x] Add method to create a site from a single file with custom domain.
- [x] Keep actions encapsulated in page-object methods only.

### 3. POM updates for sites list assertions
- [x] Extend `tests/e2e/pages/sites_page.py`:
  - [x] Add assertion helper to verify the first created site row contains the expected custom domain text.
  - [x] Reuse existing list-page, status, and popup helpers where possible.

### 4. Test implementation
- [x] Extend `tests/e2e/test_site_creation.py` with `YH-UI-SC-002`.
- [x] Use fixtures:
  - [x] `logged_in_admin`
  - [x] `clean_user_sites`
  - [x] `site_create_path`
  - [x] `sites_list_path`
- [x] Flow assertions:
  - [x] Open the site creation page.
  - [x] Enter the custom domain.
  - [x] Upload the HTML file.
  - [x] Click submit.
  - [x] Verify the sites list page is opened.
  - [x] Verify the first site appears with create/in-progress status.
  - [x] Wait until the site status becomes published/active.
  - [x] Verify the created site row contains `my-test-domain`.
  - [x] Open the generated site URL in a new tab.
  - [x] Verify the created site is accessible.

### 5. Reliability and diagnostics
- [x] Prefer Playwright waits and expectations over fixed sleeps.
- [x] Keep the test independent through API pre-cleanup.
- [x] Preserve clear assertion messages for business checkpoints.
- [x] Reuse existing Allure step style where it improves readability.

### 6. Validation
- [x] Run collection for `tests/e2e/test_site_creation.py`.
- [ ] Run the targeted `YH-UI-SC-002` E2E scenario if the local environment supports it.

## Deliverables
- `tasks/032_ui_sc002_e2e_file_site_creation_custom_domain.md`
- Updated `tests/e2e/pages/site_create_page.py`
- Updated `tests/e2e/pages/sites_page.py`
- Updated `tests/e2e/test_site_creation.py`
