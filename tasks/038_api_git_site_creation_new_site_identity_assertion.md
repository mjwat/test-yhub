# 038: API Git Site Creation New Site Identity Assertion

## Task summary
Update API scenario `YH-API-SC-002: Create site from Git repository URL` so it proves a new site was actually created without relying on an exact final site count.

## Source-of-truth scenarios (must not be modified)
- `tests/api/api_test_scenarios.md`

## Background
- The old assertion expected exactly one site after creation.
- That was valid when the precondition always removed every existing site.
- The new `ensure_site_creation_available` fixture only cleans up when the account reaches the site-count limit.
- Because of that, the account may legitimately start with one existing site and end with two sites after successful creation.

## Goal
Replace the fragile final-count assertion with a stronger identity-based assertion that confirms a new site record appears after the create request succeeds.

## Implementation plan

### 1. Capture pre-create site state
- Update `tests/api/test_site_creation.py`.
- Before calling `site_client.create_site_from_git_url(...)`, fetch current sites with `site_client.get_user_sites()`.
- Build a baseline set of existing site IDs from the pre-create response.

### 2. Keep existing request outcome assertions
- Keep the assertions for:
  - initial response status `302`
  - redirect location points to the sites list
  - success flash message equals `Site created successfully, and files uploaded.`

### 3. Replace final-count assertion with new-site detection
- Fetch the site list again after creation.
- Compare post-create site IDs against the baseline IDs.
- Assert that a new site ID appears after creation.
- Prefer asserting that exactly one new site record is present.

### 4. Validate the new site record shape
- Reuse the normalized `get_user_sites()` response.
- Assert the new site record includes required fields already exposed by the client:
  - `id`
  - `full_link`
- Keep assertion messages clear and diagnostic.

### 5. Stabilize for eventual consistency if needed
- If the new site does not always appear immediately after the create response, add a short polling/retry step around the post-create site-list check.
- Keep the retry local to the test or a narrowly scoped helper so behavior stays explicit.

### 6. Validation
- Run focused collection for `tests/api/test_site_creation.py`.
- Run targeted execution for `YH-API-SC-002` if the local environment supports network access.

## Deliverables
- `tasks/038_api_git_site_creation_new_site_identity_assertion.md`
- Updated `tests/api/test_site_creation.py`

## Implementation status
- [x] Added the task document
- [x] Capture pre-create site state in the API test
- [x] Replace final site-count assertion with new-site identity assertion
- [ ] Add retry logic if backend timing requires it
- [ ] Validate collection and targeted test execution (blocked locally: `pytest` is not installed in the current Python environment)
