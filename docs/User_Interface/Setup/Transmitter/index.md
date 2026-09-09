# Transmitter Configuration Tab

The Transmitter tab on the Signal Setup page contains settings related to the active output hardware path and transmission behavior.

Use the **RF Output Path** switch to choose between GPIO and Si5351. The switch
shows GPIO on the left and Si5351 on the right; switch it off for GPIO or on for
Si5351. The same RF Output panel then shows only the settings for that hardware.
On wide screens those controls share one row. On smaller screens they wrap or
stack without changing their order.

- **GPIO** - Available on earlier Raspberry Pi models and on Pi 5 when the
  installer-managed RP1 GPCLK provider and selected route are eligible.
- **Si5351** - If detected, the Si5351 may be used on any supported Raspberry Pi.
<!-- if-wsprrypico -->
- **Pico over USB** - Available through the separate, default-off development
  controls described below. The production USB adapter requires Linux.
<!-- endif-wsprrypico -->

## GPIO

GPIO-based transmissions are the typical method most people think of when they think of Wsprry Pi.  It uses a GPIO Pin attached to a clock generator on the Pi to transmit WSPR tones.

On Pi 5-family systems, the normal installer supplies and validates the RP1
GPCLK provider but leaves both routes unselected and output disabled.
Installation alone does not qualify either route or authorize transmission.

For the legacy GPIO backend, conducted testing qualifies 80 m, 20 m, 15 m, and 10 m with
the production pacing value. WsprryPi rejects legacy GPIO requests in the 12 m, 6 m,
and 2 m band ranges before transmitter activation. The restriction applies to
scheduled operation and Test Tone and does not limit the Si5351 backend. See
[GPIO Band Capabilities and Signal Quality](../../../FAQ/why_12m_looks_noisy.md).

There are only two choices when setting up the GPIO-based transmitter:

### Transmit Pin

GPIO4 and GPIO20 are the supported direct RF output choices. The selected pin is reserved by the GPIO backend even when transmission is disabled, because Wsprry Pi must retain ownership of the configured RF path for startup and safe-state handling.

On Pi 5, the route panel distinguishes **Requested** from **Active**. Selecting
the other pin or None creates a draft; it does not autosave or redirect
committed work. When the transmitter is completely idle, choose **Switch
route** for GPIO4 or GPIO20. Choose **Remove route** for None. Choose **Cancel**
to restore the persisted selection without changing the Pi.

Switching and removal happen in the current boot and do not require a reboot.
The status dialog remains visible through the brief controller disconnect and
checks the result without repeating the operation. If Wsprry Pi was running,
successful removal brings it back online and idle. A service that was already
stopped or administrator-masked remains stopped or masked.

The panel distinguishes checking, plan ready, switching, restoring, route
selected, removing, route removed, service stopped, restoration failed, and
recovery-required states. Transmission remains disabled during an unresolved
transaction. **Recover to no route** is an exceptional fail-closed action: it
leaves Wsprry Pi stopped and the controller inhibited for investigation. Use
**Remove route** for normal removal. See [Raspberry Pi 5 RP1 GPCLK](../../../Advanced_Operations/rp1_gpclk.md)
for recovery guidance.

Wsprry Pi permits RP1 transmission only when the route and eligibility
evidence agrees exactly.

The other pin remains available on the **Pi I/O** tab. Selecting the Si5351 backend releases both GPIO4 and GPIO20 for ordinary GPIO roles; the retained GPIO transmit-pin value is ignored while Si5351 is selected.

If an existing configuration assigns the selected RF pin to an enabled ordinary GPIO role, both controls remain visible and are marked invalid until one assignment is changed or disabled. Invalid edits are not saved.

### GPIO Power Level

These are output driver strength levels mapped within the Pi's GPIO registers.  You may adjust the output from 0-7 with the slider.  The values roughly align to power levels at the pin before any amplification or filtering:

1. 2 mA: ~-7.0 dBm
2. 4 mA - ~-1.0 dBm
3. 6 mA - ~2.6 dBm
4. 8 mA - ~5.1 dBm
5. 10 mA - ~7.0 dBm
6. 12 mA - ~8.6 dBm
7. 14 mA - ~9.9 dBm
8. 16 mA - ~11.1 dBm

Actual output should be measured with the entire circuit and antenna.

## Si5351

The Si5351 is selectable as an output device on all supported Pi versions. If
the application cannot validate communication with the Si5351, the RF Output
panel reports that the device was not detected.

### I2C Bus

Choose one of the I2C buses detected on the Raspberry Pi. Wsprry Pi lists only
buses currently exposed by Linux with a corresponding I2C device. If the saved
bus is no longer available, it remains identified as unavailable but cannot be
selected; choose another listed bus explicitly. Enable or attach an I2C bus,
then reload the page to refresh the list.

A listed bus confirms only that the Linux adapter is present. It does not
confirm access permissions, external-header routing, wiring, power, or an
attached Si5351.

