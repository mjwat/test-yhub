# AU – Authorization

## YH-AU-001: Successful login with valid credentials

### Goal
Verify that a registered user can authenticate successfully via API.

### Preconditions
- User account exists
- Valid email and password are stored in .env

### Steps
1. Send POST request to /auth/login with valid email and password.
2. Verify response status code is 200.
3. Verify access token is returned in response body.
4. Verify token type is "Bearer" (if applicable).

### Expected Result
- Authentication succeeds.
- Access token is issued.
- Token can be used for authorized API requests.



# SC – Site Creation

## YH-SC-001: Create site from single file

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