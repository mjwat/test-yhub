# AU – Authorization

## YH-AU-001: Successful login with valid credentials

### Goal
Verify that a registered user can authenticate successfully via API.

### Preconditions
- User account exists
- Valid email and password are stored in .env

### Steps
1. Get CSRF/session cookies.
2. Login with valid email/password, session cookies, and `X-XSRF-TOKEN` header.
3. Verify login response status code is 200 or 204.

### Expected Result
- Authentication succeeds.
- Session cookies are issued and accepted.


# SC – Site Creation

## YH-SC-001: Site Creation Page is available for authenticated user

### Goal
Verify that the site creation page is accessible to an authenticated user.

### Preconditions
- User account exists.
- Valid email and password are stored in .env.
- User is successfully authenticated (valid session cookie is established).

### Steps
1. Open /site/create page.
2. Verify response status code is 200.

### Expected Result
The request returns HTTP 200.
The right site creation page url is opened.


## YH-SC-002: Create site from single file

### Goal
Verify that an authorized user can create a site by uploading a single file.

### Preconditions
- User is authenticated
- /site/create page is accessible
- Valid HTML file is available for upload

### Steps
1. Open /site/create page.
2. Upload a valid HTML file.
3. Leave custom domain field empty.
4. Confirm site creation.
5. Verify redirect to /site page.
6. Verify new site appears in the list.
7. Wait until site status becomes "ready" (or equivalent).
8. Open generated site URL.

### Expected Result
- Site is successfully created.
- Auto-generated domain is assigned.
- Site appears in user’s site list.
- Uploaded content is accessible via generated URL.

### Notes
- Domain should not be empty after creation.
- Test must handle asynchronous status update.
