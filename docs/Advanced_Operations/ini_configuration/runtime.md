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
