# 013 SC-001 Pre-cleanup and Deletion Pause Variable

## Summary
Add account-cleanup precondition to SC-001 site creation page test, and improve deletion cleanup maintainability by moving pause duration into a single variable used by both logger text and `sleep`.

## Plan

### 1. Apply precondition to SC-001 test
- Update `tests/api/test_site_creation.py`:
  - Add `ensure_no_sites` fixture to `test_site_creation_page_available_for_authenticated_user`.
- Keep test body unchanged (status/url assertions remain the same).
- Reuse existing fixture architecture (no auth/session duplication).

### 2. Refine delete_all_sites pause handling
- Update `clients/site_client.py`:
  - Introduce a dedicated pause variable/constant (example: `cleanup_pause_seconds = 5`).
  - Use this variable in both:
    - logger message
    - `time.sleep(...)`
- Preserve existing behavior scope:
  - pause only after successful cleanup pass (`deleted_count > 0` and `failed_count == 0`).

### 3. Validation
- Syntax check changed files.
- Verify utility marker collection remains valid.
- Run targeted tests where environment permits.

## Checklist

### SC-001 precondition
- [x] Add `ensure_no_sites` to `test_site_creation_page_available_for_authenticated_user` fixture list.
- [x] Keep SC-001 assertions unchanged.

### Pause variable refactor
- [x] Add named variable for cleanup pause duration in `delete_all_sites()`.
- [x] Use the same variable in logger message and `time.sleep`.
- [x] Keep pause trigger conditions unchanged.

### Validation
- [x] Syntax check changed files.
- [x] Verify `pytest -m utility --collect-only -q` still works.
- [ ] Run relevant tests where environment permits. (blocked: DNS resolution failure for `yhub.net` in current environment)
