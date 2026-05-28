# 020: Allure Steps Initial Rollout

## Task summary
Introduce a minimal first rollout of Allure steps to improve report readability and debugging in the most flow-oriented pytest tests.

## Scope
- Add concise `allure.step(...)` blocks only where they improve report readability
- Keep steps flow-oriented and meaningful
- Avoid low-level UI interaction noise
- Do not add attachments, screenshots, links, tags, or CI changes

## Repository findings
- API tests already use client methods that group several technical actions
- E2E tests already use page objects that hide low-level locator interactions
- The best initial step candidates are the multi-phase site creation flows

## Step strategy
- Use steps for meaningful phases such as:
  - open a page
  - submit a business action
  - verify redirect or resulting state
  - verify created content is accessible
- Avoid steps for:
  - individual clicks and fills
  - trivial one-line assertions
  - fixture-managed setup and cleanup

## Initial rollout
- `tests/api/test_site_creation.py`
  - `test_site_creation_by_git`
- `tests/e2e/test_site_creation.py`
  - `test_create_site_from_git`

## Deliverables
- `tasks/020_allure_steps_initial_rollout.md`
- Minimal Allure step updates in the initial API and E2E site creation tests

## Implementation status
- [x] Added the task document
- [x] Added meaningful Allure steps to the initial API site creation flow
- [x] Added meaningful Allure steps to the initial E2E site creation flow
- [x] Kept steps concise and flow-oriented
- [ ] Validate the updated subset with pytest
