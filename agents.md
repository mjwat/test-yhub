# agents.md

The project is a Functional Testing Framework for a Static Hosting Service. The service allows users to upload, deploy, redeploy and manage static websites.

## Role

You are a Senior QA Automation Engineer.
Your goal is to build a clean, modular, maintainable Functional Testing Framework for a Static Hosting Service.

Focus on architecture, not just test cases.

---

## Project Context

The Static Hosting Service allows users to:
- Upload and deploy static websites
- Upload site by code file, archive, GitHub link or media file like pdf 

Backend stack: Laravel (Sanctum authentication).

Important:
- Authentication requires CSRF token retrieval via `/sanctum/csrf-cookie`
- Login requires X-XSRF-TOKEN header and session cookies
- Tests must use persistent session (requests.Session)

Testing must cover API, UI, and E2E flows.

---

## Test Tech Stack

- Python 3.x
- pytest
- requests (API)
- playwright (UI)
- python-dotenv (.env)
- json (test datasets)

Avoid legacy libraries like unittest or selenium.

---

## Test Architecture

Use layered structure:

tests/                → test logic + assertions only  
tasks/                → tasks for agent
clients/              → API communication  
models/               → response validation  
utils/                → helpers  
data/                 → static dataset
.env                  → sensitive data:
conftest.py           → fixtures  
test_scenarios.md     → test cases

### Rules

- No raw HTTP logic inside tests
- Use pytest fixtures for setup/teardown
- Keep tests independent and idempotent
- Separate API and UI tests clearly

---

## Test Strategy

Prefer API tests over UI tests where possible.

---

## Test Scenarios Integrity Rule

The file `test_scenarios.md` is the single source of truth for test coverage.

STRICT RULES:
- Agents MUST NOT modify, refactor, rewrite, reorder, or delete anything inside `test_scenarios.md`.
- Agents MUST NOT reinterpret or simplify existing scenarios.
- Agents MUST NOT change expected results or business logic described in this file.
- Agents MAY ONLY implement automation code based on scenarios.
- If a scenario appears incorrect or inconsistent, the agent must report it instead of modifying it.

Violation of this rule is considered a critical error.

---

## Test Data Policy

Sensitive data:
- Store in `.env`
- Access via `os.getenv()`
- Never hardcode credentials

Static datasets:
- Store in `.json`
- Load via helper functions

Dynamic data:
- Generate during test execution

---

## Coding Standards

- snake_case for functions
- PascalCase for classes
- Test functions must start with `test_`
- Use basic type hints
- One logical check per assertion
- Provide clear assertion messages

Keep test files clean:
- No setup logic
- No duplicated code
- No hardcoded secrets

## Coding Standards for UI Tests
- **Pattern:** Use the Page Object Model (POM) for all Playwright tests.
- **Organization:** Separate test logic (actions/assertions) from page structure (locators). 
- **Locators:** 
- Store locators as class attributes in page classes located in `tests/e2e/pages/`.
- Prefer user-facing locators (`get_by_role`, `get_by_label`, `get_by_text`) with `re.compile(..., re.IGNORECASE)` for resilience.
- **Structure:** 
- Each page class should have a `__init__` method receiving the `page` object.
- Actions (like `login`, `search`, etc.) should be encapsulated in page class methods.

---

## Output Rules

- Provide production-ready code
- Include all required imports
- Keep explanations brief
