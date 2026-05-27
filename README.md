# Test YHub

## Local setup

Install project dependencies:

```bash
pip install -r requirements.txt
```

## Run tests with Allure results

Generate Allure result files locally:

```bash
pytest --alluredir=allure-results
```

You can also target a specific test module if needed:

```bash
pytest tests/api/test_auth_login.py --alluredir=allure-results
```

## Open the HTML report locally

If the Allure CLI is installed on your machine, you can open the report directly:

```bash
allure serve allure-results
```

Or generate static HTML output and open it:

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

Note: `allure-pytest` creates the raw result files. HTML report generation requires the external Allure CLI to be installed locally.
