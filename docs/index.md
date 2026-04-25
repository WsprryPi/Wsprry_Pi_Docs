# Wsprry Pi

Wsprry Pi is a Raspberry Pi-based transmitter for amateur radio operators who want to explore propagation with WSPR. The project focuses on making a low-cost, low-complexity beacon practical to install, configure, and operate on common Raspberry Pi hardware.

As of version 3.0.0, several CW capabilities were added to the suite:

- QRSS: The name “QRSS” is a derivation of the Q code “QRS”, a phrase Morse code operators send to indicate the transmitter needs to slow down. The extra “S” means slow way, way down.
- FSKCW: Frequency Shift Keying CW is a variant of QRSS that instead of activate/deactivate the carrier, the carrier is always activated as long as the transmission lasts. During pauses between dots, dashes or characters the frequency is shifted downwards.
- DFCW: Dual Frequency CW is a combination of QRSS and FSKCW. In DFCW, the element duration is replaced by the element frequency speeding transmissions considerably.

CW and the use of these additional protocols are beyond the scope of this documentation.  A good place to start is [Scott Harden's [AJ4VD] website](https://swharden.com/blog/tags/#qrss).

This documentation is organized to help you move through the project in a practical order:

- Learn what WSPR is and how Wsprry Pi works.
- Install the software and required supporting services.
- Configure and operate the system through the web UI or command line.
- Use the reference and FAQ material when you need detail or troubleshooting.

```{toctree}
:maxdepth: 2
:caption: Start Here

About_WSPR/index
About_Wsprry_Pi/index
Install/index
```

```{toctree}
:maxdepth: 2
:caption: Operate Wsprry Pi

User_Interface/index
Command_Line_Operations/index
Advanced_Operations/index
```

```{toctree}
:maxdepth: 2
:caption: Reference

Internals/index
Development/index
FAQ/index
Additional_Reading/index
```
