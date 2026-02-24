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
- [ ] Create `clients/site_client.py` for Site Creation page API access.
- [ ] Create test file `tests/api/test_site_creation.py`.
- [ ] Update `conftest.py` with reusable fixtures for authenticated access and site client wiring.
- [ ] Update `utils/config.py` to include admin URL and page endpoint config.

### 2. Environment/config
- [ ] Add `ADMIN_BASE_URL` support in config.
- [ ] Add `SITE_CREATE_ENDPOINT` support in config (default `/site/create`).
- [ ] Keep existing auth env usage unchanged for credentials.
- [ ] Ensure URL normalization avoids double slashes.

### 3. Authentication reuse
- [ ] Add/reuse fixture to establish authenticated Sanctum session via:
  - CSRF initialization (`/sanctum/csrf-cookie`)
  - Login (`/login`) with `X-XSRF-TOKEN`
- [ ] Keep CSRF/login orchestration out of test body.
- [ ] Return authenticated session for downstream client usage.

### 4. Site Creation page verification (YH-SC-001)
- [ ] Implement scenario in `tests/api/test_site_creation.py`.
- [ ] Assert response status code is `200`.
- [ ] Assert no redirect to login occurs.
- [ ] Keep one logical check per assertion with clear messages.

### 5. Quality and stability
- [ ] Keep test independent and idempotent (fresh session per test).
- [ ] Keep client methods free of assertions.
- [ ] Keep test readable and minimal.
- [ ] Update task checkbox status after implementation.

## Expected outcome
A clean, maintainable API test that proves an authenticated user can access the Site Creation page (`/site/create`) with HTTP 200 and without login redirect, while reusing centralized Sanctum authentication fixtures.
