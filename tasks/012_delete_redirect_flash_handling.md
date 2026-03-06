# 012 Delete Redirect & Flash Handling

## Summary
Update site deletion flow to handle redirect and flash message extraction the same way as site creation, so deletion outcomes are asserted by server message instead of status code alone.

## Goal
Make `delete_site` return structured result with redirect/flash data and update cleanup logic to use that result for reliable success/failure reporting.

## Proposed plan

### 1. SiteClient delete flow update
- Keep initial delete request with `allow_redirects=False` to preserve raw redirect response.
- Read `Location` header from delete response.
- Follow redirect manually with the same authenticated session.
- Parse flash message from redirected page using existing helper (`props.flash.message`).
- Return structured delete result with:
  - `initial_status_code`
  - `redirect_location`
  - `redirect_status_code`
  - `flash_message`
  - `final_url`

### 2. Logging improvements
- Add logger entry in delete flow including redirect status/final URL/flash message.
- Add logger fallback for missing `Location` header.

### 3. Update delete_all_sites()
- Use structured delete result instead of raw `Response`.
- Determine success by flash message + expected redirect pattern (not status only).
- Keep partial failure collection and summary output.
- Include flash message in failed items for better diagnostics.
- Add forced stabilization delay after successful cleanup:
  - sleep `5` seconds before returning, to avoid immediate re-create hitting stale plan-limit state.

### 4. Utility test integration
- Keep `tests/test_utilities.py::test_cleanup_all_sites` as the entry point.
- Log expanded cleanup summary including flash messages.
- No duplicated auth/session logic (reuse fixture/client infrastructure).

### 5. Validation strategy
- Syntax check changed files.
- Collect utility tests (`pytest -m utility --collect-only -q`).
- Run cleanup utility test where environment allows.

## Expected delete flash messages
- Success: `Site deleted successfully`
- Other flash text indicates business failure and should be captured in summary.

## Checklist

### SiteClient
- [x] Update `delete_site(site_id)` to return structured redirect+flash result.
- [x] Reuse existing flash extraction helper path `props.flash.message`.
- [x] Add delete flow logging with flash message.

### Cleanup aggregation
- [x] Refactor `delete_all_sites()` to consume structured delete result.
- [x] Treat success based on expected flash message and collect failures with details.
- [x] Preserve resilient behavior (continue on per-site failure).
- [x] Add fixed `5` second wait after deletion cleanup completes.

### Utility visibility
- [x] Ensure cleanup utility output includes flash messages in summary.
- [x] Keep utility test unchanged in structure (fixture reuse only).

### Validation
- [x] Syntax check updated files.
- [x] Verify utility marker collection.
- [ ] Execute cleanup utility test where environment permits. (blocked: DNS resolution failure for `yhub.net` in current environment)
