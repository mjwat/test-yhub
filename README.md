# Test YHub

## Local setup

Install project dependencies:

```bash
pip install -r requirements.txt
```

## Prerequisites

Install the Allure CLI locally so HTML reports can be generated and opened.

## Run tests with Allure results

Generate Allure result files locally:

```bash
python3 -m pytest --alluredir=allure/results
```

You can also target a specific test module if needed:

```bash
python3 -m pytest tests/api/test_auth_login.py --alluredir=allure/results
```

## Open the HTML report locally

Generate static HTML output:

```bash
allure generate allure/results -o allure/report --clean --single-file
```

Open the generated report file directly:

```bash
open allure/report/index.html
```

On Linux, use:

```bash
xdg-open allure/report/index.html
```

Note: `allure-pytest` creates the raw result files. HTML report generation requires the external Allure CLI to be installed locally.

## Run tests with Allure history support

Use the local helper script to preserve Allure history and trends between runs:

```bash
./scripts/run_allure_with_history.sh
```

The script prefers the repository `venv/` interpreter when it exists, and falls back to `python3`. You can override that with `PYTHON_BIN=/path/to/python`.

Run a specific test selection:

```bash
./scripts/run_allure_with_history.sh tests/api/test_auth_login.py
```

Open the generated report after the run:

```bash
./scripts/run_allure_with_history.sh --open
```

The `--open` option opens the generated static single-file `allure/report/index.html` report directly and does not start a local Allure web server.

## How local history works

The script removes old `allure/results/`, runs `python3 -m pytest --alluredir=allure/results`, restores any saved Allure `history` data before report generation, then builds a temporary full report to refresh trend data and a final single-file `allure/report/` for direct local opening.

After the temporary report is generated, the script saves its refreshed `history` into `allure/history/` and reuses that updated history when generating the final single-file report. This keeps trend widgets populated without breaking direct `index.html` opening.

On the first run, no history cache exists yet. The script skips restore safely, generates the report normally, and creates the local history baseline for later runs.
