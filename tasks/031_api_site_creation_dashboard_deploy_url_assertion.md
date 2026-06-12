# 031: API Site Creation Dashboard Deploy URL Assertion

## Task summary
Update the API site-creation page availability test to assert the authenticated landing URL using a shared fixture for the dashboard deploy path instead of the legacy site-creation endpoint.

## Scope
- Keep the existing request flow unchanged
- Keep the existing status code assertion unchanged
- Remove dependency on `site_client.site_create_page_endpoint` for the final URL assertion
- Introduce a shared fixture for the dashboard deploy path
- Build the expected final URL from `admin_base_url` and the shared dashboard deploy path
- Keep API tests independent from E2E page object classes/components

## Implementation plan

### 1. Add shared navigation path fixture
- Create a shared fixture that returns the dashboard deploy path:
  - `"/dashboard#deploy"`
- Place it in a shared fixture location so both API and E2E layers can reuse it without cross-layer coupling

### 2. Update the API test dependency list
- Update `test_site_creation_page_available_for_authenticated_user` to receive:
  - `admin_base_url`
  - the new shared dashboard deploy path fixture
- Keep the existing `site_client` and `clean_user_sites` fixtures

### 3. Replace the stale endpoint-based assertion
- Remove the assertion that checks `response.url` against `site_client.site_create_page_endpoint`
- Build `expected_url` from:
  - `admin_base_url`
  - shared dashboard deploy path fixture
- Assert the final URL against this expected authenticated landing URL

### 4. Keep helper usage aligned with the new expectation
- Prefer a direct full-URL assertion if the final destination is deterministic
- Update the assertion message to include both expected and actual URLs

### 5. Validation
- Run focused collection for `tests/api/test_site_creation.py`
- Run the targeted API test if the local environment supports pytest execution

## Deliverables
- `tasks/031_api_site_creation_dashboard_deploy_url_assertion.md`
- Shared fixture file for the new dashboard deploy path
- `tests/api/test_site_creation.py`

## Implementation status
- [x] Added the task document
- [x] Add shared dashboard deploy path fixture
- [x] Update the API test to use the shared fixture
- [x] Replace the legacy endpoint-based URL assertion
- [ ] Validate collection and targeted test execution
