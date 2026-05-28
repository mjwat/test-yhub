# 017: Local Allure History Support

## Task summary
Add simple local Allure history support for this pytest project so Allure reports preserve trend/history data between local test runs.

## Scope
- Local execution only
- No CI or GitHub Actions changes
- Keep implementation minimal and easy to understand
- Reuse the existing pytest + Allure CLI setup

## Repository findings
- Test execution is currently documented via direct `pytest` commands in `README.md`
- Allure raw results are already generated with `--alluredir=allure-results`
- Allure HTML reports are already generated locally with the Allure CLI
- `allure-results/` and `allure-report/` are already ignored in `.gitignore`
- There is no reusable local helper script yet for Allure history/trend preservation
- Project uses `requirements.txt` and `pytest.ini`; no wrapper tool like Make, tox, nox, or Poetry is present

## Approved implementation plan

### 1. Add a reusable local script
- Create a small shell script under `scripts/`
- Proposed path:
  - `scripts/run_allure_with_history.sh`
- Keep the script readable and self-contained

### 2. Script behavior
- Clean old `allure-results/`
- Recreate `allure-results/`
- Run `pytest` with `--alluredir=allure-results`
- Use `python3 -m pytest` in the script for better local environment compatibility
- Restore previous history into `allure-results/history` if a saved local history cache exists
- Generate a fresh report into `allure-report/`
- Save the newly generated `allure-report/history` for reuse on the next run
- Optionally open the generated report locally
- Return the original pytest exit code so test failures remain visible

### 3. Safe local history preservation
- Store reusable trend/history data in a dedicated local cache directory
- Proposed cache path:
  - `.allure-history/`
- Recommended flow:
  - Before report generation, copy `.allure-history/history` into `allure-results/history` when present
  - After report generation, refresh `.allure-history/history` from `allure-report/history`
- First run must remain safe:
  - If no saved history exists yet, skip restore and continue normally
  - After the first successful report generation, initialize the local history cache

### 4. .gitignore update
- Add:
  - `.allure-history/`

### 5. README update
- Add prerequisites:
  - Python dependencies installed
  - Allure CLI installed locally
- Add script usage examples:
  - Run full test suite with history support
  - Run a targeted pytest selection with history support
  - Open the generated report optionally
- Explain how history/trends work:
  - Allure reads prior `history` data from the results directory during report generation
  - The script preserves that history in a local cache between runs
  - The first run creates the baseline for later trend data

## Deliverables
- `scripts/run_allure_with_history.sh`
- `.gitignore` update for local history cache
- `README.md` update for local usage and behavior

## Implementation status
- [x] Added `scripts/run_allure_with_history.sh`
- [x] Added `.allure-history/` to `.gitignore`
- [x] Updated `README.md` with prerequisites, commands, and history behavior
- [x] Kept the change local-only with no CI configuration

## Validation notes
- Verify the script is safe when `.allure-history/` does not exist
- Verify the script still generates `allure-results/` and `allure-report/`
- Verify a second run reuses saved history without manual copying
- Keep all changes local-only with no CI configuration

## Validation status
- [x] Script logic handles first-time execution by restoring history only when `.allure-history/history` exists
- [x] Shell syntax check passed for `scripts/run_allure_with_history.sh`
- [x] Allure CLI availability confirmed in the current local environment
- [x] Local repo virtualenv pytest availability confirmed (`venv/bin/python3 -m pytest --version`)
- [ ] Full end-to-end script execution against local tooling
- [ ] Confirmed second-run trend reuse with generated Allure artifacts
