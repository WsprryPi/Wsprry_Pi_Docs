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
