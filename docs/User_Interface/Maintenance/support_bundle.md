# Create and Share a Support Bundle

A support bundle gathers diagnostic information that can help a developer investigate a Wsprry Pi problem. The bundle is created on your Raspberry Pi and downloaded through your browser. Wsprry Pi does not upload it automatically.

:::{important}
A support bundle may contain sensitive information, including host and user names, network addresses, configuration values, logs, project paths, and service details. Wsprry Pi applies automatic redaction to common password, token, secret, and credential fields, but redaction is best-effort. Review the archive before sharing it.
:::

## Create the Bundle

1. Open **Maintenance** in the Wsprry Pi web interface.
2. In **Support Bundle**, select **Create Support Bundle**.
3. Read the collection and privacy notice.
4. Leave **Actively probe I²C bus 1** cleared unless a developer specifically needs an active bus scan.
5. Select **Create Support Bundle** in the dialog.
6. Wait while the panel reports that the bundle is queued or being collected. The collection time varies, so the interface does not show an estimated percentage.
7. When the bundle is ready, select **Download support bundle**.

The active I²C option is off by default. Passive I²C information is collected either way. Selecting the option runs exactly:

```bash
i2cdetect -y 1
```

That command actively probes every address on I²C bus 1. Leave it off when you do not need the scan or are unsure whether attached devices tolerate active probing.

The downloaded filename has this form:

```text
WsprryPi-support-HOST-UTC_TIMESTAMP.tar.gz
```

Your browser chooses the save location. Wsprry Pi can report the filename, but it cannot reliably report the final folder on your computer.

## What Happens After Download

The interface waits until it has received the complete archive before starting Pi-side cleanup. After a successful download, it asks the Pi to delete its retained copy.

- If cleanup succeeds, the Maintenance page confirms that the bundle was downloaded and removed from the Pi.
- If cleanup fails, your downloaded file remains valid. Use **Delete from Pi** to try again.
- A retained successful bundle expires automatically after 24 hours.
- Failed and cancelled collection jobs are removed without waiting for the retention period.
- Restarting the daemon removes stale jobs that cannot be resumed.

An interrupted or failed browser download does not trigger deletion, so you can try the download again.

## What the Bundle Collects

The collector creates a top-level `bundle` directory containing `README.txt`, `NEXT-STEPS.txt`, and the diagnostic groups below. A command that is unavailable or fails normally leaves a report showing that result rather than stopping the entire collection.

| Group | Information that may be included |
| --- | --- |
| System identity and resources | Hostname, current user and groups, kernel and operating-system release, CPU and memory details, Raspberry Pi model, boot command line, architecture, uptime, mounted filesystems, disk space, and memory use. |
| Raspberry Pi health | Firmware and bootloader version, throttling state, temperature, core voltage and clock, and ARM/GPU memory allocation when `vcgencmd` is available. |
| Wsprry Pi project | Detected checkout path, project file inventory, Git remote/status/commit information, build files, service documentation, and configuration files found in the checkout. |
| Installed runtime | Installed release and debug executable versions, help output, file metadata, architecture, ELF header, SHA-256, shared-library dependencies, installed INI file, and systemd unit details. |
| Services and logs | Wsprry Pi and Apache status, enablement, systemd properties, recent unit and identifier journals, recent system journal, kernel log, installer log, syslog/messages, and legacy Wsprry Pi logs when present. Normal collection limits the number of recent log lines. |
| GPIO and hardware | GPIO/I²C device nodes, loaded hardware-related kernel modules, group membership, GPIO chip/line information, selected GPIO lookups, pinout data, kernel GPIO debug information when readable, and Raspberry Pi boot configuration files. |
| I²C | Passive interface status from Raspberry Pi configuration, available I²C adapters from `i2cdetect -l`, and whether the active scan was skipped, succeeded, failed, or unavailable. The bus 1 address table appears only when the user explicitly enables active probing. |
| Web interface and Apache | Apache status, configuration test, sites, modules, listening TCP sockets, enabled/available Apache configuration, document-root and proxy declarations, web-root inventory, configured Wsprry Pi web/socket ports, and a local web-root probe. |
| Network and time | Interface addresses, routes, local and UTC time, time-zone/synchronization status, and Chrony or NTP peer information when available. |
| Packages | Installed Debian package list and policy information for selected Wsprry Pi build/runtime dependencies. |

