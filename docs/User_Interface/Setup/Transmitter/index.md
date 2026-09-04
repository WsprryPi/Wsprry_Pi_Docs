# Transmitter Configuration Tab

The Transmitter tab on the Signal Setup page contains settings related to the active output hardware path and transmission behavior.

Use the **RF Output Path** switch to choose the transmitter backend. The switch
shows GPIO on the left and Si5351 on the right; switch it off for GPIO or on for
Si5351. The same RF Output panel then shows only the settings for that hardware.
On wide screens those controls share one row. On smaller screens they wrap or
stack without changing their order.

- **GPIO** - Available on earlier Raspberry Pi models and on Pi 5 when the
  installer-managed RP1 GPCLK provider and selected route are eligible.
- **Si5351** - If detected, the Si5351 may be used on any supported Raspberry Pi.

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

While the Raspberry Pi has two GPIO bus (0 and 1), at the time of this writing only Bus 1 should be used.

### I2C Address

The default I2C bus address for the Si5351 is 0x60.  It may be configured to 0x61 by pulling the A0 pin high.  Other models and clones may have different addresses.

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
