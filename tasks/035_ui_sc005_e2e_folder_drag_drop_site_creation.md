# 035: YH-UI-SC-005 E2E Implementation Plan (Folder Drag and Drop Upload)

## Task summary
Implement UI scenario `YH-UI-SC-005: Create site from folder via drag and drop` using the existing authenticated E2E flow, API pre-cleanup, a dedicated folder drag-and-drop page-object action, and standard published-site accessibility verification.

## Source-of-truth scenarios (must not be modified)
- `tests/e2e/e2e_test_scenarios.md`

## Clarifications applied
1. Upload flow:
   - This task covers folder upload via drag and drop only.
   - Do not include the Select folder button flow in this task.
   - The Select folder button flow is covered separately by `YH-UI-SC-006`.
2. Test data:
   - Use the existing `data/simple_html_css` directory.
   - Keep the folder path as a local variable in the test body.
3. POM design:
   - Reuse one neutral upload page-object method for upload-based scenarios.
   - Use `create_from_upload(...)` instead of a file-specific or folder-specific method name.
   - Do not force folder upload through `create_from_upload(...)` when the page exposes a dedicated folder input.
   - The current page exposes a separate hidden folder input with `webkitdirectory`/`directory` attributes, so true folder upload should target that input directly.
4. Final site verification:
   - Reuse the standard generated-site accessibility assertion approach already used by HTML/archive flows.
   - No custom-domain or PDF-specific assertion is required.

## Implementation plan

### 1. Add true folder upload support
- [x] Update `tests/e2e/pages/site_create_page.py`:
  - [x] Keep the neutral shared method for non-folder uploads:
    - [x] `create_from_upload(upload_path: str, custom_domain: Optional[str] = None) -> None`
  - [ ] Add a dedicated folder locator for the hidden `input[type='file'][webkitdirectory]`.
  - [ ] Add a dedicated folder upload method:
    - [ ] `create_from_folder(folder_path: str) -> None`
  - [ ] Use the true folder input instead of expanding the directory into individual files.
- [x] Keep shared upload logic encapsulated in the page object.

### 2. Add `YH-UI-SC-005` E2E test
- [x] Extend `tests/e2e/test_site_creation.py` with `YH-UI-SC-005`.
- [x] Use fixtures:
  - [x] `logged_in_admin`
  - [x] `clean_user_sites`
  - [x] `site_create_path`
  - [x] `sites_list_path`
- [x] Keep the folder path as a local variable in the test body:
  - [x] Resolve `data/simple_html_css` inside the test without adding a shared fixture.
- [x] Flow assertions:
  - [x] Open the site creation page.
  - [x] Drag and drop the test folder into the upload area.
  - [x] Click submit button.
  - [x] Verify that the sites list page is opened.
  - [x] Verify the first site appears with create/in-progress status.
  - [x] Wait until the site status becomes published/active.
  - [x] Open the generated site URL in a new tab.
  - [x] Verify the created site is accessible.

### 3. Reliability and diagnostics
- [x] Prefer Playwright waits and expectations over fixed sleeps.
- [x] Keep the test independent through API pre-cleanup.
- [x] Preserve clear assertion messages for folder existence and business checkpoints.
- [x] Reuse the existing Allure step style where it improves readability.

### 4. Validation
- [x] Run collection for `tests/e2e/test_site_creation.py`.
- [ ] Run the targeted `YH-UI-SC-005` E2E scenario if the local environment supports it.

## Deliverables
- `tasks/035_ui_sc005_e2e_folder_drag_drop_site_creation.md`
- Updated `tests/e2e/pages/site_create_page.py`
- Updated `tests/e2e/test_site_creation.py`
