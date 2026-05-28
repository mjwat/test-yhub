# 018: Local Allure Custom Categories Support

## Task summary
Add source-controlled custom Allure categories support so category definitions survive local report regeneration.

## Scope
- Local execution only
- No CI or GitHub Actions changes
- Keep implementation minimal and easy to maintain
- Reuse the existing `scripts/run_allure_with_history.sh` flow

## Repository findings
- Allure local artifacts already live under `allure/`
- The current local report generation flow is implemented in `scripts/run_allure_with_history.sh`
- The script already recreates `allure/results`, restores `allure/history/history`, and generates `allure/report`
- Generated report output already includes generated category artifacts under `allure/report/data` and `allure/report/widgets`
- There is no source-controlled categories definition file yet

## Source vs generated categories
- Source config:
  - `allure/categories.json`
  - This is the file intended for manual edits and version control
- Runtime input:
  - `allure/results/categories.json`
  - This is copied from the source file before report generation
- Generated report artifacts:
  - `allure/report/data/categories.json`
  - `allure/report/widgets/categories.json`
  - These files are produced by Allure and should not be edited manually

## Approved implementation plan

### 1. Add a source-controlled categories file
- Create:
  - `allure/categories.json`
- Start with a minimal useful set of categories for:
  - Environment issues
  - API issues
  - Playwright/browser issues
  - Assertion failures

### 2. Update the local Allure helper script
- Keep `scripts/run_allure_with_history.sh` as the single local generation entry point
- Before `allure generate`, copy:
  - `allure/categories.json`
  - to `allure/results/categories.json`
- Keep the copy logic safe:
  - If `allure/categories.json` does not exist, skip the copy and continue normally

### 3. Git ignore behavior
- No `.gitignore` change is required
- Existing ignores already cover generated directories:
  - `allure/results/`
  - `allure/report/`
  - `allure/history/`
- The new source file `allure/categories.json` remains tracked

## Deliverables
- `allure/categories.json`
- `scripts/run_allure_with_history.sh` update
- `tasks/018_allure_custom_categories_local_support.md`

## Implementation status
- [x] Added `allure/categories.json`
- [x] Updated `scripts/run_allure_with_history.sh` to copy categories into `allure/results/categories.json` before report generation
- [x] Kept the copy logic safe when the source file is missing
- [x] Kept the change local-only with no CI configuration
- [x] Documented the flow in this task file instead of `README.md`

## Validation notes
- Verify the script syntax remains valid
- Verify the script still works when `allure/categories.json` is absent
- Verify generated reports pick up custom categories when the source file exists
- Keep the implementation local-only and minimal
