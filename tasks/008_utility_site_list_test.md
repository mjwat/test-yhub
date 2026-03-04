# 008 Utility Site List Test

## Summary
Replace the standalone debug script with a pytest utility test that reuses shared fixtures and authentication flow.

## Plan
Use `site_client` fixture inside a utility-marked test to fetch current sites and log them via `logging.info`, so all auth/session/base URL logic is reused from `conftest.py` and `AuthClient.authenticate(...)` path.

## Checklist

### 1. Remove duplicated debug path
- [x] Delete `tasks/tmp_check_site_list.py`.

### 2. Add utility pytest test
- [x] Create `tests/test_utilities.py`.
- [x] Add `test_print_site_list(site_client)`.
- [x] Mark test with `@pytest.mark.utility`.
- [x] Log parsed site list output in readable format (`logging.info`).

### 3. Marker registration
- [x] Register `utility` marker in `pytest.ini`.

### 4. Validation
- [x] Validate syntax for changed files.
- [x] Verify utility test can be selected with `-m utility`.
- [x] Update this checklist after implementation.

## Run commands
- Utility only: `pytest -m utility -v`
- Exclude utility: `pytest -m "not utility" -v`
