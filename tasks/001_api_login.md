# YH-AU-001: Successful login with valid credentials

## Task summary
Implement the first API authorization scenario to verify that a registered user can authenticate successfully with valid credentials, receives an access token, and can use that token for authorized API requests.

## Approved implementation plan

### 1. Project structure changes
- [ ] Create `clients/auth_client.py` for auth API communication.
- [ ] Create `models/auth_models.py` for login response validation/parsing.
- [ ] Create `utils/config.py` for centralized env loading/access.
- [ ] Create `tests/api/test_auth_login.py` for test logic/assertions only.
- [ ] Create/modify root `conftest.py` for reusable fixtures.

### 2. Fixtures to implement (`conftest.py`)
- [ ] Add `env_config` (session scope): loads `.env` once and returns required values (`BASE_URL`, `TEST_USER_EMAIL`, `TEST_USER_PASSWORD`).
- [ ] Add `api_base_url` (session scope): exposes normalized base URL from config.
- [ ] Add `auth_client` (function scope): returns initialized `AuthClient`.
- [ ] Add `valid_login_payload` (function scope): provides credentials dict from env.
- [ ] Add `auth_token` (function scope): performs login once for token-dependent checks in the same test module.

### 3. API client design
- [ ] Implement `AuthClient` class using `requests.Session` (no raw HTTP in tests).
- [ ] Implement method `login(email: str, password: str) -> requests.Response`.
- [ ] Implement optional method `get_current_user(token: str)` (or equivalent protected endpoint) for token usability check.
- [ ] Keep endpoint paths encapsulated in client, not in tests.

### 4. Test data handling strategy
- [ ] Read sensitive credentials only from `.env` via `os.getenv()` (through `utils/config.py`).
- [ ] Fail fast with clear error if required env vars are missing.
- [ ] Keep tests/fixtures/client free of hardcoded credentials.
- [ ] Do not add JSON dataset for this scenario (all dynamic/sensitive from env).

### 5. Token validation approach
- [ ] Validate login response includes `access_token`.
- [ ] Validate token is non-empty string.
- [ ] Validate `token_type == "Bearer"` when field exists.
- [ ] Validate token usability by calling one authorized endpoint with `Authorization: Bearer <token>` and expecting success (`200`).

### 6. Assertion structure
- [ ] Keep one logical check per assertion with explicit failure messages.
- [ ] Add status code check.
- [ ] Add response schema/required field presence check.
- [ ] Add token field type/content check.
- [ ] Add token type check.
- [ ] Add authorized follow-up request check.

### 7. Independence and idempotency
- [ ] Keep test read/auth-only (no persistent state mutation).
- [ ] Use fresh login call per test execution (no cross-test shared mutable state).
- [ ] Scope fixtures to avoid hidden coupling.
- [ ] Ensure no dependency on execution order or previous tests.
