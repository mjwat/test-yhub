# 002 Login Simplification

## Summary
The current Laravel Sanctum authorization test is functionally correct, but it contains duplicated authentication orchestration between the test and fixtures. The refactor will simplify structure by centralizing CSRF + login setup in fixtures and keeping the test focused on business-level authorization verification.

## Refactoring goal
Make the auth test architecture cleaner and easier to maintain by removing redundant flow logic, clarifying responsibility boundaries across client/fixtures/tests, and preserving Sanctum-critical behavior (CSRF cookie bootstrap, XSRF header, session-cookie continuity).

## Step-by-step checklist
- [x] Refactor `tests/api/test_auth_login.py` to consume `authenticated_session` fixture instead of running full CSRF/login flow inline.
- [x] Keep only authorization scenario assertions in the test (successful authenticated access to protected endpoint).
- [x] Consolidate CSRF + login orchestration in `conftest.py` within one fixture path.
- [x] Ensure fixture failure messages remain explicit (status code, URL, response body snippet) for quick 404/419 debugging.
- [x] Remove or adapt any unused fixture/code introduced by previous implementation passes.
- [x] Review `clients/auth_client.py` and keep only methods needed for current scenario.
- [x] Keep password masking in logs; reduce noisy/nonessential log lines.
- [x] Standardize config usage in `utils/config.py` around Sanctum endpoint keys.
- [x] Remove legacy config fallbacks only after confirming they are not used by current tests.
- [x] Re-check task files to ensure checkbox status accurately reflects completion state.
- [ ] Run the auth test and verify behavior remains unchanged after simplification. (`pytest` is not installed in current environment)

## Expected outcome
A lean, maintainable API auth test architecture where:
- Test files contain assertions and scenario intent only.
- Fixtures handle setup/auth preconditions.
- AuthClient handles API transport details.
- Sanctum constraints remain fully respected.
- Debugging remains straightforward with focused logs and explicit error context.
