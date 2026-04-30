
# Command Line Options

Wsprry Pi normally runs as a `systemd` service, but you can also work with it
directly from the shell for testing, calibration, and one-off transmissions.

---

## `systemd` Service

The `wsprrypi` executable is managed by Linux `systemd`. It runs in the
background after boot, and only one instance is allowed at a time. Stop the
daemon before running manual CLI commands.

Useful commands:

- `sudo systemctl status wsprrypi`  
  Show current status and recent logs.

- `sudo systemctl restart wsprrypi`  
  Restart the daemon and reload configuration.

- `sudo systemctl stop wsprrypi`  
  Stop the daemon. It will start again on reboot unless disabled.

- `sudo systemctl start wsprrypi`  
  Start the daemon manually.

- `sudo systemctl disable wsprrypi`  
  Prevent daemon startup on boot.

- `sudo systemctl enable wsprrypi`  
  Enable daemon startup on boot.

---

## Command Line Overview

The CLI supports two primary modes:

- **Direct CLI mode**  
  Run WSPR or CW-based transmissions directly.

- **INI (daemon-style) mode**  
  Use `-i` to load and monitor a configuration file.

### Usage

```text
(sudo) wsprrypi [options] CALLSIGN GRID POWER FREQ [FREQ...]
(sudo) wsprrypi -i /path/to/wsprrypi.ini
(sudo) wsprrypi --test-tone RF_FREQ [backend/options]
(sudo) wsprrypi --mode QRSS --cw-message TEXT --cw-base-frequency FREQ
```

---

## Common Examples

- `wsprrypi --help`  
  Display help text.

- `sudo wsprrypi --test-tone 780e3`  
  Transmit a constant RF tone at 780 kHz.

- `sudo wsprrypi N9NNN EM10 33 20m`  
  Transmit a single WSPR message.

- `sudo wsprrypi --use-ntp N9NNN EM10 33 20m`  
  Use NTP calibration before transmission.

- `sudo wsprrypi --repeat --offset --use-ntp N9NNN EM10 33 40m`  
  Continuous transmissions with offset randomization.

---

## Positional Arguments

These are required for direct WSPR transmission unless provided via INI:

- **CALLSIGN**  
  Your callsign or supported WSPR identity form. Standard Type 1 WSPR
  messages use a normal callsign that fits the classic WSPR field. When the
  supplied identity cannot be represented as a single Type 1 message, the
  planner can use paired WSPR message planning where supported. This allows
  Type 2 and Type 3 message forms for extended callsign/grid combinations
  rather than requiring every direct CLI transmission to fit the older
  six-character Type 1-only form.

- **GRID**  
  Maidenhead grid square or locator value used by the WSPR planner. Standard
  Type 1 messages use the normal four-character Maidenhead grid square. For
  identities that require paired planning, the grid and callsign are evaluated
  together so the planner can select the appropriate Type 2/Type 3-capable
  message strategy when available.

- **POWER**  
  Transmit power in dBm. The value is rounded to valid WSPR steps and included
  in the transmitted WSPR message where the selected message type supports it.

- **FREQ**  
  One or more frequencies or band aliases.  
  Examples: `20m`, `14097100`, `0` (skip slot)

---

## General Options

- `-h`, `--help`  
  Display help text and exit. This is processed early and does not require root.

- `-v`, `--version`  
  Print version information and exit.

- `-i`, `--ini-file <file>`  
  Load configuration from an INI file. When used, CLI transmission options are
  disabled or restricted, and the program runs in daemon-style mode.

- `-r`, `--repeat`  
  Repeat transmissions indefinitely in direct CLI mode.

- `-x`, `--terminate <count>`  
  Stop after a specified number of transmissions.

- `-J`, `--journald`  
  Send logs to the systemd journal instead of stdout.

- `-D`, `--date-time-log`  
  Prefix log lines with UTC timestamps.

- `--debug-logging`, `--no-debug-logging`  
  Enable or disable debug-level logging output.

---

## WSPR Behavior

- `--planner-preference <auto\|prefer_paired\|require_paired>`  
  Controls WSPR message planning. The default `auto` mode uses a normal single
  WSPR frame when possible and allows the planner to choose paired handling when
  needed. `prefer_paired` asks the planner to use paired handling when it is
  available. `require_paired` rejects a transmission if the supplied identity
  cannot be represented with the paired-message strategy.

- `-o`, `--offset`  
  Apply a small random frequency offset to reduce collisions.

