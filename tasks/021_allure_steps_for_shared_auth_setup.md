# 021: Allure Steps for Shared Authentication Setup

## Task summary
Add concise Allure steps to shared authentication fixtures and utilities so reports show how authenticated API and UI state is prepared.

## Scope
- Add steps to shared auth setup only
- Keep step naming high-level and readable
- Avoid low-level UI interaction or raw HTTP noise
- Do not add screenshots, attachments, or CI changes

## Strategy
- Use fixture-level steps to show when authenticated state is being prepared
- Use shared auth utility steps to show key grouped auth actions
- Keep nested steps limited to meaningful phases:
  - initialize authenticated session
  - submit login
  - verify authenticated landing area

## Deliverables
- `tasks/021_allure_steps_for_shared_auth_setup.md`
- Shared auth step updates in:
  - `tests/fixtures/auth.py`
  - `clients/auth_client.py`
  - `tests/e2e/pages/login_page.py`

## Implementation status
- [x] Added the task document
- [x] Added Allure steps to shared API authentication setup
- [x] Added Allure steps to shared UI authentication setup
- [ ] Validate updated test collection
