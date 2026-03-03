# 007 Base API Client Refactor Plan

## Summary
Introduce a shared Base API Client to centralize session handling, URL composition, request execution, and CSRF/header utilities. Migrate `AuthClient` and `SiteClient` to this core so fixtures, tests, and helper scripts rely on consistent infrastructure.

## Goal
Reduce duplicated transport/auth plumbing across:
- `clients/auth_client.py`
- `clients/site_client.py`
- `conftest.py`
- `tasks/tmp_check_site_list.py`

while keeping tests focused on scenario steps and assertions.

## Scope
- Design and add `BaseApiClient` as the transport core.
- Migrate existing clients to reuse base capabilities.
- Keep endpoint/business-specific behavior in feature clients.
- Preserve current test behavior.

Out of scope:
- New test scenarios.
- Changing scenario assertions/coverage.
- Refactoring unrelated modules.

## Proposed architecture
- `clients/base_api_client.py`
  - Owns `requests.Session`
  - Builds absolute URLs from base + endpoint
  - Unified request wrapper (`request`, optional `get`/`post`)
  - Shared JSON/header helpers
  - XSRF token extraction helper from cookies
  - Standardized response context formatter for errors/logs

- `clients/auth_client.py`
  - Auth endpoints only: csrf init, login, authenticate
  - Uses base client request/header/cookie helpers

- `clients/site_client.py`
  - Site endpoints only: open create page, create by git, parse site list
  - Uses base client request/header/cookie helpers

## Implementation checklist

### 1. Add Base API Client
- [ ] Create `clients/base_api_client.py`.
- [ ] Implement session ownership/injection.
- [ ] Implement URL builder usage (reuse `utils/url.py`).
- [ ] Implement generic request method with consistent logging.
- [ ] Implement shared helpers for JSON headers and XSRF headers.

### 2. Migrate AuthClient
- [ ] Refactor `clients/auth_client.py` to use `BaseApiClient`.
- [ ] Keep public auth methods/signatures stable where possible.
- [ ] Preserve masked credential logging behavior.

### 3. Migrate SiteClient
- [ ] Refactor `clients/site_client.py` to use `BaseApiClient`.
- [ ] Keep site list parsing logic in `SiteClient` (domain-specific).
- [ ] Preserve current endpoint usage and redirect behavior.

### 4. Fixture/script integration
- [ ] Ensure `conftest.py` works with migrated clients without raw session logic.
- [ ] Ensure `tasks/tmp_check_site_list.py` continues using shared clients only.
- [ ] Remove any newly obsolete helper duplication introduced during migration.

### 5. Validation
- [ ] Validate syntax for all touched files.
- [ ] Run targeted tests (`tests/api/test_auth_login.py`, `tests/api/test_site_creation.py`) where environment permits.
- [ ] Update task checklist after implementation.

## Risks / edge cases
- Over-centralization can hide endpoint-specific intent if base client grows too much.
- CSRF header handling must remain compatible with Laravel session flow.
- Logging must avoid leaking sensitive data.
- Runtime validation may be blocked by environment DNS/network constraints.

## Migration order
1. Add `BaseApiClient`.
2. Migrate `AuthClient`.
3. Migrate `SiteClient`.
4. Verify fixtures/scripts.
5. Run targeted tests and adjust only if behavior regresses.
