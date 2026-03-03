# 006 Site List Helper

## Summary
Add a reusable helper method to fetch and parse the authenticated user site list from the `/site` HTML page (`div#app[data-page]`) and return normalized site objects for future test preconditions.

## Scope for current iteration
- Fetch `GET {ADMIN_BASE_URL}{SITE_ENDPOINT}` using authenticated session.
- Parse HTML and extract JSON from `div#app` -> `data-page`.
- Read sites from JSON path: `props -> sites -> data`.
- Return list of dicts containing only:
  - `id`
  - `full_link`

Note:
- Do not derive `full_link` from `domain` in this task.
- Use existing `site[n].full_link` value directly.

## Implementation checklist

### 1. Client helper method
- [x] Add site list fetch/parse method in `clients/site_client.py`.
- [x] Keep HTTP and parsing logic inside client layer (not in tests).
- [x] Return `list[dict]` with `id` and `full_link` only.

### 2. HTML and JSON parsing
- [x] Parse `/site` response HTML and find `div` with `id="app"`.
- [x] Extract `data-page` attribute and parse it as JSON.
- [x] Navigate to `props -> sites -> data` safely.
- [x] Handle missing/invalid structure with clear errors.

### 3. Dependencies
- [x] Add/update parser dependency if needed (e.g., `beautifulsoup4`) in `requirements.txt`.
- [x] Keep implementation minimal and maintainable.

### 4. Temporary verification code
- [x] Add temporary runnable script to authenticate and call the new helper.
- [ ] Print parsed output in readable form to validate behavior. (blocked: `bs4` is not installed in current venv)
- [x] Keep script isolated so it can be removed after verification.

### 5. Quality checks
- [x] Validate Python syntax for updated files.
- [x] Update this checklist after implementation.

## Risks / edge cases
- `div#app` may be missing or `data-page` may be empty.
- `data-page` may contain malformed JSON.
- `props.sites.data` may be missing or null for empty accounts.
- Session expiry/redirect could return non-site-list HTML unexpectedly.
