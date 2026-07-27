# Signal Setup Tab

The Signal Setup tab of the Signal Setup page is where configuration items related to th signal type or content are configured.

![Signal Setup Panel](signal_setup_wspr.png)

This tab has two main modes, WSPR and CW.

![WSPR or CW Mode](WSPR_CW.png)

Set your preferred mode and the page context will change specific to that mode.

## WSPR Mode

WSPR or Weak Signal Prorogation Reporting is the original mode for Wsprry Pi.

![WSPR Mode](WSPR_Mode.png)

### Station Identity

Within the Station identity section, you will set your callsign and locator. For normal Type 1 WSPR messages, the callsign is any valid 6-character or fewer. The Grid Locator is the four- character Maidenhead locator for where you are transmitting.

If you need or desire to use callsign extensions, have a callsign longer than 6 characters, or want or need to use a six-character locator, you will need to consider using Type 2 or 3 messages.

#### WSPR Transmission Type Selection Examples

| Callsign | Locator | Meaning | Allowed/Required Transmission |
| --- | --- | --- | --- |
| `AA0NT` | `EM18` | Standard callsign with 4-character locator | Type 1 single-frame |
| `AA0NT` | `EM18IG` | Standard callsign with 6-character locator | Type 1/3 paired transmission should be used if full 6-character locator reporting is required |
| `<AA0NT>` | `EM18` | Explicit Type 3 callsign with 4-character locator | Not useful; Type 3 is intended for extended locator or hashed callsign use |
| `<AA0NT>` | `EM18IG` | Explicit Type 3 callsign with 6-character locator | Type 1/3 paired transmission |
| `W0/AA0NT` | `EM18` | Compound/prefixed callsign with 4-character locator | Type 2 single-frame |
| `W0/AA0NT` | `EM18IG` | Compound/prefixed callsign with 6-character locator | Type 2/3 paired transmission |
| `<W0/AA0NT>` | `EM18IG` | Explicit Type 3 form of compound/prefixed callsign | Type 2/3 paired transmission |
| `AA0NT/P` | `EM18` | Compound/suffixed callsign with 4-character locator | Type 2 single-frame |
| `AA0NT/P` | `EM18IG` | Compound/suffixed callsign with 6-character locator | Type 2/3 paired transmission |
| `<AA0NT/P>` | `EM18IG` | Explicit Type 3 form of compound/suffixed callsign | Type 2/3 paired transmission |

##### Rule Summary

- A normal callsign with a 4-character locator uses **Type 1**.

    ```text
    AA0NT EM18
    ```

- A normal callsign with a 6-character locator requires a **Type 1/3 pair** to
  remain self-identifying.

    ```text
    AA0NT EM18
    <AA0NT> EM18IG
    ```

- A compound, portable, or prefixed callsign with a 4-character locator uses  **Type 2**.

    ```text
    W0/AA0NT EM18
    AA0NT/P EM18
    ```

- A compound, portable, or prefixed callsign with a 6-character locator requires a **Type 2/3 pair**.

    ```text
    W0/AA0NT EM18
    <W0/AA0NT> EM18IG
    ```

    ```text
    AA0NT/P EM18
    <AA0NT/P> EM18IG
    ```

- Angle brackets request an explicit **Type 3** callsign frame.

    ```text
    <AA0NT>
    ```

This should not make pairing invalid. Instead, when paired transmission is
required, the planner should choose the appropriate companion frame:

- Standard inner callsign: **Type 1/3 pair**
- Compound inner callsign: **Type 2/3 pair**

### WSPR Transmission Plan

These settings govern the way that WSPR is transmitted or received.

#### Frequencies

The Frequencies setting is a single frequency, or a list of frequencies, separated by spaces or commas.  The frequencies may be in band format:

- 10m
- 20m
- 30m
- etc.

They may also be listed in engineering notation where these are all the same:

- 50MHz
- 0.05GHz
- 50000kHz
- 50000000Hz

Notice that there are no spaces between the number and `m` for meters, and none between the number and the engineering notation.

Finally, the frequency may be listed in pure Hz without a notation such as 21096.100.

Of note, WSPR is an Upper Side Band (USB) mode.  The frequency entered is a typical USB dial frequency.  You may note that the tones are shifted ~1,500Hz higher.

Using the bands will select the canonical WSPR frequency.

#### Random offset

Turning this switch on will add a positive or negative random offset to the transmitted frequency.  This can be handy when there is a lot of traffic on WSPR, and allow you to find a more clear slice of the available bandwidth.

#### Reported Power

Reported power is not the same as the actual transmission power.  The transmitters settings may be attenuated by the LPF and additional gain may be added. Possible values are:

`0, 3, 7, 10, 13, 17, 20, 23, 27, 30, 33, 37, 40, 43, 47, 50, 53, 57, 60`

dBm is added to the encoder WSPR message to be a reference for the decoded message.  The operator should choose the value that is closest to their actual transmission power.

This setting hs no bearing on actual transmission power.

#### Frequency calibration (PPM) & NTP Calibration

Some operators may choose to manually calibrate their rig.  This is more important with GPIO-based transmissions where the Raspberry Pi frequencies may be impacted by power, heat, and mechanical differences.

Others may opt for the simpler and "accurate enough" NTP calibration.  This uses an internet time source to calibrate the output frequency.  For most bands, this is more than reasonable.  Some operators on higher bands such as 6m and 2m may find even a small deviation puts them out of the transmission boundaries, and may need to use a calculated PPM adjustment.

