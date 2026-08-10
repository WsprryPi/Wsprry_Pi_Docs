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

GPIO is qualified on 80 m, 20 m, 15 m, and 10 m with the production synthesis
pacing. WsprryPi rejects direct GPIO requests in the 12 m, 6 m, and 2 m band
ranges before transmitter activation. This applies to WSPR, CW modes, and Test
Tone; Si5351 is unaffected. See
[GPIO Band Capabilities and Signal Quality](../../FAQ/why_12m_looks_noisy.md)
for the measured boundary and why changing pacing or calibration does not make
the disqualified bands usable.

```{literalinclude} default_wsprrypi.ini
:language: ini
:start-at: [GPIO]
:end-before: [Si5351]
```

(si5351-section)=
## Si5351

The `[Si5351]` section configures the I2C device, reference frequency, reference hardware, transmit output, and drive strength. `Reference Source = external_tcxo` is the compatibility default for an active clock or TCXO. Select `crystal` only when a passive crystal is connected across XA/XB.

For a passive crystal, `Crystal Load Capacitance` accepts only `6`, `8`, or `10` pF and defaults to `10`. WsprryPi programs this value only in crystal mode. It retains the setting without applying it in `external_tcxo` mode, so TCXO users should not treat it as a calibration control.

```{literalinclude} default_wsprrypi.ini
:language: ini
:start-at: [Si5351]
:end-before: [WSPR]
```
