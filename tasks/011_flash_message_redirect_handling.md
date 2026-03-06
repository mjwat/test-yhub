# 011 Flash Message Redirect Handling

## Summary
Handle site creation outcomes via flash messages after redirect, because create requests always return `302` for both success and failure cases.

## Goal
Update site creation flow to return both redirect metadata and flash message from the redirected page so tests can assert real outcome.

## Checklist

### 1. SiteClient flash parsing support
- [x] Add helper to parse Inertia payload (`div#app[data-page]`) from HTML response.
- [x] Add helper to extract flash message from fixed path: `props.flash.message`.
- [x] Reuse parser helper in existing site-list parsing to avoid duplication.

### 2. Create-by-git flow update
- [x] Update `create_site_from_git_url` to keep initial `302` response.
- [x] Follow redirect manually using same session.
- [x] Extract flash message from redirected page response.
- [x] Log extracted flash message in `create_site_from_git_url` for debug visibility.
- [x] Return structured result including:
  - `initial_status_code`
  - `redirect_location`
  - `redirect_status_code`
  - `flash_message`
  - `final_url`

### 3. Test update
- [x] Update `test_site_creation_by_git` to assert using structured create result.
- [x] Keep redirect assertions (`302` + `Location` to site list).
- [x] Add explicit flash message assertion for success case:
  - `Site created successfully, and files uploaded.`
- [x] Keep post-condition site count assertion as secondary signal.

### 4. Validation
- [x] Syntax check changed files.
- [ ] Run targeted test where environment permits. (blocked: DNS resolution failure for `yhub.net` in current environment)
- [x] Update this checklist after implementation.

## Known flash messages
- `Site created successfully, and files uploaded.`
- `You have reached the maximum number of sites allowed by your plan.`
- `Site deleted successfully`
