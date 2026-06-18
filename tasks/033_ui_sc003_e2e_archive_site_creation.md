# 033: YH-UI-SC-003 E2E Implementation Plan (Archive Upload)

## Task summary
Implement UI scenario `YH-UI-SC-003: Create site from archive` using the existing authenticated E2E flow, API pre-cleanup, shared upload-form page-object actions, and post-create published-site accessibility validation.

## Source-of-truth scenarios (must not be modified)
- `tests/e2e/e2e_test_scenarios.md`

## Clarifications applied
1. Upload form behavior:
   - Archive upload uses the same default form as single-file upload.
   - No additional tab switch or archive-specific form selection is required.
2. Page-object design:
   - Reuse the existing upload flow by replacing the single-purpose file-upload method with a generic uploaded-file method.
   - Keep `custom_domain` optional so the same method supports:
     - `YH-UI-SC-002` with domain
     - `YH-UI-SC-003` without domain
3. Test data:
   - Use the existing `data/archive.zip` file.
   - Keep the archive path as a local variable in the test body.

## Implementation plan

### 1. Refactor shared upload action
- [x] Update `tests/e2e/pages/site_create_page.py`:
  - [x] Replace the scenario-specific uploaded-file method with a generic method.
  - [x] Proposed shape:
    - [x] `create_from_uploaded_file(file_path: str, custom_domain: Optional[str] = None) -> None`
  - [x] Only fill the domain input when `custom_domain` is provided.
  - [x] Reuse the existing file input and create button logic.
- [x] Update the existing `YH-UI-SC-002` test to use the new shared method.

### 2. Add archive E2E test
- [x] Extend `tests/e2e/test_site_creation.py` with `YH-UI-SC-003`.
- [x] Use fixtures:
  - [x] `logged_in_admin`
  - [x] `clean_user_sites`
  - [x] `site_create_path`
  - [x] `sites_list_path`
- [x] Keep the archive path as a local variable in the test body:
  - [x] Resolve `data/archive.zip` inside the test without adding a shared fixture.
- [x] Flow assertions:
  - [x] Open the site creation page.
  - [x] Upload the zip file.
  - [x] Click submit through the shared upload action.
  - [x] Verify the sites list page is opened.
  - [x] Verify the first site appears with create/in-progress status.
  - [x] Wait until the site status becomes published/active.
  - [x] Open the generated site URL in a new tab.
  - [x] Verify the created site is accessible.

### 3. Reliability and diagnostics
- [x] Prefer Playwright waits and expectations over fixed sleeps.
- [x] Keep the test independent through API pre-cleanup.
- [x] Preserve clear assertion messages for archive file existence and business checkpoints.
- [x] Reuse the existing Allure step style where it improves readability.

### 4. Validation
- [x] Run collection for `tests/e2e/test_site_creation.py`.
- [ ] Run the targeted `YH-UI-SC-003` E2E scenario if the local environment supports it.

## Deliverables
- `tasks/033_ui_sc003_e2e_archive_site_creation.md`
- Updated `tests/e2e/pages/site_create_page.py`
- Updated `tests/e2e/test_site_creation.py`
