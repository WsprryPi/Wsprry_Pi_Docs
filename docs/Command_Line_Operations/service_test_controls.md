# Service, GPIO, and Test Controls

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
