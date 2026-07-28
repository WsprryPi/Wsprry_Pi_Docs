# WSPR Settings

Use this section for WSPR station identity, reported power, frequency, transmission planning, and random offset. For the complete message-type and pairing workflow, see [Configure WSPR](../../User_Interface/Setup/Signal_Setup/wspr.md). Direct command-line users should also see [General and WSPR Options](../../Command_Line_Operations/wspr_options.md); frequency accuracy is covered in [Transmission Timing and Calibration](../timing_calibration.md).

(wspr-section)=
## WSPR

The `[WSPR]` section accepts standard, compound, and extended callsigns; Maidenhead locators; transmit power in dBm; a band name or frequency; one of the documented planner preferences; and optional random offset.

```{literalinclude} default_wsprrypi.ini
:language: ini
:start-at: [WSPR]
:end-before: [CW]
```
