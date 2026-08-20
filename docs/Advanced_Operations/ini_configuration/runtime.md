# Runtime and Service Settings

Use these sections for process behavior, active transmission mode, service ports, transmission gating, and shared control GPIOs. For normal browser-based configuration, see [Setup Overview](../../User_Interface/Setup/index.md). Related operator references include [Configure Raspberry Pi I/O](../../User_Interface/Setup/Pi_IO/index.md), [REST API](../rest_api.md), [WebSocket Interface](../websocket.md), and [View Logs](../../User_Interface/Logs/index.md).

(meta-section)=
## Meta

The `[Meta]` section controls diagnostic logging.

```{literalinclude} default_wsprrypi.ini
:language: ini
:start-at: [Meta]
:end-before: [Security]
```

(security-section)=
## Security

The `[Security]` section controls privileged network-location access. This is
separate from ordinary Setup autosave.

```{literalinclude} default_wsprrypi.ini
:language: ini
:start-at: [Security]
:end-before: [Operation]
```

`enforced` is the default and recommended value. Missing, empty, malformed,
boolean-like, numeric, or unknown values also fail closed to enforced behavior
and produce a warning. Only the exact value `insecure-disabled` bypasses the
peer/subnet check for protected operations. It does not weaken Host, Origin,
CORS, malformed-request, method, command, forwarded-header, or ordinary
configuration validation.

Use the [Privileged Network Safety](../../User_Interface/Maintenance/network_safety.md)
panel to change this value through the validated Apache apply/reload transaction.
Do not edit it through normal Setup autosave.

(operation-section)=
## Operation

The `[Operation]` section selects the active mode and backend, gates RF transmission, configures service ports, and assigns shared indicator, amplifier, and shutdown controls.

```{literalinclude} default_wsprrypi.ini
:language: ini
:start-at: [Operation]
:end-before: [Experimental]
```

(experimental-frequency-section)=
## Experimental frequency policy

The `[Experimental]` section provides advanced CLI/INI-only controls for operators performing authorized experiments. These settings are intentionally absent from the Web UI and default to `false`.

```{literalinclude} default_wsprrypi.ini
:language: ini
:start-at: [Experimental]
:end-before: [Calibration]
```

`Allow Unqualified Frequency` permits a backend, hardware profile, band, and
mode combination whose recorded state is **Untested** or **Unqualified**. It
cannot make an **Unavailable** hardware plan usable. `Allow Non-Amateur
Frequency` additionally permits a frequency outside Wsprry Pi's recognized
amateur-band ranges, but only when `Allow Unqualified Frequency` is also
`true`.

These controls do not grant permission to transmit. The operator remains responsible for authorization, RF-path safety, filtering, and compliance with applicable rules.

When the process starts with `--ini-file`, Wsprry Pi loads these INI values
before processing the remaining CLI switches. A CLI `--allow-*` or `--no-*`
switch overrides the corresponding INI value at startup and does not rewrite
this file. Repeated switches are processed from left to right, so the last
occurrence wins. If a later change to this monitored file is accepted, the
reloaded INI values become the live settings for subsequent transmission
decisions. See [Experimental Frequency Policy](../../Command_Line_Operations/transmitter_backends.md#experimental-frequency-policy)
for concrete commands and the procedure for confirming the effective settings
of a running process.

### Startup transmitter safety

`Enable on Boot` determines whether WsprryPi requests transmission after the daemon starts. Independently of that policy, every daemon start first attempts to place the configured transmitter backend in a disabled state. The Si5351 backend disables all clock outputs. The GPIO backend stops its DMA and clock path and returns the configured transmit GPIO to an input state.

If that startup operation fails, WsprryPi keeps the web and socket services available but inhibits WSPR scheduling, CW scheduling, manual launches, startup tones, and test tones. The inhibition is latched for the lifetime of the process and does not change the saved `Transmit` or `Enable on Boot` values.

To recover, correct the reported hardware or configuration problem and restart the WsprryPi service. A configuration reload or transmission toggle cannot clear the startup inhibition. See [Configuration Troubleshooting](../configuration_troubleshooting.md#startup-transmission-is-inhibited) for operator checks.

This protection begins when the daemon runs. Use a separate hardware inhibit when the transmitter must remain disabled during the earlier power-up and operating-system boot interval.
