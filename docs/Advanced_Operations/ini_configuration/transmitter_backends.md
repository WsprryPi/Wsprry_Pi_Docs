# Calibration and Transmitter Backends

Use these sections for frequency calibration and RF output-path settings. See [Configure Transmitter](../../User_Interface/Setup/Transmitter/index.md), [Configure Raspberry Pi I/O](../../User_Interface/Setup/Pi_IO/index.md), [Transmission Timing and Calibration](../timing_calibration.md), [Transmitter Backend Options](../../Command_Line_Operations/transmitter_backends.md), and [RF and Electrical Reference](../rf_electrical.md) for the corresponding workflows.

(calibration-section)=
## Calibration

The `[Calibration]` section supplies **Reference calibration (PPM)** for the Si5351 backend. GPIO calibration uses the separate values in `[GPIO]`.

```{literalinclude} default_wsprrypi.ini
:language: ini
:start-at: [Calibration]
:end-before: [GPIO]
```

(gpio-section)=
## GPIO

The `[GPIO]` section configures the supported direct RF pin, GPIO-backend power level, provider-derived system clock estimate, conducted residual, and fixed/manual fallback. When `Operation.Transmit Backend = gpio`, the configured transmit pin is reserved even if `Operation.Transmit = false`. The other supported transmit pin remains available to ordinary GPIO roles. When the Si5351 backend is selected, a retained GPIO transmit-pin value reserves nothing.

GPIO qualification depends on the Raspberry Pi clock profile, band, and
transmission mode. Requests for unqualified combinations are blocked by default,
while combinations the backend cannot construct remain unavailable. Check the
[Band qualification](../../About_Wsprry_Pi/index.md#band-qualification) table
and its numbered notes for the current mode-specific status. See
[GPIO Band Capabilities and Signal Quality](../../FAQ/why_12m_looks_noisy.md)
for the measured signal-quality findings.

```{literalinclude} default_wsprrypi.ini
:language: ini
:start-at: [GPIO]
:end-before: [Si5351]
```

(si5351-section)=
## Si5351

The `[Si5351]` section configures the I2C device, reference frequency, reference hardware, transmit output, and drive strength. `Reference Source = external_tcxo` is the compatibility default for an active clock or TCXO. Select `crystal` only when a passive crystal is connected across XA/XB.

`I2C Address` accepts decimal or `0x`-prefixed hexadecimal values from `0x60`
through `0x6F` inclusive. The web interface further limits its address menu to
register-compatible devices detected on the selected, host-present I2C bus.
Direct CLI and INI configuration still undergo range and transmission-readiness
validation.

For a passive crystal, `Crystal Load Capacitance` accepts only `6`, `8`, or `10` pF and defaults to `10`. WsprryPi programs this value only in crystal mode. It retains the setting without applying it in `external_tcxo` mode, so TCXO users should not treat it as a calibration control.

```{literalinclude} default_wsprrypi.ini
:language: ini
:start-at: [Si5351]
:end-before: [WSPR]
```


<!-- if-wsprrypico -->
(wtp-section)=
## Pico WTP

Set `[Operation] Transmit Backend = wtp` to select a Pico on Linux. Keep
`Transmit = false` and `Enable on Boot = Never` while configuring and checking
the endpoint. The inactive WTP defaults have empty identities and zero USB IDs;
selecting WTP requires complete, valid values.

| Setting in `[WTP]` | Value and purpose |
| --- | --- |
| `Endpoint` | Dedicated WTP character-device path under `/dev/`. A stable `/dev/serial/by-id/` alias is accepted after identity checks. The Console interface is rejected. |
| `USB Serial` | Exact USB serial string, preserving leading zeros. |
| `USB Vendor ID` | Decimal USB vendor ID, from 1 through 65535. |
| `USB Product ID` | Decimal USB product ID, from 1 through 65535. |
| `Device ID` | WTP device identity from HELLO: 32 lowercase hexadecimal characters. |
| `Start Uncertainty ns` | Maximum permitted start uncertainty, from 1 through 1000000000 nanoseconds. Default: 1000000 (1 ms). |
| `Allow Frequency Adjustment` | Default: `false`. Explicitly permits the device's reported realizable frequency rounding; it does not establish RF accuracy. |

Obtain identities from the attached device rather than copying another board's
values. USB identity, WTP device identity and the current boot identity serve
different checks. A changed USB path alone does not identify a replacement.

The host requires synchronized UTC with at most 500 ms reported maximum error.
The Pico separately needs valid UTC within the configured start-uncertainty
budget and its own clock limits. Wsprry Pi observes that clock; USB does not
provision it. Raising the budget is an explicit acceptance decision, not clock
calibration or proof of start accuracy.

Set host `[Calibration] PPM = 0.0`. Disable TX LED, amplifier, shutdown-button
and band-selector GPIO controls, including per-frequency `@` selectors. CW fades
are unsupported. Settings for inactive GPIO and Si5351 backends are retained.
An unresolved WTP session blocks endpoint or backend replacement until its state
is resolved.

See [Pico development controls](../../User_Interface/Setup/Transmitter/index.md#pico-development-controls)
for selection, status and recovery. Keep transmission disabled until configuration,
clock evidence and the intended RF path have been checked.
<!-- endif-wsprrypico -->
