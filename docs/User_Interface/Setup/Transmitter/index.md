# Transmitter Configuration Tab

The Transmitter tab on the Signal Setup page contains settings related to the active output hardware path and transmission behavior.

![Transmitter Configuration](Signal_Setup_Transmitter.png)

Use this page to choose the transmitter backend and review the hardware-specific configuration required for your station.  Either the GPIO or Si5351 is chosen to display contextual setup fields.

![Transmitter Type](select_output.png)

- **GPIO** - Available on the Raspberry Pi models before the Pi 5.
- **Si5351** - If detected, the Si5351 may be used on any supported Raspberry Pi.

## GPIO

GPIO-based transmissions are the typical method most people think of when they think of Wsprry Pi.  It uses a GPIO Pin attached to a clock generator on the Pi to transmit WSPR tones.

It is available to select on all Pi versions before the Pi 5.

![GPIO Configuration](GPIO.png)

There are only two choices when setting up the GPIO-based transmitter:

### Transmit Pin

GPIO4 is the most common pin used.  GPIO20 is technically possible to use, however this has not been tested.  It is there in case you wish to experiment.

### Power Level

These are output driver strength levels mapped within the Pi's GPIO registers.  You may adjust the output from 0-7 with the slider.  The values roughly align to power levels at the pin before any amplification or filtering:

- 0 - 2 mA
- 1 - 4 mA
- 2 - 6 mA
- 3 - 8 mA
- 4 - 10 mA
- 5 - 12 mA
- 6 - 14 mA
- 7 - 16 mA

Actual output should be measured with the entire circuit and antenna.

## Si5351

The Si5351 is selectable as an output device on all supported Pi versions.  If the application cannot validate communication with the Si5351, it will show that it is not detected when viewed in the dropdown.

### I2C Bus

While the Raspberry Pi has two GPIO bus (0 and 1), at the time of this writing only Bus 1 should be used.

### I2C Address

The default I2C bus address for the Si5351 is 0x60.  It may be configured to 0x61 by pulling the A0 pin high.  Other models and clones may have different addresses.

### Reference Frequency

You must have a reference frequency to govern the clock generator.  QRP Labs breakout boards use a 27MHz TCXO, where the Adafruit breakouts I have seen use 25MHz.  Either will work fine for most frequencies.  QRP Labs has shared in some notes that 25MHz fails to divide to frequencies that can cleanly support 2M transmissions, so they have standardized on 27MHz.

Enter the frequency here that corresponds to your installed TCXO.

### Power Level

The Si5351 has four configurable power levels:

1. 2mA - ~0 to +3 dBm
2. 4mA - ~+3 to +6 dBm
3. 6mA - ~+6 to +8 dBm
4. 8mA - ~+8 to +10 dBm

While these are technically feasible levels, the device is not intended to drive a load.  It should be followed by an amplifier of some sort.
