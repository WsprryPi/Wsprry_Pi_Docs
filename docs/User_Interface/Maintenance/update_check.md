# WsprryPi Automatic Update Polling

## Architecture Overview

WsprryPi uses two independent background update systems that share common UI infrastructure but serve different purposes.

### User Interface Build Polling

The UI build poller detects local web UI file changes and prompts the browser to reload when the active interface is outdated.

It works by:

* Generating a `ui_build_id` from tracked PHP, JS, and CSS file metadata
* Polling the local `/version` endpoint every 60 seconds
* Comparing the loaded build ID against the current server build ID
* Showing a `UI refresh required` modal when they differ

This mechanism is entirely local and does not contact GitHub.

Purpose:

* Detect live UI changes during development
* Force asset cache invalidation
* Reload stale browser tabs after UI updates

### GitHub Application Update Polling

The GitHub update poller checks whether the installed WsprryPi build is behind upstream releases or branch commits.

It works by:

* Polling update metadata once per hour
* Fetching GitHub release and branch information
* Comparing the installed SHA/version against upstream targets
* Applying branch-aware update policy rules
* Showing an `Update available` or `Newer branch build available` modal when appropriate

Purpose:

* Notify users about newer releases
* Support branch-based prerelease workflows
* Detect newer commits on development branches

### Shared Infrastructure

Both systems share:

* The `/version` endpoint
* Shared Bootstrap modal infrastructure
* Local storage persistence
* Duplicate interval guards
* Modal suppression/retry logic

However, they intentionally use separate:

* Poll timers
* Comparison logic
* Dismissal state
* Update policies
* User-facing messaging

## Technical Overview

Current implementation lives primarily in `WsprryPi-UI/data/site.js`, with UI build metadata from `WsprryPi-UI/data/ui_version.php` and `/version` metadata from `src/web_server.cpp` or `WsprryPi-UI/data/version.php`.

### Two Separate Pollers

WsprryPi has two update mechanisms:

1. UI build-id polling detects whether the web UI files changed and prompts the browser to reload.
2. GitHub/app update polling checks whether the installed WsprryPi build is behind an upstream GitHub branch or release.

They share the `/version` endpoint and the shared Bootstrap `#confirmModal`, but they have separate timers, comparison rules, cache behavior, and dismissal state.

For ordinary update checks and notifications, use the [Maintenance page](index.md#update-checker). The pages below are implementation references for development and validation.

```{toctree}
:maxdepth: 1
:hidden:

UI Build Polling <update_check/ui_build_polling>
GitHub Update Polling <update_check/github_update_polling>
Update Prompts and Stored State <update_check/prompts_and_state>
Developer Validation and Safeguards <update_check/developer_validation>
```

## Detailed References

(ui-build-polling)=
- [UI Build Polling](update_check/ui_build_polling.md) documents build identity, asset cache invalidation, polling, refresh comparisons, and retry safeguards.

(github-app-update-polling)=
(github-comparison-flow)=
(update-policy)=
(main-branch-behavior)=
(non-main-branch-behavior)=
(detached-or-unknown-branch-behavior)=
(sha-comparison-behavior)=
(tagged-release-behavior)=
(commit-based-prerelease-behavior)=
- [GitHub Update Polling](update_check/github_update_polling.md) documents version metadata, comparison flow, and branch-aware release policy.

(modal-behavior)=
(ui-build-reload-modal)=
(app-update-modal)=
(local-storage-keys)=
(clear-update-check-state-for-testing)=
(force-github-check)=
(force-ui-reload-prompt)=
(reset-in-memory-ui-prompt-suppression)=
- [Update Prompts and Stored State](update_check/prompts_and_state.md) documents modal ownership, notification paths, dismissal behavior, local-storage keys, and testing controls.

(developer-workflows)=
(run-the-comparison-regression-test)=
(simulate-a-non-main-branch-update)=
(test-main-branch-release-policy)=
(useful-debug-console-calls)=
(safeguards)=
- [Developer Validation and Safeguards](update_check/developer_validation.md) collects regression workflows, debug calls, and duplicate-polling, cache, and policy protections.
