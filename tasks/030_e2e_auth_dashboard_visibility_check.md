# 030: E2E Auth Dashboard Visibility Check

## Task summary
Update the login E2E assertion to validate dashboard navigation visibility after login instead of logout visibility, and align the shared UI component naming with `navigation`.

## Scope
- Keep the existing login flow unchanged
- Keep the existing URL assertion unchanged
- Replace the post-login `logout` visibility check with a `dashboard` visibility check
- Preserve the Page Object Model structure by exposing the locator from the navigation component
- Rename the shared `sidebar` component to `navigation`

## Deliverables
- `tasks/030_e2e_auth_dashboard_visibility_check.md`
- `tests/e2e/components/navigation.py`
- `tests/e2e/test_auth.py`

## Implementation status
- [x] Added the task document
- [x] Added a dashboard navigation locator
- [x] Updated the auth E2E assertion to use dashboard visibility
- [x] Renamed sidebar references to navigation
- [ ] Validate the updated E2E test
