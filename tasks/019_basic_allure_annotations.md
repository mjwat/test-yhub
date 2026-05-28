# 019: Basic Allure Annotations for Pytest Tests

## Task summary
Introduce a minimal set of Allure annotations to improve report readability in the active pytest suite.

## Scope
- Apply only these decorators:
  - `@allure.feature(...)`
  - `@allure.title(...)`
- Keep implementation lightweight
- Do not add severity, description, tags, links, steps, attachments, or CI changes

## Repository findings
- Allure is already configured for local pytest execution and report generation
- The active business-facing tests currently live in:
  - `tests/api/test_auth_login.py`
  - `tests/api/test_site_creation.py`
  - `tests/e2e/test_auth.py`
  - `tests/e2e/test_site_creation.py`
- These tests do not yet include test-level Allure annotations

## Annotation strategy

### Feature mapping
- Features map to stable product areas
- Initial features:
  - `Authentication`
  - `Site Creation`

### Title mapping
- Titles should be short human-readable expected outcomes
- Titles should avoid internal IDs and implementation details
- Initial title style examples:
  - `User can log in with valid credentials`
  - `Authenticated user can open the site creation page`
  - `User can create a site from a Git repository URL`

## Approved implementation plan

### 1. Update the initial subset of active tests
- Add minimal Allure decorators to:
  - `tests/api/test_auth_login.py`
  - `tests/api/test_site_creation.py`
  - `tests/e2e/test_auth.py`
  - `tests/e2e/test_site_creation.py`

### 2. Keep the first pass intentionally small
- Do not annotate fixtures, page objects, helper modules, or temp utility tests
- Do not introduce helper abstractions or shared constants yet

### 3. Validate collection and execution
- Run the updated test subset with pytest
- Confirm annotation changes do not affect test collection

## Deliverables
- `tasks/019_basic_allure_annotations.md`
- Minimal Allure annotation updates in the four active test modules

## Implementation status
- [x] Added the task document
- [x] Added minimal Allure annotations to the initial API and E2E test subset
- [x] Kept the implementation limited to feature and title decorators
- [x] Avoided any additional Allure functionality
- [x] Validate the updated subset with pytest

## Validation notes
- Ran:
  - `./venv/bin/python3 -m pytest -q tests/api/test_auth_login.py tests/api/test_site_creation.py tests/e2e/test_auth.py tests/e2e/test_site_creation.py`
- Result:
  - Test collection proceeded with the updated annotations in place
  - Full execution did not complete successfully in this environment
- Environment blockers observed during validation:
  - API tests could not resolve `yhub.net`
  - E2E tests failed during browser/runtime execution setup
