# 005 Site Creation by Git URL

## Summary
Add automated coverage for creating a site from a Git repository URL, focusing on initial creation success behavior only.

## Scope for current iteration
Validate only the first expected result:
- Site creation request by Git URL succeeds.
- Response status code is `302`.
- Redirect target is the sites list page.
- Git URL must be sent in request body as JSON:
  - `{"github_url": GIT_REP_URL}`

Out of scope for this iteration:
- Verifying created site presence in list data.
- Comparing created site names.
- Deployment readiness/status polling.

## Implementation checklist

### 1. Test placement
- [x] Add the Git creation test to `tests/api/test_site_creation.py`.
- [x] Keep existing SC-001 test unchanged.

### 2. Config and fixtures
- [x] Reuse authenticated fixtures (`authenticated_auth_client`, `site_client`).
- [x] Expose required `GIT_REP_URL` in `utils/config.py`.
- [x] Add `git_repo_url` fixture in `conftest.py` that reads from config.

### 3. Client updates
- [x] Add create-by-git method to `clients/site_client.py` (no assertions inside client).
- [x] Keep endpoint values env/config-driven (no hardcoded endpoints in tests).
- [x] Update create-by-git request payload format to JSON body:
  - `{"github_url": GIT_REP_URL}`
- [x] Include CSRF/session headers in create-by-git request:
  - use `X-XSRF-TOKEN` from authenticated session cookie
  - keep session cookies attached to the same request

### 4. Test assertions (current scope)
- [x] Assert create-by-git response status code is `302`.
- [x] Assert `Location` header exists in response.
- [x] Assert redirect location points to sites list page.

### 5. Quality checks
- [x] Keep test minimal: scenario steps + assertions only.
- [x] Keep raw HTTP calls out of test functions.
- [x] Update this checklist after implementation.

## Notes
- `GIT_REP_URL` already exists in `.env` and should be reused.
- Laravel `419` on create request usually indicates missing/invalid CSRF header for authenticated web route.
