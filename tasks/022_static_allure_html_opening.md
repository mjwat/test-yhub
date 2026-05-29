# 022: Static Allure HTML Opening

## Task summary
Replace local Allure report opening commands that keep Java processes running with a static HTML opening workflow.

## Scope
- Keep local report generation based on `allure generate`
- Open `allure/report/index.html` directly
- Preserve existing history and categories behavior
- Update local usage documentation
- Do not add CI changes

## Repository findings
- The local helper script currently uses `allure open` when `--open` is passed
- The README still documents both `allure serve` and `allure open`
- Existing history restore/save logic and categories copy logic already work and should remain unchanged

## Implementation plan
- Keep:
  - `allure generate allure/results -o allure/report --clean --single-file`
- Replace:
  - `allure open allure/report`
  - `allure serve allure/results`
- New open behavior:
  - macOS: `open allure/report/index.html`
  - Linux: `xdg-open allure/report/index.html`

## Deliverables
- `tasks/022_static_allure_html_opening.md`
- `scripts/run_allure_with_history.sh`
- `README.md`

## Implementation status
- [x] Added the task document
- [x] Replaced script-based `allure open` usage with static HTML opening
- [x] Switched Allure report generation to single-file mode for direct local opening
- [x] Kept history and categories support unchanged
- [x] Updated README to describe the static HTML workflow
- [x] Updated the script to refresh history through a temporary full report before the final single-file build
- [ ] Validate script syntax
