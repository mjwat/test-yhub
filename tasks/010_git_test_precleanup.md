# 010 Git Test Pre-cleanup

## Summary
Add precondition cleanup for `test_site_creation_by_git` so the test can run reliably under the 1-site account limit.

## Plan
Introduce a dedicated fixture that ensures the user has zero sites before the git creation test starts. Reuse existing `site_client` and deletion helpers (`get_user_sites`, `delete_all_sites`) with shared authenticated session.

## Checklist

### 1. Fixture setup
- [x] Add fixture in `conftest.py` (function scope), e.g. `ensure_no_sites`.
- [x] In fixture, fetch current sites with `site_client.get_user_sites()`.
- [x] If sites exist, call `site_client.delete_all_sites()`.
- [x] Re-fetch site list after cleanup and verify it is empty.
- [x] Raise clear error if cleanup fails to empty account.

### 2. Test integration
- [x] Apply fixture only to `test_site_creation_by_git` in `tests/api/test_site_creation.py`.
- [x] Keep existing SC-001 test unaffected.
- [x] Keep git test body focused on create request + assertions.

### 3. Quality
- [x] Keep no raw HTTP logic in test functions.
- [x] Reuse existing fixture/client auth flow (no duplicated login logic).
- [x] Update checklist after implementation.

### 4. Validation
- [x] Validate syntax for changed files.
- [x] Verify utility marker collection still works.
- [ ] Run `test_site_creation_by_git` where environment permits and inspect logs. (blocked: DNS resolution failure for `yhub.net` in current environment)
