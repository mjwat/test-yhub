# YH-AU-001: Successful login with valid credentials

## Task summary
Implement the first API authorization scenario to verify that a registered user can authenticate successfully with valid credentials using Laravel Sanctum CSRF + session-cookie flow.

## Backend update (Laravel Sanctum)
- [x] Confirm backend requires CSRF flow: `GET /sanctum/csrf-cookie` before login.
- [x] Confirm login endpoint is `POST /login` with session cookies and `X-XSRF-TOKEN` header.
- [x] Confirm expected auth mechanism is session/cookie-based (not bearer token for this flow).

## Approved implementation plan

### 1. Project structure changes
- [x] Create `clients/auth_client.py` for auth API communication.
- [x] Create `models/auth_models.py` for login response validation/parsing.
- [x] Create `utils/config.py` for centralized env loading/access.
- [x] Create `tests/api/test_auth_login.py` for test logic/assertions only.
- [x] Create/modify root `conftest.py` for reusable fixtures.

### 2. Fixtures to implement (`conftest.py`)
- [x] Add `env_config` (session scope): loads `.env` once and returns required values (`BASE_URL`, `TEST_USER_EMAIL`, `TEST_USER_PASSWORD`).
- [x] Add `api_base_url` (session scope): exposes normalized base URL from config.
- [x] Add `auth_client` (function scope): returns initialized `AuthClient`.
- [x] Add `valid_login_payload` (function scope): provides credentials dict from env.
- [x] Add `authenticated_session` (function scope): initializes CSRF and login with session cookies for dependent checks.

### 3. API client design
- [x] Implement `AuthClient` class using `requests.Session` (no raw HTTP in tests).
- [x] Implement method `login(email: str, password: str, xsrf_token: str) -> requests.Response`.
- [x] Implement method `get_current_user()` for session-based protected endpoint checks.
- [x] Keep endpoint paths encapsulated in client, not in tests.

### 4. Test data handling strategy
- [x] Read sensitive credentials only from `.env` via `os.getenv()` (through `utils/config.py`).
- [x] Fail fast with clear error if required env vars are missing.
- [x] Keep tests/fixtures/client free of hardcoded credentials.
- [x] Do not add JSON dataset for this scenario (all dynamic/sensitive from env).

### 5. Token validation approach
- [x] Validate login response includes `access_token`.
- [x] Validate token is non-empty string.
- [x] Validate `token_type == "Bearer"` when field exists.
- [x] Validate token usability by calling one authorized endpoint with `Authorization: Bearer <token>` and expecting success (`200`).

### 6. Assertion structure
- [x] Keep one logical check per assertion with explicit failure messages.
- [x] Add status code check.
- [x] Add response schema/required field presence check.
- [x] Add token field type/content check.
- [x] Add token type check.
- [x] Add authorized follow-up request check.

### 7. Independence and idempotency
- [x] Keep test read/auth-only (no persistent state mutation).
- [x] Use fresh login call per test execution (no cross-test shared mutable state).
- [x] Scope fixtures to avoid hidden coupling.
- [x] Ensure no dependency on execution order or previous tests.

## Revised implementation plan (Sanctum CSRF flow)

### 8. API client changes for Sanctum
- [x] Add `get_csrf_cookie()` in `clients/auth_client.py` to call `GET /sanctum/csrf-cookie`.
- [x] Read `XSRF-TOKEN` from session cookies after CSRF call.
- [x] Send `POST /login` with headers: `X-XSRF-TOKEN`, `Accept: application/json`, `Content-Type: application/json`.
- [x] Reuse one `requests.Session` so `laravel_session` + `XSRF-TOKEN` cookies persist automatically.
- [x] Keep request logging with masked password and include CSRF/login URLs.

### 9. Fixture and config updates
- [x] Add configurable `CSRF_ENDPOINT` defaulting to `/sanctum/csrf-cookie`.
- [x] Set `LOGIN_ENDPOINT` default to `/login` for Sanctum flow.
- [x] Keep credentials loaded from `.env` without hardcoding.

### 10. Test assertion updates
- [x] Assert CSRF request succeeds before attempting login.
- [x] Assert login status code is `200` or `204` based on backend behavior.
- [x] Assert auth session is valid via protected endpoint using same session (cookie-based), not bearer token.
- [x] Keep one logical check per assertion with clear failure messages.

### 11. Regression and idempotency checks
- [x] Ensure test remains independent by creating a fresh session per test.
- [x] Ensure no persistent data mutation beyond authentication session.
- [x] Update task checkboxes as each Sanctum subtask is completed.