- `--no-offset`  
  Disable random offset.

### WSPR Message Types

The CLI is no longer limited to classic Type 1-only callsign handling. Direct
CLI WSPR input is passed through the same WSPR planning path used by the rest
of the application.

- **Type 1** is the normal single-frame WSPR message form for standard
  callsign, grid, and power combinations.
- **Type 2** supports compound or extended identity cases by transmitting a
  callsign-hash-oriented frame as part of a paired strategy.
- **Type 3** supports the complementary extended identity information needed
  for paired decoding.

For ordinary callsigns and four-character grid squares, no special option is
usually needed. For identities that require Type 2/Type 3 handling, use
`--planner-preference` when you want to prefer or require paired planning.

---

## Backend Selection

- `--backend <gpio\|si5351>`  
  Select RF output method.  
  - `gpio`: Direct RF from Raspberry Pi GPIO (limited models).  
  - `si5351`: External clock generator via I2C.

- `--power-level <level>`  
  Set transmit power for the active backend:  
  - GPIO: 0–7  
  - Si5351: 1–4

- `--gpio-power-level <0-7>`  
  Explicitly set GPIO drive strength.

- `--si5351-power-level <1-4>`  
  Set Si5351 output drive strength.

---

## GPIO Backend

- `--transmit-gpio <4\|20>`  
  Select GPIO pin used for RF output.

- `--transmit-pin <4\|20>`  
  Legacy alias for transmit GPIO.

- `-n`, `--use-ntp`  
  Enable NTP-based frequency calibration.

- `--no-use-ntp`  
  Disable NTP calibration and use manual PPM.

- `-p`, `--ppm <value>`  
  Apply manual frequency correction (-200 to 200 ppm).

---

## Si5351 Backend

- `--si5351-i2c-bus <bus>`  
  Select I2C bus (default: 1).

- `--si5351-i2c-address <addr>`  
  Set device address (decimal or hex).

- `--si5351-reference-frequency <hz>`  
  Define reference oscillator frequency.

- `--si5351-tx-output <CLK0\|CLK1\|CLK2>`  
  Select output clock. This option is not exposed in the Web UI.

---

## CW / QRSS / FSKCW / DFCW Modes

- `--mode <WSPR\|QRSS\|FSKCW\|DFCW>`  
  Select transmission mode.

- `--cw-message <text>`  
  Message to transmit in CW-based modes.

- `--cw-base-frequency <freq>`  
  Base RF frequency. Supports Hz, kHz, MHz, GHz suffixes.

- `--cw-shift-hz <hz>`  
  Frequency shift for FSK-based modes.

- `--cw-dot-seconds <seconds>`  
  Length of a Morse "dot".

### Timing

- `--cw-start-minute <0-59>`  
  Start minute for scheduled transmissions.

- `--cw-repeat-minutes <minutes>`  
  Interval between transmissions.

### Spacing

- `--cw-intra-element-gap <multiple>`  
  Gap between elements of a character.

- `--cw-inter-character-gap <multiple>`  
  Gap between characters.

- `--cw-inter-word-gap <multiple>`  
  Gap between words.

### Envelope Control

- `--cw-fade-shape <none\|linear\|raised_cosine>`  
  Shape of amplitude transitions.

- `--cw-fade-in-ms <ms>`  
  Fade-in duration.

- `--cw-fade-out-ms <ms>`  
  Fade-out duration.

- `--cw-fade-slice-ms <ms>`  
  Resolution of fade steps.

---

## Service and GPIO Controls

- `--no-web`  
  Disable Web UI and WebSocket server.

- `-w`, `--web-port <port>`  
  HTTP REST API port (default: 31415).

- `-k`, `--socket-port <port>`  
  WebSocket port (default: 31416).

- `-l`, `--led_pin <gpio>`  
  Set TX LED GPIO.

- `--led-pin <gpio>`  
  Alias for LED pin.

- `--use-led`, `--no-led`  
  Enable or disable LED.

- `-s`, `--shutdown_button <gpio>`  
  Set shutdown button GPIO.

- `--shutdown-button <gpio>`  
  Alias.

- `--use-shutdown`, `--no-shutdown`  
  Enable or disable shutdown monitoring.

---

## Test Tone

- `-t`, `--test-tone <frequency>`  
  Generate a continuous RF tone. Useful for calibration and testing.

---

## Notes

- CLI options override INI values unless restricted.
- Some advanced features are CLI-only.
- Root privileges (`sudo`) are required for RF output.
