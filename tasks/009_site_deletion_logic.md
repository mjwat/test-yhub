# 009 Site Deletion Logic

## Summary
Plan account cleanup support to remove existing sites before tests, addressing the current 1-site account limit.

## Objective
Introduce reusable deletion logic in `SiteClient` and a utility entry point in `tests/test_utilities.py` so cleanup can be run on demand using existing authenticated fixtures and BaseApiClient infrastructure.

## Implementation plan (no code yet)

### 1. SiteClient deletion methods
Add two methods in `clients/site_client.py`:

- `delete_site(site_id)`
  - Low-level method for deleting one site by id.
  - Use `BaseApiClient` request helpers (`post`/`request`) and session reuse.
  - Include CSRF-aware headers via shared base helper (`xsrf_json_headers`) so Laravel web routes pass CSRF validation.
  - Keep method assertion-free; return `requests.Response`.

- `delete_all_sites()`
  - High-level method for cleanup.
  - Use existing `get_user_sites()` to fetch current sites.
  - Iterate through sites and call `delete_site(site_id)` for each.
  - Return structured summary (for example: total_found, deleted_ids, failed_ids/statuses) for debugging and utility output.

### 2. Route and payload considerations
- Confirm deletion route contract before coding (method/path/body):
  - confirmed: `DELETE {{BASE_ADMIN_URL}}/site/{{site_id}}`.
- Keep endpoint values config-driven where needed (avoid hardcoding URLs in tests).

### 3. Utility integration in tests/test_utilities.py
- Add a utility-marked test to trigger cleanup, e.g. `@pytest.mark.utility`.
- Use `site_client` fixture (already authenticated via `AuthClient.authenticate` in fixtures).
- Call `delete_all_sites()` and log summary with `logging.info`.
- Keep utility test simple and idempotent (safe to run repeatedly).

### 4. BaseApiClient architecture alignment
- Reuse shared session from fixture-created clients.
- Reuse shared request wrappers from `BaseApiClient`.
- Reuse shared XSRF header helper from `BaseApiClient`.
- Do not duplicate login/session logic in utility test.

### 5. Risks / edge cases
- Wrong deletion route or expected HTTP method can return `405`.
- Missing CSRF headers can return `419`.
- Some sites may be undeletable due to transient backend state; cleanup should continue and report partial failures.
- Site list may change during iteration; operate on snapshot returned by `get_user_sites()`.
- If no sites exist, cleanup should return success summary with zero deletions.

## Checklist

### SiteClient
- [x] Confirm delete endpoint contract (path, method, payload/method-override).
- [x] Add `delete_site(site_id)` method using BaseApiClient request + XSRF headers.
- [x] Add `delete_all_sites()` method reusing `get_user_sites()`.
- [x] Return cleanup summary for logging/debug.
- [x] Ensure no assertions inside client methods.

### Utility test
- [x] Add utility-marked cleanup test in `tests/test_utilities.py`.
- [x] Reuse existing `site_client` fixture (no duplicated auth logic).
- [x] Log cleanup summary via `logging.info`.
- [x] Keep utility test rerunnable and safe when site list is empty.

### Validation
- [x] Syntax check updated files.
- [x] Run utility test selection with `pytest -m utility --collect-only -q`.
- [ ] After implementation, run cleanup utility test and inspect logs. (blocked: DNS resolution failure for `yhub.net` in current environment)