When NTP is enabled, the Frequency Calibration field is dithered.  When using the Si5351 clock module, NTP is disabled and manual calibration should be used - although the combination of a TCXO and the Si5351 is often so close, it may be ignored.

In all cases, NTP will continue to keep the Pi in sync to time messages appropriately.

#### Planning Mode

Planning mode relates to the use of Type 1, 2, and 3 messages, and the behavior when certain data elements are entered.

- **Automatic** - The planner attempts to choose the best transmission plan based on the data entered.
- **Prefer paired when available** - If the planner finds it can generate both Type 2 and 3 messages, it ill do so in alternating windows.
- **Require paired** - Requires the planner to always use a paired Type 2 and 3 message format.  For those who want the additional data to be received and understood by even the most remote stations under challenging conditions, this is likely the best choice.

## CW Mode

CW Mode, using one of QRSS, FSKCW, or DFCW, was added as of version 3 of Wsprry Pi.  It offers some new exciting methods of QRP transmissions.

![CW Mode](CW_Mode.png)

CW modes are not as strictly formatted, and are **not** a beacon mode as WSPR is.  Radio beacons send continuous, automated, unattended, one-way transmissions without specific reception targets. In contrast, QRSS transmitters are only intended to be transmitting when the control operator is available to control them, and the recipients are known QRSS grabbers around the world.

### Mode

The Mode panel allows configuring most of the metadata for CW modes.

#### Available Modes

The actual CW mode is one of:

- **QRSS** - QRSS is extreme slow speed CW, the name is derived from the Q-code QRS (reduce your speed).  This mode, when displayed on a grabber's screen, is the most "CW-looking" of all the modes, with familiar dots and dashes.
- **FSKCW** - FSKCW means Frequency Shift Keying CW.  Instead of activate/deactivate the carrier, the carrier is always activated as long as the transmission lasts. During pauses between dots, dashes or characters the frequency is shifted downwards.  The upper trace shown on the screen contains the morse information, the lower trace is drawn during signal pauses.
- **DFCW** - DFCW means Dual Frequency CW.  DFCW mode was developed that enhances the average speed in LF transmissions (more impacted by QRN) by a factor of 2.5 to 3. In DFCW the element *duration* is replaced by the element *frequency*. Dots and dashes do not have a different length but they are transmitted on a different frequency. Due to this frequency shift there is no space needed between the dots/dashes and the character space can be reduced to the same dot length. A short space (typically 1/3 of a dot length) is added between the dots and dashes for ease of copy.

#### Dot seconds

Dot seconds are the basis for timing the character elements.  If a dot is 3 seconds, a dash is 3*dot or 9 seconds.

#### Frequency offset

This is the positive offset from the base that FSKCW or DFCW will shift to transmit characters.  This is in Hz and should be entered without any engineering notation.  This field is dithered and unavailable in QRSS mode.

#### Base frequency

This is the base frequency for transmissions.  For QRSS it is the exact frequency of the characters.  For FSKCW or DFCW it is the base from which the shift is made to transmit.  This is entered as a whole-number in Hz such as `14096900`, or include `Hz`, `kHz`, `MHz`, or `GHz` for decimal values such as `14.0969MHz`.

#### Frequency calibration

This is the CW form of the PPM/NTP settings in WSPR.  Here you may calibrate your frequency (the actual tone frequency, as opposed to the SSB offset for WSPR) in PPM.  Your available range is +-200PPM.

#### Start minute / Repeat interval

QRSS operators generally start at minute 0 and repeat every 10 minutes. Start at 0 and Repeat at 10 will enable this cadence. The repeat interval must also be long enough for the complete CW message. A transmission may take exactly the full repeat interval, but it may not run longer than that interval.

#### Intra-Element Gap

This adds a small gap in between elements of a character.  In other words, an "S" without gaps may be indistinguishable from a "T".  This is a positive multiplier applied to the dot seconds.

#### Inter-Character Gap

This adds gaps between characters, as a multiplier applied to the dot timing.  Typically this is 3*dot length.

#### Inter-Word Gap

This adds gaps between words, as a multiplier applied to the dot timing.  Typically this is 7*dot length.

### CW Message

Enter the text to transmit in the Message field. Setup updates the **Estimated Message Length** when you edit the message or change:

- the selected QRSS, FSKCW, or DFCW mode;
- the dot length or speed;
- the spacing values used by the selected mode.

Changing the repeat interval reevaluates whether that estimated duration fits within the transmission window.

Only the active spacing controls affect the estimate. QRSS and FSKCW use their shared spacing values, while DFCW uses the DFCW spacing values.

(cw-message-too-long)=
#### When a CW message is too long

If the estimated message length exceeds the repeat interval, Setup keeps the draft in the Message field but does not save it. The Message field is marked invalid, and the Setup header displays a persistent **Save failed** status. The detail reports the calculated message duration and configured repeat interval, then identifies the available corrections.

Autosave remains paused while the message is too long. Further edits that remain over the limit update the estimate and keep the inline failure visible; they do not repeatedly open the general configuration reload-failure dialog.

To correct the configuration, use one or more of these options:

- Shorten the message.
- Reduce the dot length or select a faster speed.
- Reduce the spacing values used by the selected mode.
- Increase the repeat interval.

Setup clears the duration error and resumes autosave automatically as soon as the estimated message length is less than or equal to the repeat interval. A duration equal to the repeat interval is valid.

An empty message or a message containing an unsupported character is a separate validation error. Correct the message shown in the field; clearing a duration error does not make an empty or unsupported message valid.
