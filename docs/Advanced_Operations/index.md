# Advanced Operations

These topics cover the underlying controls and operating details behind WSPR and `wsprrypi`. Most users can stay in the web UI, but this page is useful when you need timing, calibration, or API details.

## Transmission Timing

This software uses system time to determine the start of WSPR transmissions, so keep the system clock synchronized to within one second. Use network time synchronization or set the time manually with `date`. A WSPR transmission starts on an even UTC minute and runs for about two minutes.

## Frequency Calibration

### GPIO-Based Transmissions

Starting in version 2.0, the installer replaces the default `ntpd` implementation with [Chrony](https://chrony-project.org/), which has proven more reliable for this application.

NTP tracks and calculates a PPM correction automatically. If your Pi is running NTP, use `--use-ntp` to query the latest correction before each WSPR transmission. Residual error can remain because of NTP loop delay, so this works best after the system has been powered on long enough for clock and temperature behavior to settle.

Frequency calibration matters because WSPR occupies a narrow band. The Raspberry Pi reference crystal has both static error and temperature-dependent drift. You can rely on NTP-based correction or apply a fixed PPM correction manually.

### Si5351-Based Transmissions

The Si5351 required a crystal reference, and it is this reference that will govern the transmission frequency calibration.  `chrony` is not used to calibrate this frequency, however you may manually adjust the calibration via the PPM offset configuration item.  In testing against a 27MHz crystal, no calibration was needed.

### AM Calibration

A practical manual method is to tune the transmitter near a medium-wave AM broadcast station, zero-beat the signal, and calculate the remaining frequency error from the known station frequency.

Suppose your local AM station is at 780 kHz. Use `--test-tone` to produce nearby tones, such as `780100`, until you achieve zero beat. If the zero-beat tone on the command line is `F`, calculate the correction as `ppm=(F/780000-1)*1e6`. You can then supply that value with `--ppm` on future transmissions.

## INI File

The daemon reads `wsprrypi.ini` for its execution parameters. In normal use there is rarely a reason to edit the file directly. The installer stores it in the user data directory:

```bash
$ ls -al /usr/local/etc/wsprrypi.ini
total 12
drwxr-xr-x  2 root root 4096 Feb 18 14:51 .
drwxr-xr-x 10 root root 4096 Sep 21 19:02 ..
-rw-rw-rw-  1 root root  171 Mar  6 19:47 wsprrypi.ini
```

The file uses standard INI syntax. It has four sections: `Meta`, `Operation`, `Calibration`, `GPIO`, `Si5351`, `WSPR`, `CW`, and `Band GPIO`. Blank lines and extra whitespace are ignored. Each setting is a key/value pair separated by an equals sign.

This is the default INI file that ships with the installation. Any comments in the file must begin with a semicolon (`;`).

```ini
; Created for WsprryPi version %SEMANTIC_VERSION%
; Copyright (C) 2023 - 2026 Lee C. Bussy (@LBussy)

[Meta]
debug_logging = False

[Operation]
; Mode:
; Active transmit mode.
; Valid values:
;   WSPR
;   QRSS
;   FSKCW
;   DFCW
Mode = WSPR

; Transmit:
; Global RF transmit gate. False prevents transmission and scheduling.
Transmit = False

; Transmit Backend:
; RF transmit backend.
; Valid values:
;   gpio    - Raspberry Pi GPCLK/PWM RF output
;   si5351  - Si5351 clock-generator RF output
Transmit Backend = gpio

; Use LED:
; Enable status LED output.
Use LED = False

; LED Pin:
; BCM GPIO used for LED status output.
LED Pin = 18

; Use Amp:
; Enables optional external amplifier control.
Use Amp = false

; Amp Pin:
; BCM GPIO used for optional external amplifier control.
; Leave blank to disable amplifier control.
Amp Pin =

; Amp Pin Active High:
; Controls amplifier GPIO polarity.
Amp Pin Active High = false

; Web Port:
; Port used for REST interface.
Web Port = 31415

; Socket Port:
; Port used for WebSocket interface.
Socket Port = 31416

; Use Shutdown:
; Enable shutdown button monitoring.
Use Shutdown = False

; Shutdown Button:
; BCM GPIO used for shutdown trigger.
Shutdown Button = 19


[Calibration]
; PPM:
; Frequency calibration in parts per million.
; Used directly by the Si5351 backend and whenever GPIO.Use NTP is false.
PPM = 0.0


[GPIO]
; Transmit Pin:
; BCM GPIO used for RF output when Transmit Backend = gpio.
; GPCLK0 is supported on BCM GPIO 4 or 20.
; Ignored by the Si5351 backend.
Transmit Pin = 4

; Power Level:
; GPIO backend RF output power setting.
; Valid range is 0 to 7.
Power Level = 7

; Use NTP:
; Apply NTP-based PPM correction for the GPIO backend.
; Ignored by the Si5351 backend, which uses Calibration.PPM only.
Use NTP = True


[Si5351]
; I2C Bus:
; Linux I2C bus number for the Si5351 device.
; Bus 1 usually maps to /dev/i2c-1 on Raspberry Pi systems.
I2C Bus = 1

; I2C Address:
; 7-bit Si5351 I2C address.
; 0x60 is the common default for many Si5351 breakout boards.
I2C Address = 0x60

; Reference Frequency:
; Si5351 crystal or reference input frequency in Hz.
; Typical modules use 27000000.
Reference Frequency = 27000000

; TX Output:
; Si5351 clock output used for transmit RF.
; Valid values:
;   CLK0
;   CLK1
;   CLK2
; Unused outputs are held in a safe non-transmitting state by WsprryPi.
; The internal parked PLL is a synthesis state, not an emitted parked RF output.
; This setting is configurable in INI and CLI; it is not exposed in the web UI.
TX Output = CLK0

; Power Level:
; Si5351 backend drive-strength level.
; Valid range is 1 to 4.
Power Level = 1


[WSPR]
; Call Sign:
; Your amateur radio callsign.
; Supports standard, compound, and extended WSPR formats.
Call Sign = NXXX

; Grid Square:
; Your Maidenhead grid locator.
Grid Square = ZZ99

; TX Power:
; Transmitter power in dBm.
TX Power = 20

; Frequency:
; WSPR band name or dial frequency in Hz.
Frequency = 20m

; Planner Preference:
; Controls how WsprryPi selects between single-frame and paired WSPR transmissions.
; Valid values:
;   auto
;   prefer_paired
;   require_paired
Planner Preference = auto

; Use Random Offset:
; Enable WSPR frequency randomization around the dial-derived RF frequency.
Use Random Offset = True


[CW]
; Message:
; Text transmitted by QRSS, FSKCW, or DFCW when the selected mode is non-WSPR.
; Numeric-looking text such as 73 remains a text message.
Message = 73

; Base Frequency:
; Base RF frequency for non-WSPR modes.
; Use whole-number Hz, or add Hz, kHz, MHz, or GHz to decimal values.
; QRSS transmits on this frequency.
; FSKCW uses this as the space frequency.
; DFCW uses this as the dot frequency.
Base Frequency = 14096900

; Shift Hz:
; Frequency shift in Hz for keyed dual-frequency CW modes.
; FSKCW mark frequency = Base Frequency + Shift Hz.
; DFCW dash frequency = Base Frequency + Shift Hz.
; QRSS ignores this field.
Shift Hz = 5

; Dot Seconds:
; Dot length in seconds for QRSS, FSKCW, and DFCW timing.
Dot Seconds = 3.0

; Intra Element Gap:
; QRSS/FSKCW gap between dots and dashes, expressed as a multiple of Dot Seconds.
Intra Element Gap = 1.0

; Inter Character Gap:
; QRSS/FSKCW gap between characters, expressed as a multiple of Dot Seconds.
Inter Character Gap = 3.0

; Inter Word Gap:
; QRSS/FSKCW gap between words, expressed as a multiple of Dot Seconds.
Inter Word Gap = 7.0

; DFCW Intra Element Gap:
; DFCW gap between equal-duration dot/dash symbols, expressed as a multiple of Dot Seconds.
; DFCW dot and dash symbols have the same duration and differ by frequency.
DFCW Intra Element Gap = 0.333333

; DFCW Inter Character Gap:
; DFCW gap between characters, expressed as a multiple of Dot Seconds.
DFCW Inter Character Gap = 1.0

; DFCW Inter Word Gap:
; DFCW gap between words, expressed as a multiple of Dot Seconds.
DFCW Inter Word Gap = 3.0

; Fade Shape:
; Envelope fade shape for QRSS, FSKCW, and DFCW events.
; Valid values: none, linear, raised_cosine.
Fade Shape = raised_cosine

; Fade In Ms:
; RF envelope fade-in duration in milliseconds.
Fade In Ms = 20

; Fade Out Ms:
; RF envelope fade-out duration in milliseconds.
Fade Out Ms = 20

; Fade Slice Ms:
; Advanced envelope approximation control for QRSS, FSKCW, and DFCW fades.
; Smaller values produce smoother duty-gated fades at higher switching cost.
; This does not change Fade In Ms or Fade Out Ms duration.
Fade Slice Ms = 2

; Start Minute:
; Minute after the top of the hour for scheduled QRSS/FSKCW/DFCW launches.
; Valid range: 0 to 59.
Start Minute = 0

; Repeat Minutes:
; Repeat interval in minutes for scheduled QRSS/FSKCW/DFCW launches.
; Must be greater than 0.
Repeat Minutes = 10


[Band GPIO]
; Per-band GPIO assignment for band switching (BCM numbering).
; Assign a GPIO number to enable switching for that band.
; Leave blank to disable switching for that band.
; The same GPIO may be assigned to multiple bands.
; "<band> Active High" controls polarity (default = false).

2200m = 
2200m Active High = false

630m = 
630m Active High = false

160m = 
160m Active High = false

80m = 
80m Active High = false

60m = 
60m Active High = false

40m = 
40m Active High = false

30m = 
30m Active High = false

22m = 
22m Active High = false

20m = 
20m Active High = false

17m = 
17m Active High = false

15m = 
15m Active High = false

12m = 
12m Active High = false

10m = 
10m Active High = false

6m = 
6m Active High = false

4m =
4m Active High = false

2m =
2m Active High = false
```

## Troubleshooting CW Configuration Saves

When a QRSS, FSKCW, or DFCW message would take longer than its configured repeat interval, Setup marks the Message field invalid and displays **Save failed** with the calculated duration and repeat interval. The invalid draft remains in the browser so it can be corrected, but it is not applied to the running configuration. Autosave resumes automatically when the adjusted duration is less than or equal to the repeat interval.

This inline state identifies a timing problem that can be corrected on the Setup page. Other configuration reload failures that cannot be tied safely to an editable field may still appear in the general reload-failure dialog and may require checking the application log or configuration file.

See {ref}`cw-message-too-long` for the duration inputs and correction steps.

## REST and WebSocket Interfaces

WsprryPi exposes both an HTTP REST interface and a WebSocket interface for configuration, control, monitoring, and UI synchronization.

For normal browser and API use, access these interfaces through the Apache proxy path:

```text
http://{servername}.local/wsprrypi/
```

The WsprryPi backend still listens on its service ports internally:

- HTTP REST/UI backend: `31415`
- WebSocket backend: `31416`

Those ports are implementation details behind the proxy. Most users and documentation examples should use the proxied `/wsprrypi/` paths.

## REST API

The HTTP interface serves both the browser UI and the REST API through the proxied base path.

The UI entry point is:

```text
http://{servername}.local/wsprrypi/
```

### Configuration Endpoint

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

### Version Endpoint

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

## WebSocket Interface

The WebSocket interface provides:

- Runtime state broadcasts
- Browser UI synchronization
- Configuration reload notifications
- Transmission lifecycle events
- Test-tone state updates
- Real-time control integration

For normal browser use, connect through the proxied WebSocket path:

```text
ws://{servername}.local/wsprrypi/socket
```

The backend service receives this connection internally as:

```text
ws://127.0.0.1:31416/socket
```

### Available Commands

Examples of supported commands include:

- `get_tx_state`
- `shutdown`
- `reboot`
- Runtime control and synchronization requests used by the browser UI

Example request:

```json
{"command":"get_tx_state"}
```

Example response:

```json
{"tx_state":true}
```

### Broadcast Events

As long as the socket remains connected, the server broadcasts runtime events to all connected clients.

#### Configuration Reload

Broadcast when the active configuration changes:

```json
{
    "state":"reload",
    "timestamp":"2025-05-06T16:43:02Z",
    "type":"configuration"
}
```

#### Transmission Start

Broadcast when a transmission begins:

```json
{
    "state":"starting",
    "timestamp":"2025-05-06T16:40:01Z",
    "type":"transmit"
}
```

#### Transmission Complete

Broadcast when a transmission finishes:

```json
{
    "state":"finished",
    "timestamp":"2025-05-06T16:41:51Z",
    "type":"transmit"
}
```

#### Transmission Cancelled

Broadcast when a transmission is stopped before completion:

```json
{
    "state":"cancelled",
    "timestamp":"2025-05-06T16:40:20Z",
    "type":"transmit"
}
```

#### Test Tone State

Broadcast during transient RF test tone operations:

```json
{
    "state":"starting",
    "type":"test_tone"
}
```

The browser UI relies heavily on these broadcasts for:

- Live status updates
- Modal synchronization
- Runtime control state
- Configuration refresh
- Multi-tab coordination
- Update notification behavior

## PWM Peripheral

The GPIO RF backend uses the Raspberry Pi PWM peripheral to time the frequency transitions of the output clock.

The Raspberry Pi sound subsystem also uses this peripheral, so sound activity during a WSPR transmission can interfere with transmission quality.

The install script disables the onboard audio path automatically, so most users do not need to make manual changes.

This restriction applies only to the direct GPIO RF backend. External hardware backends such as Si5351 are not affected.

## RF and Electrical Considerations

The GPIO RF backend produces a square-wave RF clock, so a low-pass filter is required.

Connect a low-pass filter through a DC-blocking capacitor to GPIO4 (`GPCLK0`) and a ground pin on the Raspberry Pi before connecting an antenna.

GPIO4 and ground are on header pins 7 and 9 respectively.

See:

- http://elinux.org/RPi_Low-level_peripherals

for Raspberry Pi pin layout details.

Examples of low-pass filters can be found here:

- http://www.gqrp.com/harmonic_filters.pdf

TAPR also offers a Raspberry Pi shield with filtering and amplification:

- https://www.tapr.org/kits_20M-wsprrypi-pi.html

The expected RF power output from the GPIO backend is configurable from the command line, INI file, or Web UI.

Even at low power levels, WSPR transmissions are commonly received over very long distances.

Because the Raspberry Pi does not strongly attenuate ripple and noise from the 5 V supply, use a regulated power supply with good ripple suppression.

Supply ripple can appear as mixing products centered around the transmit carrier, typically at 100 Hz or 120 Hz.

Do not expose GPIO pins to voltages or currents above the Raspberry Pi absolute maximum ratings.

GPIO4 outputs a 3.3 V digital clock with a maximum current of approximately 16 mA.

Do not:

- Short GPIO4 directly to ground
- Connect a resistive dummy load directly to the GPIO
- Connect external amplifier keying circuitry directly to GPIO pins

Use appropriate isolation when controlling external amplifiers.

Most amplifiers expect their control line to be switched relative to chassis ground, which usually requires:

- A relay
- An SSR
- A MOSFET driver
- Or another isolated switching stage

Do not connect amplifier keying inputs directly to Raspberry Pi GPIO pins.

A DC-blocking capacitor should always be used when connecting transformers, filters, or antennas to the GPIO RF output.

Antennas can also expose GPIO pins to:

- Static discharge
- Induced RF energy
- Lightning transients

Some form of isolation and protection is strongly recommended.
