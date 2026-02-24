# 003 Site Creation Page

## Summary
Implement automated coverage for **YH-SC-001** to verify that the Site Creation page is available to an authenticated user using Laravel Sanctum session authentication.

## Scope and constraints
- Do not modify `test_scenarios.md`.
- Reuse project architecture: client layer + fixtures + clean test assertions.
- No raw HTTP in tests.
- No absolute file system paths.

## Implementation checklist

### 1. Structure and files
- [x] Create `clients/site_client.py` for Site Creation page API access.
- [x] Create test file `tests/api/test_site_creation.py`.
- [x] Update `conftest.py` with reusable fixtures for authenticated access and site client wiring.
- [x] Update `utils/config.py` to include admin URL and page endpoint config.

### 2. Environment/config
- [x] Add `ADMIN_BASE_URL` support in config.
- [x] Add `SITE_CREATE_ENDPOINT` support in config (default `/site/create`).
- [x] Keep existing auth env usage unchanged for credentials.
- [x] Ensure URL normalization avoids double slashes.

### 3. Authentication reuse
- [x] Add/reuse fixture to establish authenticated Sanctum session via:
  - CSRF initialization (`/sanctum/csrf-cookie`)
  - Login (`/login`) with `X-XSRF-TOKEN`
- [x] Keep CSRF/login orchestration out of test body.
- [x] Return authenticated session for downstream client usage.

### 4. Site Creation page verification (YH-SC-001)
- [x] Implement scenario in `tests/api/test_site_creation.py`.
- [x] Assert response status code is `200`.
- [ ] Assert the correct site creation page URL is opened.
- [x] Keep one logical check per assertion with clear messages.

### 5. Quality and stability
- [x] Keep test independent and idempotent (fresh session per test).
- [x] Keep client methods free of assertions.
- [x] Keep test readable and minimal.
- [x] Update task checkbox status after implementation.

## Expected outcome
A clean, maintainable API test that proves an authenticated user can access the Site Creation page (`/site/create`), receive HTTP 200, and land on the correct site creation page URL, while reusing centralized Sanctum authentication fixtures.
