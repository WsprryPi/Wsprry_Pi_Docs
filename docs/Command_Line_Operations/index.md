<!-- Grammar and spelling checked -->
# Command Line Operations

Wsprry Pi normally runs as a `systemd` service, but you can also work with it directly from the shell for testing and one-off transmissions.

## `systemd` Service

The `wsprrypi` executable is controlled by Linux `systemd`. It runs in the background after boot, and only one `wsprrypi` process is allowed at a time. Stop the daemon before taking manual control from the command line.

Useful service commands:

- `sudo systemctl status wsprrypi`: Show a status page for the running daemon.
- `sudo systemctl restart wsprrypi`: Restart the daemon and `wsprrypi` with it.
- `sudo systemctl stop wsprrypi`: Stop the daemon. The daemon will restart again upon reboot.
- `sudo systemctl start wsprrypi`: Start the daemon if it is not running.
- `sudo systemctl disable wsprrypi`: Disable the daemon from restarting on reboot.
- `sudo systemctl enable wsprrypi`: Enable the daemon to start on reboot if it is disabled.

## Command Line

To see the built-in help, run:

```text
$ wsprrypi -h

WsprryPi version 2.0 (main).

Usage:
 (sudo) wsprrypi [options] callsign gridsquare transmit_power frequency <f2> <f3> ...
 OR
 (sudo) wsprrypi --test-tone {frequency}

Options:
 -h, --help
 Display this help message.
 -v, --version
 Show the WsprryPi version.
 -i, --ini-file <file>
 Load parameters from an INI file.  Provide the path and filename.

See the documentation for a complete list of available options.
```

### Common Command Line Examples

To create a transmission you must either send a test tone or provide your callsign, grid square, transmit power, and frequency. Any command that causes RF output should be run with `sudo`.

Arguments may use either the short form with a single hyphen, such as `-h`, or the long form with a double hyphen, such as `--help`.

Examples:

- `wsprrypi --help`

  Display a brief help screen.

- `sudo wsprrypi --test-tone 780e3`

  Transmit a constant test tone at 780 kHz.

- `sudo wsprrypi N9NNN EM10 33 20m`

  Transmit a single WSPR message on 20 meters with no frequency offset calibration.

- `sudo wsprrypi --use-ntp N9NNN EM10 33 20m`

  Use NTP-based frequency calibration before transmitting.

- `sudo wsprrypi --repeat --terminate 7 --ppm 43.17 N9NNN EM10 33 10140210 0 0 0 0`

  Transmit slightly off-center on 30 meters every 10 minutes for seven transmissions using a fixed PPM correction.

- `sudo wsprrypi --repeat --offset --use-ntp N9NNN EM10 33 40m`

  Transmit repeatedly on 40 meters, apply NTP-based calibration, and randomize the offset to reduce collisions.

### Complete Command Line Listing

Command-line input falls into three groups: positional arguments, switches that take no value, and options that require a value. You can also load parameters from an INI file:

`wsprrypi -i /usr/local/etc/wsprrypi.ini`

If the required values are present in the INI file, no additional arguments are required. If you supply both an INI file and command-line options, the command line is applied after the INI values and overrides them. In some cases the INI file is updated with the revised parameters.

#### Positional Arguments

Four positional arguments exist and are required for WSPR transmissions unless they are supplied by the INI file:

- **Callsign**: Your six-character or shorter callsign.
- **Gridsquare**: Your four-character Maidenhead grid square.
- **Power**: Your transmit power in dBm.
- **Frequency** (list): The transmission frequency or list of frequencies, separated by spaces.

Example:

`wsprrypi N9NNN EM10 33 10140210 0 0 0 0`

#### No Arguments

The following commands require no arguments:

- `--help` or `-h`: Show the version and an abbreviated help listing, then exit.
- `--version` or `-v`: Show the current version, then exit.
- `--use-ntp` or `-n`: Use Network Time Protocol through `chrony` to adjust transmission frequency calibration.
- `--repeat` or `-r`: Repeat the frequency or loop through the list of frequencies indefinitely.
- `--offset` or `-o`: Apply a random offset to the transmission frequency.
- `--date-time-log` or `-D`: Apply a UTC timestamp, for example `2025-05-06 12:17:00.561 UTC`, to log lines shown on screen.

#### Arguments Required

These commands require an argument immediately after the option:

- `--ini-file` or `-i`: Load initial configuration from an INI file using a full or relative path.
- `--ppm` or `-p`: Apply a fixed PPM correction value from `-200.00` to `200.00`.
- `--terminate` or `-x`: Stop after a specific number of iterations.
- `--test-tone` or `-t`: Generate a test tone at the chosen frequency. This overrides the need for the positional transmission arguments.
- `--led_pin` or `-l`: Set the Raspberry Pi GPIO pin number, in BCM numbering, for the transmission indicator.
- `--shutdown_button` or `-s`: Set the Raspberry Pi GPIO pin number, in BCM numbering, for the shutdown button.
- `--power_level` or `-d`: Set the Raspberry Pi GPIO output power:
  - `0`: 2 mA or 3.0 dBm
  - `1`: 4 mA or 6.0 dBm
  - `2`: 6 mA or 7.8 dBm
  - `3`: 8 mA or 9.0 dBm
  - `4`: 10 mA or 10.0 dBm
  - `5`: 12 mA or 10.8 dBm
  - `6`: 14 mA or 11.5 dBm
  - `7`: 16 mA or 12.0 dBm
- `--web-port` or `-w`: Set the socket used for the configuration REST API. The default is `31415`.
- `--socket-port` or `-k`: Set the socket used for the web UI Web Socket server. The default is `31416`.

<!-- Not yet implemented - `--transmit-pin` or `-a`: The pin Raspberry Pi pin number, in BCM formatting (e.g., use "18" for GPIO4 or header pin 7) for the transmissions. -->
