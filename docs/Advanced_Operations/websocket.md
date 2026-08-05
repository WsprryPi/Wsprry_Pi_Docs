# WebSocket Interface

The WebSocket interface provides:

- Runtime state broadcasts
- Browser UI synchronization
- Configuration reload notifications
- Transmission lifecycle events
- Test-tone state updates
- Real-time control integration

For normal browser use, connect through the proxied WebSocket path:

```text
ws://{servername}.local/wsprrypi/socket
```

The backend service receives this connection internally as:

```text
ws://127.0.0.1:31416/socket
```

## Available Commands

Examples of supported commands include:

- `get_tx_state`
- `shutdown`
- `reboot`
- Runtime control and synchronization requests used by the browser UI

Example request:

```json
{"command":"get_tx_state"}
```

Example response:

```json
{"tx_state":true}
```

## Broadcast Events

As long as the socket remains connected, the server broadcasts runtime events to all connected clients.

### Configuration Reload

Broadcast when the active configuration changes:

```json
{
    "state":"reload",
    "timestamp":"2025-05-06T16:43:02Z",
    "type":"configuration"
}
```

### Transmission Start

Broadcast when a transmission begins:

```json
{
    "state":"starting",
    "timestamp":"2025-05-06T16:40:01Z",
    "type":"transmit"
}
```

### Transmission Complete

Broadcast when a transmission finishes:

```json
{
    "state":"finished",
    "timestamp":"2025-05-06T16:41:51Z",
    "type":"transmit"
}
```

### Transmission Cancelled

Broadcast when a transmission is stopped before completion:

```json
{
    "state":"cancelled",
    "timestamp":"2025-05-06T16:40:20Z",
    "type":"transmit"
}
```

### Test Tone State

Broadcast during transient RF test tone operations:

```json
{
    "state":"starting",
    "type":"test_tone"
}
```

Test Tone Start and End requests are transactionally serialized across client
handler threads. Each lifecycle operation remains serialized through its result
broadcast before the next request is processed. After a timeout or disconnect,
the RF state may be unknown; clients must preserve access to End until the
controller confirms that the tone has stopped.

The browser UI relies heavily on these broadcasts for:

- Live status updates
- Modal synchronization
- Runtime control state
- Configuration refresh
- Multi-tab coordination
- Update notification behavior
