# 016: Local Allure Report Setup for Pytest

## Task summary
Add local Allure Report support for this pytest-based test project so test runs can generate Allure result files, with no CI changes in this step.

## Scope
- Local setup only
- No CI or GitHub Actions changes
- Keep changes minimal and focused

## Implementation status
- [x] Add `allure-pytest` to `requirements.txt`
- [x] Keep `pytest.ini` unchanged
- [x] Add minimal local Allure usage documentation
- [x] Update `.gitignore` for Allure artifacts
- [x] Keep the change scoped to local setup only

## Repository findings
- Test framework uses `pytest`
- Dependencies are managed via `requirements.txt`
- No `pyproject.toml`, `Pipfile`, or Poetry configuration is present
- Existing pytest configuration is in `pytest.ini`
- Existing ignore rules in `.gitignore` do not yet cover Allure output
- No project `README.md` is currently present

## Approved implementation

### 1. Add dependency
- [x] Added `allure-pytest` to `requirements.txt`

### 2. Keep pytest configuration unchanged
- [x] Left `pytest.ini` unchanged for this initial local setup
- [x] Used CLI flags as the documented way to generate Allure results

### 3. Local test command with Allure results
- [x] Documented:
  - `pytest --alluredir=allure-results`

### 4. Optional local HTML report commands
- [x] Documented optional Allure CLI usage:
  - `allure serve allure-results`
  - `allure generate allure-results -o allure-report --clean`
  - `allure open allure-report`

### 5. Documentation update
- [x] Added minimal local usage documentation
- [x] Created root `README.md`
- [x] Included:
  - dependency installation
  - test execution with Allure results
  - local HTML report generation and opening
  - note that HTML report generation requires the Allure CLI

### 6. Git ignore update
- [x] Updated `.gitignore` to ignore:
  - `allure-results/`
  - `allure-report/`

## Notes
- `allure-pytest` enables pytest to write raw Allure result files
- HTML report generation is handled by the external Allure CLI, not by the Python package
- Some tests may use Playwright, but no Playwright-specific Allure setup is required for this initial local integration

## Files changed
- `requirements.txt`
- `.gitignore`
- `README.md`
- `tasks/016_allure_report_local_setup.md`

## Validation notes
- No test execution was performed in this step
- No dependency installation was performed in this step
