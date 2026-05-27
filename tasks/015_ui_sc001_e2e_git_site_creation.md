# 015: YH-UI-SC-001 E2E Implementation Plan (Git Site Creation)

## Task summary
Implement UI scenario `YH-UI-SC-001: Create site from Git repository URL` using Page Object Model, authenticated fixture reuse, pre-cleanup, and async status validation (`Created` -> `Active`).

## Source-of-truth scenarios (must not be modified)
- `tests/e2e/e2e_test_scenarios.md`

## Clarifications applied
1. Navigation naming:
   - Use shared `navigate(path)` from `BasePage`.
   - Do **not** add separate `open(...)` methods for admin pages unless needed later.
2. Async UI checks:
   - Use Playwright `expect(...).to_contain_text(...)` with explicit timeout for status transitions.
3. Pre-cleanup requirement:
   - Use API-layer cleanup fixture to ensure user has no existing site before test starts (free-plan precondition).
   - Do not use UI interactions for precondition cleanup.
4. Status progression:
   - Validate newly created site first appears as `Created` and later reaches `Active`.

## Implementation plan

### 1. Config and fixture prerequisites
- [x] Ensure env/config exposes required values for UI site creation flow:
  - [x] `GIT_REP_URL` (already used).
  - [x] `SITE_CREATE_PATH` (default `/site/create`) for UI navigation.
  - [x] `SITES_LIST_PATH` (default `/site`) for post-create assertions.
- [x] Keep `base_url` handling as currently configured in Playwright context.

### 2. Reusable authenticated fixture (UI layer)
- [x] In `tests/e2e/conftest.py`, add function-scoped fixture `authenticated_dashboard_page`:
  - [x] Navigate to `login_path` via `LoginPage.navigate(...)`.
  - [x] Execute `login_action(email, password)`.
  - [x] Assert dashboard URL and return `DashboardPage`.

### 3. Pre-cleanup fixture for free-plan precondition
- [x] Add function-scoped fixture `ensure_no_sites_api` in shared module `tests/fixtures/preconditions_api.py`.
- [x] Behavior:
  - [x] Authenticate via API client (`requests.Session` + Sanctum flow).
  - [x] List existing sites via API.
  - [x] If sites exist, delete all via API and verify deletion results.
  - [x] Re-check via API that site list is empty before UI scenario starts.
- [x] Failure handling:
  - [x] Fail fast with clear assertion message if cleanup is incomplete.
- [x] Notes:
  - [x] Keep API cleanup and UI scenario in same function scope.
  - [x] Avoid parallel execution for this shared free-plan user (or use dedicated user per worker).
  - [x] If needed, add short retry/poll for eventual consistency between API cleanup and UI read.
  - [x] Make fixture reusable for both API and E2E test layers.
  - [x] Register shared fixtures from `tests/conftest.py` (keep `tests/e2e/conftest.py` UI-only).

### 4. POM additions for site creation flow
- [x] Create `tests/e2e/pages/site_create_page.py` inheriting `AdminBasePage`:
  - [x] Locator for Git URL input.
  - [x] Locator for `Create` submit button.
  - [x] Method `create_from_git(repo_url: str) -> None` using existing `navigate(...)`.
- [x] Create `tests/e2e/pages/sites_page.py` inheriting `AdminBasePage`:
  - [x] Locators for sites table/list rows, status cell, generated domain/link.
  - [x] Methods:
    - [x] assert sites list page opened.
    - [x] assert newly created site row visible.
    - [x] assert row contains `Created` status.
    - [x] wait/assert row status transitions to `Active` using `expect(...).to_contain_text(...)`.
    - [x] click generated site link, capture new tab (`page.expect_popup()`), and validate created site availability in the new tab.

### 5. Test implementation
- [x] Create `tests/e2e/test_site_creation.py`.
- [x] Add test for `YH-UI-SC-001` with fixtures:
  - [x] `authenticated_dashboard_page`
  - [x] `ensure_no_sites_api`
  - [x] `git_repo_url` (or UI-specific alias)
  - [x] `site_create_path`, `sites_list_path`
- [x] Flow assertions:
  - [x] Submit valid git repo URL.
  - [x] Verify redirect/opened sites list page.
  - [x] Verify created site row appears with `Created` status.
  - [x] Wait for status `Active`.
  - [x] Verify generated site link/domain is non-empty, clickable, and accessible.

### 6. Reliability and diagnostics
- [x] Avoid fixed sleeps where possible; prefer Playwright waits/expect timeouts.
- [x] Add explicit assertion messages for each business checkpoint.
- [x] Keep test independent/idempotent via cleanup fixture.

### 7. Validation
- [x] Run collection:
  - [x] `python3 -m pytest --collect-only -q tests/e2e`
- [x] Run target scenario:
  - [x] `python3 -m pytest -q tests/e2e/test_site_creation.py -k ui_sc_001`

## Deliverables
- New fixtures in `tests/e2e/conftest.py`.
- New page objects for site creation and site list.
- New E2E test module for `YH-UI-SC-001`.
- Stable async status verification from `Created` to `Active`.
