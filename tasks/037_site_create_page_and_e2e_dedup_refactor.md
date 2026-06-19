# 037: SiteCreatePage and E2E Site Creation Dedup Refactor

## Task summary
Refactor `SiteCreatePage` and the site-creation E2E tests to reduce duplication, improve method naming clarity, and preserve existing scenario coverage and behavior.

## Source-of-truth scenarios (must not be modified)
- `tests/e2e/e2e_test_scenarios.md`

## Naming decisions approved
1. Rename ambiguous upload methods in `SiteCreatePage`:
   - `create_from_git(...)` -> `create_via_git(...)`
   - `create_from_upload(...)` -> `create_via_upload_file(...)`
   - `create_from_folder(...)` -> `create_via_upload_folder(...)`
   - `create_from_editor(...)` -> `create_via_editor(...)`
2. Keep public method names intent-revealing at test call sites.
3. Prefer `via_upload_*` wording for upload-driven flows to distinguish them from Git and Editor creation modes.
4. Standardize `custom_domain` support across all public `create_via_*` methods where the UI supports the field.

## Refactoring goals
- Reduce duplicated submit/wait logic inside `tests/e2e/pages/site_create_page.py`.
- Keep Page Object Model boundaries clean: selectors and UI interaction details stay in page classes.
- Reduce repeated setup and verification code in `tests/e2e/test_site_creation.py` without weakening scenario readability.
- Preserve existing test independence and assertions.

## Implementation plan

### 1. Refactor `SiteCreatePage`
- [x] Update `tests/e2e/pages/site_create_page.py`.
- [x] Rename methods:
  - [x] `create_from_git(...)` -> `create_via_git(...)`
  - [x] `create_from_upload(...)` -> `create_via_upload_file(...)`
  - [x] `create_from_folder(...)` -> `create_via_upload_folder(...)`
  - [x] `create_from_editor(...)` -> `create_via_editor(...)`
- [x] Introduce an internal `create_site(...)` orchestration method to centralize shared flow.
- [x] Add optional `custom_domain` support to all public `create_via_*` methods.
- [x] Validate source-specific arguments inside the orchestration method.
- [x] Add small private helpers for repeated actions:
  - [x] create-button submit helper
  - [x] optional custom-domain fill helper
  - [x] single-file upload helper
  - [x] folder upload helper
- [x] Keep existing behavior for:
  - [x] Git repository creation
  - [x] file upload creation
  - [x] folder upload creation
  - [x] editor-based creation

### 2. Update site creation E2E tests
- [x] Update `tests/e2e/test_site_creation.py` to use the renamed page-object methods.
- [x] Reduce repeated flow code where practical while keeping each scenario readable.
- [x] Extract shared helpers for repeated asset lookup and/or repeated post-creation verification if this can be done without hiding test intent.
- [x] Do not change scenario meaning, order, or expected results.

### 3. Reliability and readability checks
- [x] Keep explicit assertions with clear messages for missing local test assets.
- [x] Continue using Playwright expectations instead of sleeps.
- [x] Avoid introducing raw page interaction logic into test functions beyond scenario orchestration.

### 4. Validation
- [x] Run focused test collection for `tests/e2e/test_site_creation.py`.
- [ ] Run the targeted E2E site creation test module if the local environment supports it.

## Deliverables
- `tasks/037_site_create_page_and_e2e_dedup_refactor.md`
- Updated `tests/e2e/pages/site_create_page.py`
- Updated `tests/e2e/test_site_creation.py`
