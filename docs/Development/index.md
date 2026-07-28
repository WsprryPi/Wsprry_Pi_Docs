# Wsprry Pi Development

Wsprry Pi is developed as a modular Raspberry Pi application with a native C++ backend and a separate Bootstrap-based web UI.

```{toctree}
:maxdepth: 1
:hidden:

Automatic Update Polling Internals <../User_Interface/Maintenance/update_check>
```

The project officially supports Raspberry Pi 5. GPIO RF transmission on Raspberry Pi 5 requires dedicated supported hardware rather than the older direct GPIO clock path used on earlier Raspberry Pi models.

## Build Environment

Current development builds are compiled directly on the target Raspberry Pi. This avoids distributing binaries that may depend on newer `GLIBC` versions than the user's installed operating system provides.

The project is currently built with `g++` from GCC 14:

```text
gcc (Debian 14.2.0-19) 14.2.0
```

The backend is developed in modern C++.

## Repository Layout

The top-level `WsprryPi` repository contains the main application source, configuration defaults, install scripts, documentation support, and several Git submodules.

The web UI is kept as a top-level submodule:

```text
WsprryPi-UI/
```

The native C++ support libraries are kept under:

```text
src/
```

## Submodules

Because of modularity, reuse, and licensing considerations, the central WsprryPi repository references these Git repositories as submodules.

### Web UI

- [WsprryPi-UI](https://github.com/WsprryPi/WsprryPi-UI): The Bootstrap-based Wsprry Pi web UI.

### Core Support Libraries

- [INI-Handler](https://github.com/WsprryPi/INI-Handler): A class for reading and writing formatted INI files.
- [LCBLog](https://github.com/WsprryPi/LCBLog): A logging class for formatting, writing, levels, and timestamps.
- [Mailbox](https://github.com/WsprryPi/Mailbox): A replacement interface for Broadcom mailbox communication.
- [MonitorFile](https://github.com/WsprryPi/MonitorFile): A class for watching a file for changes.
- [PPM-Manager](https://github.com/WsprryPi/PPM-Manager): A class for tracking and applying system clock PPM correction.
- [Signal-Handler](https://github.com/WsprryPi/Signal-Handler): A class for intercepting process signals such as `SIGINT` and allowing clean shutdown.
- [Singleton](https://github.com/WsprryPi/Singleton): A class for enforcing a single running instance.

### WSPR and Transmission Libraries

- [WSPR-Reference](https://github.com/WsprryPi/WSPR-Reference): Reference WSPR encoding and decoding support used for validation and compatibility.
- [WSPR-Transmitter](https://github.com/WsprryPi/WSPR-Transmitter): The transmission backend library that manages RF backend execution, timing, DMA-backed GPIO transmission where supported, and hardware-backed transmission paths.

## Current Submodule Layout

At the time this documentation was updated, the project used the following submodule paths:

```text
WsprryPi-UI
src/INI-Handler
src/LCBLog
src/Mailbox
src/MonitorFile
src/PPM-Manager
src/Signal-Handler
src/Singleton
src/WSPR-Reference
src/WSPR-Transmitter
```

## Development Notes

This organization keeps the main application focused on configuration, scheduling, runtime orchestration, command-line handling, REST/WebSocket service behavior, and web UI integration.

The submodules isolate reusable pieces such as:

- INI parsing
- logging
- mailbox communication
- file monitoring
- PPM correction
- signal handling
- single-instance locking
- WSPR reference behavior
- RF transmission backends

This modular layout makes it easier to update or replace lower-level components independently as hardware support evolves.

## Raspberry Pi 5 Support

Raspberry Pi 5 support is now official.

Because Raspberry Pi 5 hardware differs significantly from earlier Raspberry Pi models, supported transmission paths may require dedicated external hardware or backend-specific support. The older direct GPIO RF approach remains associated with earlier Raspberry Pi generations where that clocking path is supported.

## Web UI Development

The web UI lives in the `WsprryPi-UI` submodule. It provides the browser-based setup, operation, logging, and maintenance interface.

The main backend exposes REST and WebSocket interfaces used by the UI for:

- Reading and writing configuration
- Starting and stopping runtime actions
- Receiving transmission state updates
- Receiving configuration reload events
- Displaying version and update status
- Coordinating multi-tab browser behavior

## Backend Development

The native backend is responsible for:

- Command-line parsing
- INI and JSON configuration translation
- Runtime validation
- Scheduling
- RF backend selection
- GPIO control orchestration
- REST API service
- WebSocket service
- Update/version metadata exposure
- Integration with the web UI

## Build and Test Workflow

The project should be built from the `src` directory when using the existing make targets:

```bash
cd src
make -j$(nproc)
make -j$(nproc) release
```

Node.js is required for the complete runtime semantics validation target. Run it from the Raspberry Pi checkout:

```bash
cd ~/WsprryPi/src
make semantics-test
```

Targeted regression tests are also built and run from `src`.

Examples:

```bash
make -j$(nproc) build/bin/ui_source_regression_test
./build/bin/ui_source_regression_test

make -j$(nproc) build/bin/dial_frequency_semantics_test
./build/bin/dial_frequency_semantics_test
```

Additional tests may be available depending on the current branch and enabled build targets.
