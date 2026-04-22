# AU – Authorization via UI

## YH-UI-AU-001: Successful login with valid credentials

### Goal
Verify that a registered user can authenticate successfully via the web interface.

### Test Data
- Credentials: Email and password from .env / config file.
- URL: The Base URL and login path from .env / config file.

### Preconditions
- User account exists
- Valid email and password are stored in .env
- Browser is opened in a clean context (no previous sessions)

### Steps
1. Navigate to the login page.
2. Enter valid email into the email input field.
3. Enter valid password into the password input field.
4. Click the "Login" button.
5. Verify that the URL changes to the expected post-login page (e.g., /dashboard).
6. Verify that a success element is visible (e.g., "Logout" button or user profile name).


### Expected Result
- Authentication succeeds and the user is redirected.
- The UI reflects the "Logged In" state.