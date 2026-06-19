# 036: YH-UI-SC-007 E2E Implementation Plan (Code Editor Default Project)

## Task summary
Implement UI scenario `YH-UI-SC-007: Create site by code editor` using the existing authenticated E2E flow, API pre-cleanup, a dedicated editor-tab page-object action, and standard published-site accessibility verification.

## Source-of-truth scenarios (must not be modified)
- `tests/e2e/e2e_test_scenarios.md`

## Clarifications applied
1. Editor behavior:
   - The Editor tab is pre-populated with a valid default project.
   - This task covers creating a site from the default editor state only.
   - Do not add custom code editing interactions in this task.
2. Test scope:
   - The business goal is to verify that site creation succeeds from editor mode.
   - Treat this as an editor-mode smoke flow, not a content-editing scenario.
3. Final site verification:
   - Reuse the standard generated-site accessibility assertion approach already used by the existing HTML/archive flows.

## Implementation plan

### 1. Add editor-tab page-object action
- [x] Update `tests/e2e/pages/site_create_page.py`:
  - [x] Add locator for the Editor tab/button.
  - [x] Add dedicated method for site creation from editor mode.
  - [x] Proposed shape:
    - [x] `create_from_editor() -> None`
  - [x] The method should:
    - [x] select the Editor tab
    - [x] reuse the existing create button
- [x] Keep editor-tab interaction encapsulated in the page object.

### 2. Add `YH-UI-SC-007` E2E test
- [x] Extend `tests/e2e/test_site_creation.py` with `YH-UI-SC-007`.
- [x] Use fixtures:
  - [x] `logged_in_admin`
  - [x] `clean_user_sites`
  - [x] `site_create_path`
  - [x] `sites_list_path`
- [x] Flow assertions:
  - [x] Open the site creation page.
  - [x] Select the Editor tab.
  - [x] Click submit through the editor page-object action.
  - [x] Verify that the sites list page is opened.
  - [x] Verify the first site appears with create/in-progress status.
  - [x] Wait until the site status becomes published/active.
  - [x] Open the generated site URL in a new tab.
  - [x] Verify the created site is accessible.

### 3. Reliability and diagnostics
- [x] Prefer Playwright waits and expectations over fixed sleeps.
- [x] Keep the test independent through API pre-cleanup.
- [x] Preserve clear assertion messages for editor-mode business checkpoints.
- [x] Reuse the existing Allure step style where it improves readability.

### 4. Validation
- [x] Run collection for `tests/e2e/test_site_creation.py`.
- [ ] Run the targeted `YH-UI-SC-007` E2E scenario if the local environment supports it.

## Deliverables
- `tasks/036_ui_sc007_e2e_code_editor_site_creation.md`
- Updated `tests/e2e/pages/site_create_page.py`
- Updated `tests/e2e/test_site_creation.py`
