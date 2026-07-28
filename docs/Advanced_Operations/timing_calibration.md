# Transmission Timing and Calibration

Use these procedures when transmission timing or RF frequency accuracy needs direct attention beyond normal web UI operation.

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
