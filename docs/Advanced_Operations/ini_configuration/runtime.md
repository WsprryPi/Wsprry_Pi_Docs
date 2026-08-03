# Runtime and Service Settings

Use these sections for process behavior, active transmission mode, service ports, transmission gating, and shared control GPIOs. For normal browser-based configuration, see [Setup Overview](../../User_Interface/Setup/index.md). Related operator references include [Configure Raspberry Pi I/O](../../User_Interface/Setup/Pi_IO/index.md), [REST API](../rest_api.md), [WebSocket Interface](../websocket.md), and [View Logs](../../User_Interface/Logs/index.md).

(meta-section)=
## Meta

The `[Meta]` section controls diagnostic logging.

```{literalinclude} default_wsprrypi.ini
:language: ini
:start-at: [Meta]
:end-before: [Operation]
```

(operation-section)=
## Operation

The `[Operation]` section selects the active mode and backend, gates RF transmission, configures service ports, and assigns shared indicator, amplifier, and shutdown controls.

```{literalinclude} default_wsprrypi.ini
:language: ini
:start-at: [Operation]
:end-before: [Calibration]
```

### Startup transmitter safety

`Enable on Boot` determines whether WsprryPi requests transmission after the daemon starts. Independently of that policy, every daemon start first attempts to place the configured transmitter backend in a disabled state. The Si5351 backend disables all clock outputs. The GPIO backend stops its DMA and clock path and returns the configured transmit GPIO to an input state.

If that startup operation fails, WsprryPi keeps the web and socket services available but inhibits WSPR scheduling, CW scheduling, manual launches, startup tones, and test tones. The inhibition is latched for the lifetime of the process and does not change the saved `Transmit` or `Enable on Boot` values.

To recover, correct the reported hardware or configuration problem and restart the WsprryPi service. A configuration reload or transmission toggle cannot clear the startup inhibition. See [Configuration Troubleshooting](../configuration_troubleshooting.md#startup-transmission-is-inhibited) for operator checks.

This protection begins when the daemon runs. Use a separate hardware inhibit when the transmitter must remain disabled during the earlier power-up and operating-system boot interval.
