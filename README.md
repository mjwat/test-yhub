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

If the Allure CLI is installed on your machine, you can open the report directly:

```bash
allure serve allure/results
```

Or generate static HTML output and open it:

```bash
allure generate allure/results -o allure/report --clean
allure open allure/report
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

## How local history works

The script removes old `allure/results/`, runs `python3 -m pytest --alluredir=allure/results`, restores any saved Allure `history` data before report generation, then builds a fresh `allure/report/`.

After the report is generated, the script saves `allure/report/history` into `allure/history/` so the next local run can reuse it and keep trend widgets populated.

On the first run, no history cache exists yet. The script skips restore safely, generates the report normally, and creates the local history baseline for later runs.
