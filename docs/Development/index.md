<!-- Grammar and spelling checked -->
# Wsprry Pi Development

All current development has been done with `g++` version `gcc (Debian 14.2.0-19) 14.2.0` (C++20).  The compilation is done on on the user's Pi to allow the compiled executable to run regardless of the `GLIBC` library versions.

Because of modularity, re-use, and licensing considerations, the central WsprryPi repository references the following Git Repositories as submodules:

- [WsprryPi-UI](https://github.com/WsprryPi/WsprryPi-UI): The Bootstrap-based Wsprry Pi Web UI.
- [Mailbox](https://github.com/WsprryPi/Mailbox): A replacement for Broadcom's interface for Mailbox communication.
- [INI-Handler](https://github.com/WsprryPi/INI-Handler): A class that allows reading and wriging formatted INI cfiles.
- [LCBLog](https://github.com/WsprryPi/LCBLog): A class to handle log formatting, writing, and timestamps.
- [MonitorFile](https://github.com/WsprryPi/MonitorFile): A class to watch a file for changes.
- [PPM-Manager](https://github.com/WsprryPi/PPM-Manager): A class to maintain an eye on the current PPM value for the OS/clock.
- [Signal-Handler](https://github.com/WsprryPi/Signal-Handler): A class to intercept various signals (e.g. SIGINT), and allow proper handling.
- [Singleton](https://github.com/WsprryPi/Singleton): A class that enforces running only a single instance.
- [WSPR-Message](https://github.com/WsprryPi/WSPR-Message): A class that creates WSPR symbols from the callsign, gridsquare, and power in dBm.
- [WSPR-Transmitter](https://github.com/WsprryPi/WSPR-Transmitter): A class that manages DMA work and scheduling for transmistting WSPR symbols.

In theory, this organization will allow more modular changes (like maybe adding Raspberry Pi 5 support?) in the future.