Configuration-like text files are scanned for common credentials before the archive is created. URL-embedded credentials and common fields such as passwords, tokens, secrets, API keys, access keys, upload keys, and reporter passwords are replaced with `[REDACTED]`. Review is still necessary because logs and configuration formats can contain identifiers or sensitive values that the automatic patterns do not recognize.

The Maintenance workflow runs through the privileged daemon, so it can normally read the intended service and system diagnostics. The command-line collector also supports unprivileged use; when it cannot read privileged logs or system files, its result records that diagnostics may be incomplete.

## Review the Bundle Before Sharing

You can inspect the archive with your computer's archive application. To review it from a macOS or Linux terminal without extracting it first, set `BUNDLE` to the file your browser downloaded:

```bash
BUNDLE="/path/to/WsprryPi-support-HOST-UTC_TIMESTAMP.tar.gz"
tar -tzf "$BUNDLE" | less
```

To extract it into a new private temporary directory:

```bash
BUNDLE="/path/to/WsprryPi-support-HOST-UTC_TIMESTAMP.tar.gz"
REVIEW_DIR="$(mktemp -d "${TMPDIR:-/tmp}/wsprrypi-support-review.XXXXXX")"
chmod 700 "$REVIEW_DIR"
tar -xzf "$BUNDLE" -C "$REVIEW_DIR" --no-same-owner --no-same-permissions
printf 'Review directory: %s\n' "$REVIEW_DIR"
```

Each repeat creates a separate review directory and does not overwrite an earlier extraction. Delete that temporary directory with your file manager when you finish reviewing it.

Start with these files and directories:

- `bundle/README.txt` for the archive summary.
- `bundle/NEXT-STEPS.txt` for the generated handoff reminder.
- `bundle/configs` for configuration and service files.
- `bundle/logs` for application, Apache, installer, system, and kernel logs.
- `bundle/project` for checkout and installed-runtime information.
- `bundle/hardware`, `bundle/web`, `bundle/network`, and `bundle/commands` for their corresponding diagnostic reports.

Look especially for callsigns or other station identifiers, host/user names, IP addresses, project paths, URLs, and configuration values you do not want to make public. Do not edit the original archive after review; if it should not be public, ask the developer for a private sharing method.

## Attach the Bundle to a GitHub Issue

1. Open the relevant issue in the [WsprryPi repository](https://github.com/WsprryPi/WsprryPi/issues), or create one if the developer asks you to.
2. Add a comment describing what went wrong, what you expected, whether it is repeatable, and approximately when it happened. Timing helps the developer find the relevant log entries.
3. Drag the reviewed `.tar.gz` file into the comment box, or use the **Attach files** paperclip and select it.
4. Wait for GitHub to place the uploaded file link in the comment. Verify the attachment is present before submitting the comment.

GitHub currently supports `.gz` archives in issue comments and limits non-media attachments to 25 MB. If the bundle is larger, or if it contains information that should not be public, do not attach it to a public issue. Ask the developer for an approved private transfer method. Files attached to a public repository can be accessed without authentication. See GitHub's [Attaching files](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/attaching-files) documentation for the current rules.

The support-bundle API is restricted to loopback or a directly connected trusted LAN and checks the browser-visible host and origin. This is network-location access control, not user authentication. Only share a bundle with people you trust.

## Command-Line Alternative

The Maintenance workflow is recommended for most users because it handles consent, status, verified download, and Pi-side cleanup. The installed collector remains available for command-line troubleshooting:

```bash
/usr/local/lib/wsprrypi/collect-support-bundle.sh --help
```

Without an explicit private output directory, the command-line collector writes its archive, SHA-256 sidecar, and result JSON in the current directory. It does not upload them. Active I²C probing remains opt-in through `--probe-i2c`.
