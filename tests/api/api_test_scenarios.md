# AU – Authorization via API

## YH-API-AU-001: Successful login with valid credentials

### Goal
Verify that a registered user can authenticate successfully via API.

### Test Data
- Login and password locate in env / config.

### Preconditions
- User account exists
- Valid email and password are stored in .env

### Steps
1. Get CSRF/session cookies.
2. Login with valid email/password, session cookies, and `X-XSRF-TOKEN` header.
3. Verify login response status code is 200 or 204.
4. Verify admin url in response.

### Expected Result
- Authentication succeeds.
- Session cookies are issued and accepted.


# SC – Site Creation via API

## YH-API-SC-001: Site Creation Page is available for authenticated user

### Goal
Verify that the Site Creatin page is accessible to an authenticated user.

### Preconditions
- User account exists.
- Valid email and password are stored in .env.
- User is successfully authenticated (valid session cookie is established).

### Steps
1. Open Site Creatin page.
2. Verify response status code is 200.

### Expected Result
The request returns HTTP 200.
The right site creation page url is opened.


## YH-API-SC-002: Create site from Git repository URL

### Goal
Verify that an authorized user can create a site by providing a valid Git repository URL.

### Test Data
- An example repository URL for testing locates in env / config.

### Preconditions
- User is authenticated.
- Site Creation page is opened.
- A valid Git repository URL with a deployable static site is available.

### Steps
1. Enter a valid Git repository URL.
2. Confirm site creation (submit the form).
3. Verify that Sites list page is opened.
4. Verify new site appears in the list.
5. Wait until the site status becomes Active ("status": 4).
6. Open the generated site URL.

### Expected Result
- Site is successfully created based on the provided Git repository.
- An auto-generated domain is assigned.
- The new site appears in the user’s site list.
- Created site is accessible via the generated URL.

### Notes
- Domain value should not be empty after creation.
- Test must correctly handle asynchronous status updates while the site is being built/deployed.


## YH-API-SC-003: Create site from single HTML file

### Goal
Verify that an authorized user can create a site by uploading a single file.

### Test Data
- An example file is located at the path data/index.html

### Preconditions
- User is authenticated
- Site Creation page is opened
- Valid HTML file is available for upload

### Steps
1. Upload a valid HTML file.
2. Confirm site creation.
3. Verify that Sites list page is opened.
4. Verify new site appears in the list.
5. Wait until the site status becomes Active ("status": 4).
6. Open generated site URL.

### Expected Result
- Site is successfully created.
- Auto-generated domain is assigned.
- Site appears in user’s site list.
- Created site is accessible via the generated URL.

### Notes
- Domain should not be empty after creation.
- Test must handle asynchronous status update.
