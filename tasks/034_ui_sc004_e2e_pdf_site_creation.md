# 034: YH-UI-SC-004 E2E Implementation Plan (PDF Upload)

## Task summary
Implement UI scenario `YH-UI-SC-004: Create site with pdf` using the existing authenticated E2E flow, API pre-cleanup, shared uploaded-file page-object action, and a lightweight generated-site availability assertion that does not assume a specific PDF rendering mode.

## Source-of-truth scenarios (must not be modified)
- `tests/e2e/e2e_test_scenarios.md`

## Clarifications applied
1. Upload flow:
   - Reuse the existing shared upload-form action for uploaded files.
   - No PDF-specific form mode or tab switch is assumed.
2. Test data:
   - Use the existing `data/sample.pdf` file.
   - Keep the PDF path as a local variable in the test body.
3. Generated-site verification:
   - Use the minimal availability strategy for the opened generated site.
   - Do not assume whether the generated result is:
     - a browser-rendered PDF document
     - or a normal HTML page that embeds or links the PDF
4. Accessibility assertion scope:
   - Validate that the generated site opens successfully in a new tab.
   - Validate an `http/https` URL and loaded page state only.
   - Do not add PDF-specific content assertions in this task.

## Implementation plan

### 1. Reuse shared upload action
- [x] Keep using `tests/e2e/pages/site_create_page.py` shared method:
  - [x] `create_from_uploaded_file(...)`
- [x] Do not introduce a PDF-specific page-object method unless the real UI later requires one.

### 2. Add PDF E2E test
- [x] Extend `tests/e2e/test_site_creation.py` with `YH-UI-SC-004`.
- [x] Use fixtures:
  - [x] `logged_in_admin`
  - [x] `clean_user_sites`
  - [x] `site_create_path`
  - [x] `sites_list_path`
- [x] Keep the PDF path as a local variable in the test body:
  - [x] Resolve `data/sample.pdf` inside the test without adding a shared fixture.
- [x] Flow assertions:
  - [x] Open the site creation page.
  - [x] Upload the PDF file.
  - [x] Click submit through the shared upload action.
  - [x] Verify the sites list page is opened.
  - [x] Verify the first site appears with create/in-progress status.
  - [x] Wait until the site status becomes published/active.
  - [x] Open the generated site URL in a new tab.
  - [x] Verify the generated site is available using a minimal popup accessibility check.

### 3. Reliability and diagnostics
- [x] Prefer Playwright waits and expectations over fixed sleeps.
- [x] Keep the test independent through API pre-cleanup.
- [x] Preserve clear assertion messages for PDF file existence and business checkpoints.
- [x] Reuse the existing Allure step style where it improves readability.

### 4. Validation
- [x] Run collection for `tests/e2e/test_site_creation.py`.
- [ ] Run the targeted `YH-UI-SC-004` E2E scenario if the local environment supports it.

## Deliverables
- `tasks/034_ui_sc004_e2e_pdf_site_creation.md`
- Updated `tests/e2e/test_site_creation.py`
