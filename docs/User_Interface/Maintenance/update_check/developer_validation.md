# Developer Validation and Safeguards

This page collects the update-check regression workflows, debug calls, and safeguards. Use it with [UI Build Polling](ui_build_polling.md) and [GitHub Update Polling](github_update_polling.md) when validating a specific polling path.

## Run the Comparison Regression Test

```bash
node src/tests/update_check_comparison_test.js
```

## Simulate a Non-Main Branch Update

```bash
git checkout my-feature
git commit --allow-empty -m "test update polling"
git push origin my-feature
```

Load an older local build from the same branch. The GitHub compare status should become `ahead`, causing an update notification.

## Test Main Branch Release Policy

```bash
git checkout main
git commit --allow-empty -m "test main ahead without release"
git push origin main
```

A `main` commit difference alone should not show an app update. A newer tagged GitHub release is required.

## Useful Debug Console Calls

```js
updateWsprryPiVersion();
forceUpdateCheckNow();
checkUiBuildVersion();
readUpdateModalState();
isUpdateCheckDisabled();
setUpdateCheckDisabled(false);
```

## Safeguards

* `uiBuildPollTimer` prevents duplicate UI polling intervals
* `githubUpdatePollTimer` prevents duplicate GitHub polling intervals
* `uiBuildVersionCheckRunning` prevents overlapping UI build checks
* `uiRefreshPromptActive` prevents duplicate UI reload prompts
* `data-update-check-active` protects shared modal ownership
* `releaseUpdateCheckModalOwnership()` clears update modal handlers before generic confirmation dialogs reuse the modal
* `/ui-version.php` sends:

```text
Cache-Control: no-store, no-cache, must-revalidate, max-age=0
```

* GitHub API fetches use:

```js
cache: "no-store"
```

* UI assets use build-id query parameters for cache busting
* Branch-aware policy prevents `main` from reporting unreleased commits as user-facing updates
