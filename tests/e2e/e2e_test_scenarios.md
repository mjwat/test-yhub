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


# SC – Site Creation via UI

## YH-UI-SC-001: Create site from Git repository URL

### Goal
Verify that an authorized user can create a site by providing a valid Git repository URL.

### Test Data
- Repository URL in env / config.

### Preconditions
- User is authenticated.
- User has no created site on free plan.
- Site Creation page is opened.
- A valid Git repository URL with a deployable static site is available.

### Steps
1. Select Git tab.
2. Enter a valid Git repository URL.
3. Click submit button.
4. Verify that Sites list page is opened.
5. Verify new site appears in the list with Create status.
6. Wait until the site status becomes Published.
7. Open the generated site URL.
8. Verify new site is available.

### Expected Result
- Site is successfully created based on the provided Git repository.
- An auto-generated domain is assigned.
- The new site appears in the user’s site list.
- Created site link is clickable and accessible.

### Notes
- Domain value should not be empty after creation.
- Test must correctly handle asynchronous status updates while the site is being built/deployed.



## YH-UI-SC-002: Create site from single file and with custom domain

### Goal
Verify that an authorized user can create a site by providing a html file and with custom domain.

### Test Data
- test file index.html in /data directory.
- domain is "my-test-domain"

### Preconditions
- User is authenticated.
- User has no created site on free plan.
- Site Creation page is opened.
- Test file exist.

### Steps
1. Enter domain.
2. Upload html file.
3. Click submit button.
4. Verify that Sites list page is opened.
5. Verify new site appears in the list with Create status.
6. Wait until the site status becomes Published.
7. Check created site domain matches entered value.
8. Open the generated site URL.
9. Verify new site is available.


## YH-UI-SC-003: Create site from archive

### Goal
Verify that an authorized user can create a site by providing archive.

### Test Data
- test file archive.zip in /data directory.

### Preconditions
- User is authenticated.
- User has no created site on free plan.
- Site Creation page is opened.
- Test file exist.

### Steps
1. Upload zip file.
2. Click submit button.
3. Verify that Sites list page is opened.
4. Verify new site appears in the list with Create status.
5. Wait until the site status becomes Published.
6. Open the generated site URL.
7. Verify new site is available.



## YH-UI-SC-004: Create site with pdf

### Goal
Verify that an authorized user can create a site by providing pdf.

### Test Data
- test file sample.pdf in /data directory.

### Preconditions
- User is authenticated.
- User has no created site on free plan.
- Site Creation page is opened.
- Test file exist.

### Steps
1. Upload pdf file.
2. Click submit button.
3. Verify that Sites list page is opened.
4. Verify new site appears in the list with Create status.
5. Wait until the site status becomes Published.
6. Open the generated site URL.
7. Verify new site is available.