### I2C Address

After a bus is selected, Wsprry Pi checks addresses `0x60` through `0x6F` and
lists only addresses that respond to the Si5351 register-read check. The saved
address remains selected only while it is detected on that bus. If it is
missing, the menu has no selection; choose a detected address explicitly.

The menu distinguishes discovery in progress, no compatible response, and a
discovery error. Select the bus again or reload the page to retry after fixing
wiring, power, permissions, or I2C configuration.

The standard Si5351 address is `0x60`; some boards support `0x61`, and
compatible devices or clones may use another address in the supported range.
The Si5351 does not provide a definitive silicon-identification register, so a
listed address means that a register-compatible device responded. Verify the
attached hardware before transmitting.

### Reference Frequency

You must configure the reference frequency installed on the clock-generator board. QRP Labs synthesizer kits are supplied with a 27 MHz crystal and support optional TCXO configurations; Adafruit breakout boards use a 25 MHz crystal. Either reference can generate many supported frequencies.

For qualified 2 m WSPR operation, use a 27 MHz reference. [QRP Labs selected 27 MHz](https://qrp-labs.com/images/synth/synth_assembly6.pdf) because its synthesis calculations preserve WSPR tone spacing through 145 MHz, while its 25 MHz configuration does not. Wsprry Pi's current planner can calculate the four 2 m tones from a 25 MHz reference, but Wsprry Pi has physically qualified only its 27 MHz reference configuration on 2 m. A 25 MHz reference therefore remains unqualified for 2 m rather than proven incompatible.

Enter the frequency that corresponds to the installed reference hardware.

### Reference Source

Choose **External clock / TCXO** for a module driven by an active reference. This is the default and preserves existing behavior. Choose **Passive crystal** only when a crystal is connected across the Si5351 XA/XB pins.

When **Passive crystal** is selected, the **Crystal Load Capacitance** menu appears with 6, 8, and 10 pF choices. Select the value specified for the installed crystal; 10 pF is the default. The menu is hidden and its value is not programmed when **External clock / TCXO** is selected.

### Si 5351 Power Level

The Si5351 has four configurable power levels:

1. 2mA - ~0 to +3 dBm
2. 4mA - ~+3 to +6 dBm
3. 6mA - ~+6 to +8 dBm
4. 8mA - ~+8 to +10 dBm

While these are technically feasible levels, the device is not intended to drive a load.  It should be followed by an amplifier of some sort.


<!-- if-wsprrypico -->
## Pico development controls

Enable **Show Pico development controls** to reveal the **Pico output** panel.
This switch defaults off and saves only a browser preference. Hiding the panel
preserves the saved output selection and field drafts. If Pico remains selected,
the page says so beside the switch.

**Use Pico over USB** is the separate, persisted output selection. Keep
transmission disabled while configuring it. Disable TX LED, amplifier,
shutdown-button and band GPIO controls first; host GPIO calibration and CW
fades do not apply. Set host PPM to zero.

Enter **Endpoint path**, **USB serial**, **Device identity**, **USB vendor ID**
and **USB product ID** for the attached Pico's dedicated WTP function. Do not
use its Console port. The USB IDs are decimal; the device identity is 32
lowercase hexadecimal characters. See the
[WTP INI reference](../../../Advanced_Operations/ini_configuration/transmitter_backends.md#pico-wtp)
for exact requirements.

**Maximum start uncertainty (ns)** defaults to 1000000 (1 ms). The Pico's own
clock evidence must meet this limit. The host also needs synchronized UTC;
neither the USB connection nor GPSDO frequency discipline alone supplies the
Pico with valid UTC. **Allow device frequency rounding** accepts the device's
reported realizable frequencies and does not qualify RF accuracy.

These controls expose development integration. Continuous **Test Tone** is
unavailable with Pico; complete finite jobs run using the Pico's local timing.
Revealing or hiding the panel neither starts transmission nor clears a fault.

### Pico status and recovery

**Pico status** shows **Output observed**, **Host UTC**, **Device / boot** and
**Last job**. These are recorded observations, not electrical measurements.
Check their age and any reported failure. An unavailable status response means
unknown; it does not establish that the Pico is stopped. A previous job failure
remains in the history after cleanup.

If a job or connection becomes unresolved, disable transmission and review the
reported state. **Reconcile Pico** checks an idle device or reconnects the
current session to resolve its owned job. Recovery may stop that job. It never
resumes transmission, reloads an uncertain job or takes another owner's job.
After successful reconciliation, review the current observation and configuration
before explicitly enabling transmission again.

Status polling does not perform recovery. A changed device or boot identity,
foreign ownership, or unresolved output blocks further work. Restarting the
host creates a new session and does not adopt the old session's job. Closing
USB or exiting the host application is not proof of RF shutdown.
<!-- endif-wsprrypico -->
