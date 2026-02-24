# 004 Configs Improving

## Summary
Standardize environment/config/client URL handling to reduce duplication and make endpoint configuration fully centralized and explicit.

## Implementation checklist

### 1. Environment updates
- [x] Update `.env` so `ADMIN_BASE_URL` is set as `BASE_URL + /admin` value.
- [x] Ensure `.env` keeps `SITE_CREATE_ENDPOINT=/site/create`.
- [x] Remove `AUTH_USER_EMAIL` and `AUTH_USER_PASSWORD` entries from `.env`.
- [x] Verify `AUTH_CHECK_ENDPOINT` is not present in `.env` (it is unused in current codebase).

### 2. Config validation updates (`utils/config.py`)
- [x] Remove support for `AUTH_USER_EMAIL` and `AUTH_USER_PASSWORD` aliases.
- [x] Validate `TEST_USER_EMAIL` and `TEST_USER_PASSWORD` directly via `_get_required_value`.
- [x] Move `ADMIN_BASE_URL` from optional fallback assignment to `_get_required_value` validation in config dict.
- [x] Keep `SITE_CREATE_ENDPOINT` as an endpoint config key loaded from env/default.

### 3. Endpoint ownership cleanup
- [x] Remove endpoint default values from client class constructor signatures where config is the single source.
- [x] Ensure endpoint values used by `AuthClient` and `SiteClient` are passed from fixtures/config.
- [x] Keep client constructors minimal and explicit.

### 4. Shared URL builder extraction
- [x] Extract duplicated `_build_url` logic from `clients/auth_client.py` and `clients/site_client.py` into a shared utility (e.g., `utils/url.py`).
- [x] Replace both client-specific `_build_url` methods with shared utility usage.
- [x] Keep URL normalization behavior unchanged.

### 5. Integration checks
- [x] Update fixtures in `conftest.py` to pass all required endpoints from config into clients after constructor changes.
- [ ] Verify login test still works with refactored config/client wiring. (blocked: DNS resolution failure for `yhub.net` in current environment)
- [ ] Verify site creation test still targets admin base URL + site create endpoint correctly. (blocked: DNS resolution failure for `yhub.net` in current environment)
- [x] Update this task checklist after implementation.

## Notes from pre-check
- `AUTH_CHECK_ENDPOINT` usage in code: not found.
- `AUTH_CHECK_ENDPOINT` in `.env`: already absent.
