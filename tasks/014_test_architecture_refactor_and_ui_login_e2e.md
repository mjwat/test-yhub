# 014: Test Architecture Refactoring and E2E Login Implementation

## Task summary
Refactor pytest fixture architecture into layered `conftest.py` files and implement UI login E2E scenario `YH-UI-AU-001` using Playwright.

## Source-of-truth scenarios (must not be modified)
- `tests/api/api_test_scenarios.md`
- `tests/e2e/e2e_test_scenarios.md`

## Phase 1: Planning and approval
- [x] Prepare detailed refactoring/implementation plan before code changes.
- [x] Wait for explicit user approval before implementation.

## Approved implementation plan

### 1. Conftest hierarchy refactor
- [x] Create `tests/conftest.py` and keep only global essentials:
  - [x] `env_config` fixture (loads config once via `utils.config.get_env_config`).
  - [x] `base_url` fixture (normalized from `BASE_URL`).
- [x] Reduce root `conftest.py` to global essentials only (or remove if redundant after migration).
- [x] Move API-layer fixtures into `tests/api/conftest.py`:
  - [x] `api_base_url` (compat alias from `base_url` if needed).
  - [x] `admin_base_url`.
  - [x] `auth_client`.
  - [x] `test_user`.
  - [x] `git_repo_url`.
  - [x] `authenticated_auth_client`.
  - [x] `site_client`.
  - [x] `ensure_no_sites`.
  - [x] Keep requests/session/token handling in API layer only.
- [x] Create `tests/e2e/conftest.py` with UI/Playwright fixtures:
  - [x] `ui_user` fixture (email/password from env config).
  - [x] `browser_context_args` fixture (viewport + headed mode toggle policy).
  - [x] Optional UI path helpers for login/dashboard routes.

### 2. Implement UI scenario YH-UI-AU-001
- [x] Create `tests/e2e/test_auth.py`.
- [x] Navigate to `/login` using relative path from `base_url`.
- [x] Fill email/password from config-backed fixture.
- [x] Click login button using accessible locators (`get_by_role` / `get_by_label`).
- [x] Assert redirect to `/dashboard`.
- [x] Assert logged-in indicator visible (`Logout` or profile indicator).

### 3. Dependencies and validation
- [x] Ensure `pytest-playwright` is present in `requirements.txt`.
- [x] Run collection checks:
  - [x] `pytest --collect-only` for API and E2E tests.
- [x] Run focused E2E test (environment permitting):
  - [x] `tests/e2e/test_auth.py`.

## Architecture outcome (target)
- `tests/conftest.py` -> global shared fixtures only.
- `tests/api/conftest.py` -> API-only fixtures and requests session/token flow.
- `tests/e2e/conftest.py` -> UI-only Playwright setup.
- `tests/e2e/test_auth.py` -> YH-UI-AU-001 test implementation.
