# Update Prompts and Stored State

This page documents the UI refresh and application update prompts, their shared modal coordination, dismissal behavior, and stored state. See [UI Build Polling](ui_build_polling.md) and [GitHub Update Polling](github_update_polling.md) for the checks that initiate these prompts.

## UI Build Reload Modal

* Uses `showConfirmationDialog()`
* Title:

```text
UI refresh required
```

* Confirm button:

```text
Refresh
```

* Cancel suppresses the same build/version for the current page lifetime
* Hidden while active also records the same in-memory dismissal
* Failed show attempts are retried on later polls

## App Update Modal

* Uses `showWsprryPiUpdateModal()`
* Uses `#confirmModal` with:

```js
backdrop: "static"
keyboard: false
```

* Marks ownership with:

```js
modalEl.dataset.updateCheckActive = "true"
```

* Stores modal state in localStorage using:

```text
wsprrypi.updateModalState
```

* Suppresses repeat modal popups for the same identity for two hours:

```js
UPDATE_MODAL_RATE_LIMIT_MS = 2 * 60 * 60 * 1000;
```

Modal identity is:

```json
{
  "branch": "...",
  "currentSha": "...",
  "targetSha": "...",
  "updateUrl": "..."
}
```

A different target SHA, remote version, branch, current SHA, or update URL can trigger an immediate popup.

The app update modal has these user paths:

* `Dismiss`: writes reason `dismissed`
* Close/hidden while active: writes reason `dismissed`
* `View release`: writes reason `opened`, hides modal, opens release URL
* `Never check again`: writes reason `dismissed`, sets:

```text
wsprrypi.updateCheckDisabled = "true"
```

and hides the modal.

Tagged release updates show a release link and `View release`. Commit/branch updates show branch/SHA context and hide the confirm action.

Storage events keep multiple tabs in sync. If another tab disables checks or dismisses/opens the same modal identity, the active modal hides.

## Local Storage Keys

Current keys:

```text
wsprrypi.updateCheck:<branchState>:<branch>:<sha>:<dirty-state>
wsprrypi.updateCheckFailure:<branchState>:<branch>:<sha>:<dirty-state>
wsprrypi.updateCheckDisabled
wsprrypi.updateModalState
```

There are no current `wsprrypi.updateDismissed*` localStorage keys. UI refresh dismissal is held only in JS variables, and app update dismissal is represented by `wsprrypi.updateModalState`.

### Clear Update-Check State for Testing

```js
Object.keys(localStorage)
  .filter((k) =>
    k.startsWith("wsprrypi.updateCheck") ||
    k.startsWith("wsprrypi.updateCheckFailure") ||
    k === "wsprrypi.updateModalState" ||
    k === "wsprrypi.updateCheckDisabled"
  )
  .forEach((k) => localStorage.removeItem(k));
```

### Force GitHub Check

```js
forceUpdateCheckNow();
```

### Force UI Reload Prompt

```js
maybePromptForUiRefresh({
  ui_build_id: "test-" + Date.now(),
  ui_version: window.WSPRRYPI_UI_VERSION
});
```

### Reset In-Memory UI Prompt Suppression

```js
dismissedUiRefreshBuildId = null;
dismissedUiRefreshVersion = null;
uiRefreshPromptActive = false;
```
