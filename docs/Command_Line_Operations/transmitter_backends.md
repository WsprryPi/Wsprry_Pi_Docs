# Transmitter Backend Options

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

The GPIO backend is qualified on 80 m, 20 m, 15 m, and 10 m with production
pacing. Requests whose final RF frequency is in the 12 m, 6 m, or 2 m band
range are rejected before GPIO activation, whether entered as a band name or
an arbitrary frequency. This covers WSPR, CW modes, and Test Tone; Si5351 is
unaffected. A steady test tone is not sufficient evidence that WSPR modulation will decode. See
[GPIO Band Capabilities and Signal Quality](../FAQ/why_12m_looks_noisy.md).

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

- `--si5351-reference-source <external_tcxo|crystal>`
  Select an active external clock/TCXO or a passive crystal. Missing settings default to `external_tcxo`.

- `--si5351-crystal-load-capacitance <6|8|10>`
  Set the internal load capacitance used only with `--si5351-reference-source crystal`. The default is 10 pF.

- `--si5351-tx-output <CLK0\|CLK1\|CLK2>`  
  Select output clock. This option is not exposed in the Web UI.
