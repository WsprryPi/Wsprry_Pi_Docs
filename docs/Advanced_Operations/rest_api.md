# REST API

WsprryPi exposes both an HTTP REST interface and a WebSocket interface for configuration, control, monitoring, and UI synchronization.

For persistent event and command connections, see {doc}`websocket`.

For normal browser and API use, access these interfaces through the Apache proxy path:

```text
http://{servername}.local/wsprrypi/
```

The WsprryPi backend still listens on its service ports internally:

- HTTP REST/UI backend: `31415`
- WebSocket backend: `31416`

Those ports are implementation details behind the proxy. Most users and documentation examples should use the proxied `/wsprrypi/` paths.

Apache is required for browser operation and uses the browser's actual peer
address for privileged network safety. Browser code does not fall back to the
direct backend ports for protected operations. Compatible direct non-browser
clients remain subject to peer, local `Host`, and optional matching `Origin`
validation. `Forwarded`, `X-Forwarded-For`, `X-Real-IP`, and similar headers do
not grant access.

The HTTP interface serves both the browser UI and the REST API through the proxied base path.

The UI entry point is:

```text
http://{servername}.local/wsprrypi/
```

## Configuration Endpoint

The primary proxied configuration endpoint is:

```text
http://{servername}.local/wsprrypi/config
```

Supported operations:

- `GET`: Returns the active runtime configuration as JSON
- `PUT`: Replaces the configuration with a full JSON payload
- `PATCH`: Updates selected configuration fields

The backend service receives this request internally as:

```text
http://127.0.0.1:31415/config
```

The API exposes configuration for:

- WSPR Type 2/3 support
- QRSS, FSKCW, and DFCW configuration
- Si5351 backend configuration
- Band GPIO selector configuration
- Amp Control GPIO support
- Web and WebSocket port configuration
- CW timing and fade configuration
- Planner preferences and paired-frame behavior

Configuration replacement and patch requests apply the same GPIO ownership validation as startup and INI reload. With the GPIO backend, the selected GPIO4 or GPIO20 RF output cannot also be used by an enabled Band GPIO, Transmit LED, Shutdown Button, or Amp Control, regardless of the `Operation.Transmit` value. A rejected request returns the conflict instead of clearing or moving either assignment.

With privileged network safety enforced, `PUT` and `PATCH` require a browser
peer on the Pi's directly connected LAN. `GET /config` remains read-only and
available where practical. Repair/reset, stop-and-disable, support-bundle
operations, and `POST /api/network-safety` are also protected. An off-LAN
request is rejected before the operation is proxied.

A typical payload resembles:

```json
{
    "Operation": {
        "Mode": "WSPR",
        "Transmit": true,
        "Transmit Backend": "gpio",
        "Use LED": true,
        "LED Pin": 18,
        "Use Amp": false,
        "Amp Pin": -1,
        "Amp Pin Active High": false,
        "Use Shutdown": true,
        "Shutdown Button": 19,
        "Web Port": 31415,
        "Socket Port": 31416
    },
    "Common": {
        "Call Sign": "AA0NT",
        "Grid Square": "EM18",
        "Power": 20,
        "Frequencies": "20m"
    },
    "GPIO": {
        "Transmit Pin": 4,
        "Power Level": 7,
        "Use NTP": true,
        "PPM": 0.0
    },
    "Band GPIO": {
        "20m": {
            "Enabled": true,
            "GPIO": 21,
            "Active High": true
        }
    },
    "Meta": {
        "Use INI": true,
        "INI Filename": "/usr/local/etc/wsprrypi.ini",
        "Date Time Log": true,
        "Loop TX": false,
        "TX Iterations": 0
    }
}
```

## RP1 GPCLK Route Endpoint

Pi 5 route controls use the bounded same-origin endpoint:

```text
GET  /wsprrypi/api/rp1-gpclk-route
POST /wsprrypi/api/rp1-gpclk-route
```

`GET` is read-only and reports requested, persisted, configured, active,
eligible, generation, journal, service-restoration status, and operator state.

For the installed runtime route profile, `POST` accepts these fixed operations:

- `preflight` validates a GPIO4 or GPIO20 switch and returns the current
  transaction generation and plan digest.
- `switch` applies the preflighted GPIO4 or GPIO20 route in the current boot.
- `remove` removes the exact active GPIO4 or GPIO20 route and restores the
  prior Wsprry Pi service intent.
- `recover` performs exceptional fail-closed cleanup and leaves Wsprry Pi
  stopped and inhibited.

`switch` requires the current generation; the service binds that generation to
the reviewed preflight digest.
`remove` names the exact route being removed. A successful switch or removal
response means the bounded operation was queued; clients must poll `GET` until
the route reaches a terminal state. A temporary disconnect is not proof of
success. Normal removal finishes as route neutral with Wsprry Pi either online
and idle, or still stopped or masked because that was its prior state.

The compatibility development profile retains `preflight`,
`apply-and-reboot`, and `rollback`. Runtime requests are never translated into
reboot operations. Unknown operations, routes, stale generations, non-idle
state, foreign boot content, and ownership conflicts fail closed.

The endpoint never accepts a shell command, arbitrary path, overlay name, or
reboot command. Active or neutral state is not inferred until read-only status
reconciliation succeeds.

## Network Safety Endpoint

The Maintenance page uses:

```text
GET  /wsprrypi/api/network-safety
POST /wsprrypi/api/network-safety
```

`GET` is read-only and reports whether configured and active state are known,
their values when known, and the exact status text. `POST` is protected and
accepts one explicit mode:

```json
{"mode":"enforced"}
```

or:

```json
{"mode":"insecure-disabled"}
```

The apply response distinguishes whether the request was applied and reports
configured and active state. When disabled, status is exactly `NETWORK SAFETY
OFF`. A failed validation, publish, Apache reload, confirmation, or rollback
must be treated as failure; do not infer active state from the requested value.

## Version Endpoint

Version and update metadata are available through the proxied endpoint:

```text
http://{servername}.local/wsprrypi/version
```

The backend service receives this request internally as:

```text
http://127.0.0.1:31415/version
```

Modern versions expose structured metadata:

```json
{
    "wspr_version": "3.0.0-rc.4+abcdef0 (devel)",
    "ui_version": "3.0.0-rc.4+abcdef0 (devel)",
    "ui_build_id": "mtime-1234567890abcdef",
    "wspr_version_raw": "3.0.0-rc.4+abcdef0",
    "wspr_branch": "devel",
    "wspr_branch_state": "branch",
    "wspr_commit": "abcdef0123456789",
    "wspr_build_dirty": false
}
```

This endpoint is used for:

- Browser UI version display
- Automatic update polling
- UI build reload detection
- Asset cache busting
- GitHub update comparison logic
