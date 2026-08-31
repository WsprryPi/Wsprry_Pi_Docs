# About Wsprry Pi

WsprryPi creates a simple WSPR beacon on your Raspberry Pi by generating a Pulse-Width Modulation (PWM) square-wave signal through a General-Purpose Input/Output (GPIO) pin. As of version 3.0.0, support for the inexpensive Si5351 clock generator was added, allowing use of the more capable Raspberry Pi 5.

You connect the generated output through a [Low-Pass Filter to remove harmonics](https://www.nutsvolts.com/magazine/article/making\_waves\_) and then to an appropriate antenna.

:::{warning}
Do not use Wsprry Pi without an appropriate low-pass filter. Unfiltered output can create harmonic interference on other bands.
:::

## Attribution

This idea likely originated with Oliver Mattos and Oskar Weigl at the PiFM project. While the website is no longer online, the Wayback Machine has [the last known good version]( http://web.archive.org/web/20131016184311/http://www.icrobotics.co.uk/wiki/index.php/Turning_the_Raspberry_Pi_Into_an_FM_Transmitter).

The icrobotics.co.uk website still hosts the original PiFM code. However, I suspect the domain has fallen into disrepair and may be unsafe, and I will not provide direct links here. Use the URL above to see the site; should the code disappear, I have [saved it here](https://github.com/WsprryPi/WsprryPi/raw/refs/heads/main/historical/pifm.tar.gz).

After a conversation with Bruce Raymond of TAPR, I forked @threeme3's repo and added rudimentary installation capabilities and orchestration. Version 1.x of this project was a fork of threeme3/WsprryPi (no longer on GitHub), licensed under the GNU General Public License v3 (GPLv3). The original project is no longer maintained.

In late 2024, George [K9TRV] of TAPR contacted me with questions about using WsprryPi on the Pi 5. The conversation led me to discard the original code in favor of a more modern, extensible, and maintainable base.

As of Version 2.0+, all of the original code has been replaced with my own; it is no longer derivative work, and I have released it under the MIT license.

My goal, and where you will validate my success, is to let you execute one command on your Pi to install and run the Wsprry Pi software. If you are lucky and have been living right, a radio wave will hit the cosmos and be received [somewhere else](https://wsprnet.org).

## Raspberry Pi model compatibility

Compatibility depends on both the Raspberry Pi model and transmitter type.

| Model | GPIO | Si5351 |
| --- | --- | --- |
| Raspberry Pi 1 Model B | <span class="compatibility-status compatibility-status--tested">Tested</span> | <span class="compatibility-status compatibility-status--tested">Tested</span> |
| Raspberry Pi 1 Model A | <span class="compatibility-status compatibility-status--tested">Tested</span> | <span class="compatibility-status compatibility-status--tested">Tested</span> |
| Raspberry Pi 1 Model B+ | <span class="compatibility-status compatibility-status--tested">Tested</span> | <span class="compatibility-status compatibility-status--tested">Tested</span> |
| Raspberry Pi 1 Model A+ | <span class="compatibility-status compatibility-status--tested">Tested</span> | <span class="compatibility-status compatibility-status--tested">Tested</span> |
| Raspberry Pi 2 Model B | <span class="compatibility-status compatibility-status--tested">Tested</span> | <span class="compatibility-status compatibility-status--tested">Tested</span> |
| Raspberry Pi 3 Model B | <span class="compatibility-status compatibility-status--tested">Tested</span> | <span class="compatibility-status compatibility-status--tested">Tested</span> |
| Raspberry Pi 3 Model B+ | <span class="compatibility-status compatibility-status--tested">Tested</span> | <span class="compatibility-status compatibility-status--tested">Tested</span> |
| Raspberry Pi 3 Model A+ | <span class="compatibility-status compatibility-status--tested">Tested</span> | <span class="compatibility-status compatibility-status--tested">Tested</span> |
| Raspberry Pi 4 Model B | <span class="compatibility-status compatibility-status--tested">Tested</span> | <span class="compatibility-status compatibility-status--tested">Tested</span> |
| Raspberry Pi 5 | <span class="compatibility-status compatibility-status--unsupported">Not supported</span> | <span class="compatibility-status compatibility-status--tested">Tested</span> |
| Raspberry Pi Zero | <span class="compatibility-status compatibility-status--tested">Tested</span> | <span class="compatibility-status compatibility-status--tested">Tested</span> |
| Raspberry Pi Zero W | <span class="compatibility-status compatibility-status--tested">Tested</span> | <span class="compatibility-status compatibility-status--tested">Tested</span> |
| Raspberry Pi Zero 2 W | <span class="compatibility-status compatibility-status--tested">Tested</span> | <span class="compatibility-status compatibility-status--tested">Tested</span> |
| Raspberry Pi 400 | <span class="compatibility-status compatibility-status--untested">Untested</span> | <span class="compatibility-status compatibility-status--untested">Untested</span> |
| Raspberry Pi 500 | <span class="compatibility-status compatibility-status--unsupported">Not supported</span> | <span class="compatibility-status compatibility-status--untested">Untested</span> |
| Raspberry Pi 500+ | <span class="compatibility-status compatibility-status--unsupported">Not supported</span> | <span class="compatibility-status compatibility-status--untested">Untested</span> |

- <span class="compatibility-status compatibility-status--tested">Tested</span>: WsprryPi operation has been recorded on this model and transmitter type.
- <span class="compatibility-status compatibility-status--untested">Untested</span>: The hardware is expected to support this transmitter type, but model-specific operation has not been recorded.
- <span class="compatibility-status compatibility-status--unsupported">Not supported</span>: WsprryPi cannot use this transmitter type on the model.

Raspberry Pi 5-family systems use the Si5351 transmitter only.

## Compute Module compatibility

Compute Modules retain the GPIO and I2C capabilities of their corresponding Raspberry Pi generation, but they do not include GPIO headers. Their carrier board must route the connections required by the selected transmitter. Although these configurations are untested, they are expected to work as indicated in the table; generation-specific restrictions, including the Compute Module 5 GPIO limitation, still apply.

| Model | GPIO | Si5351 |
| --- | --- | --- |
| Raspberry Pi Compute Module 1 | <span class="compatibility-status compatibility-status--untested">Untested</span> | <span class="compatibility-status compatibility-status--untested">Untested</span> |
| Raspberry Pi Compute Module 3 | <span class="compatibility-status compatibility-status--untested">Untested</span> | <span class="compatibility-status compatibility-status--untested">Untested</span> |
| Raspberry Pi Compute Module 3+ | <span class="compatibility-status compatibility-status--untested">Untested</span> | <span class="compatibility-status compatibility-status--untested">Untested</span> |
| Raspberry Pi Compute Module 4 | <span class="compatibility-status compatibility-status--untested">Untested</span> | <span class="compatibility-status compatibility-status--untested">Untested</span> |
| Raspberry Pi Compute Module 4S | <span class="compatibility-status compatibility-status--untested">Untested</span> | <span class="compatibility-status compatibility-status--untested">Untested</span> |
| Raspberry Pi Compute Module 5 | <span class="compatibility-status compatibility-status--unsupported">Not supported</span> | <span class="compatibility-status compatibility-status--untested">Untested</span> |
| Raspberry Pi Compute Module Zero | <span class="compatibility-status compatibility-status--untested">Untested</span> | <span class="compatibility-status compatibility-status--untested">Untested</span> |

## Raspberry Pi Pico incompatibility

Raspberry Pi Pico boards are microcontrollers and do not run Linux, so they are incompatible with WsprryPi. WsprryPi cannot use either the GPIO or Si5351 transmitter backend on these boards.

| Model | GPIO | Si5351 |
| --- | --- | --- |
| Raspberry Pi Pico | <span class="compatibility-status compatibility-status--unsupported">Not supported</span> | <span class="compatibility-status compatibility-status--unsupported">Not supported</span> |
| Raspberry Pi Pico W | <span class="compatibility-status compatibility-status--unsupported">Not supported</span> | <span class="compatibility-status compatibility-status--unsupported">Not supported</span> |
| Raspberry Pi Pico 2 | <span class="compatibility-status compatibility-status--unsupported">Not supported</span> | <span class="compatibility-status compatibility-status--unsupported">Not supported</span> |
| Raspberry Pi Pico 2 W | <span class="compatibility-status compatibility-status--unsupported">Not supported</span> | <span class="compatibility-status compatibility-status--unsupported">Not supported</span> |

## Transmitter qualification

Qualification is specific to the transmitter type, band, and GPIO clock profile.

### GPIO clock profiles

Wsprry Pi supports two GPIO clock profiles. The processor identifies which profile a Raspberry Pi uses, but the relevant transmitter difference is the PLLD frequency and the resulting divider range.

In the table, **SoC** means system on chip and **CM** means Compute Module.

| GPIO profile | SoC or package | Pi models | <span class="no-break">PLLD</span> |
| --- | --- | --- | --- |
| Legacy | [`BCM2835`, `BCM2836`, `BCM2837`, and `BCM2837B0`](https://www.raspberrypi.com/documentation/computers/processors.html#bcm2835); [`RP3A0`](https://www.raspberrypi.com/documentation/computers/processors.html#rp3a0) contains a `BCM2710A1` die from the `BCM2837` family | Pi 1 A/A+/B/B+; Pi 2 B; Pi 3 A+/B/B+; Pi Zero/Zero W/Zero 2 W; CM1/CM3/CM3+ | 500 MHz |
| BCM2711 | [`BCM2711`](https://www.raspberrypi.com/documentation/computers/processors.html#bcm2711) | Pi 4 B; Pi 400; CM4/CM4S | 750 MHz |

Some Raspberry Pi 2 and Raspberry Pi 3 model revisions use different processors within the legacy profile. They retain the same 500 MHz PLLD category for Wsprry Pi GPIO transmission.

### Band qualification

| Band | GPIO: Pi 1–3<br>500 MHz PLLD | GPIO: Pi 4<br>750 MHz PLLD | GPIO: Pi 5<br>200 MHz PLL_SYS | Si5351 |
| --- | --- | --- | --- | --- |
| 2200 m | <span class="qualification-status qualification-status--partial">Partial</span><sup>1</sup> | <span class="qualification-status qualification-status--qualified">Qualified</span><sup>1</sup> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 630 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--untested">Untested</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 160 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 80 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 60 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 40 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 30 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 22 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 20 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 17 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 15 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--untested">Untested</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 12 m | <span class="qualification-status qualification-status--unqualified">Unqualified</span><sup>2</sup> | <span class="qualification-status qualification-status--unqualified">Unqualified</span><sup>2</sup> | <span class="qualification-status qualification-status--untested">Untested</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 10 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--untested">Untested</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 6 m | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--partial">Partial</span><sup>4</sup> | <span class="qualification-status qualification-status--untested">Untested</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 4 m | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--untested">Untested</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 2 m | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--untested">Untested</span> | <span class="qualification-status qualification-status--qualified">Qualified</span><sup>3</sup> |
| 1.25 m | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--unavailable">Unavailable</span><sup>5</sup> | <span class="qualification-status qualification-status--untested">Untested</span> | <span class="qualification-status qualification-status--unavailable">Unavailable</span><sup>5</sup> |
| 70 cm | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--unavailable">Unavailable</span><sup>5</sup> | <span class="qualification-status qualification-status--untested">Untested</span> | <span class="qualification-status qualification-status--unavailable">Unavailable</span><sup>5</sup> |

1. On 2200 m, the 500 MHz PLLD profile is qualified for TONE, QRSS, FSKCW, and DFCW; WSPR did not meet the decode requirement. The 750 MHz PLLD profile is qualified for TONE, QRSS, FSKCW, DFCW, and WSPR.
2. GPIO transmission on 12 m did not meet the WSPR decode requirement with either clock profile. This does not affect the separate Si5351 qualification.
3. Si5351 qualification on 2 m requires the tested 27 MHz reference configuration. A 25 MHz reference did not pass 2 m qualification testing and is unqualified.
4. On 6 m, the 750 MHz PLLD profile is qualified for TONE, QRSS, FSKCW, and DFCW. WSPR did not meet the decode requirement.
5. The 750 MHz PLLD GPIO planner cannot construct 1.25 m or 70 cm output. Si5351 direct output is also unavailable on these bands. Experimental overrides cannot enable unavailable combinations.

- <span class="qualification-status qualification-status--qualified">Qualified</span>: The transmitter type produced usable output on that band during qualification testing.
- <span class="qualification-status qualification-status--partial">Partial</span>: At least one supported mode is qualified on that band and at least one other mode is not. Check the numbered note before transmitting.
- <span class="qualification-status qualification-status--untested">Untested</span>: The backend can construct the requested output, but qualification evidence has not been recorded. Wsprry Pi blocks the combination by default; controlled testing requires the explicit experimental override.
- <span class="qualification-status qualification-status--unqualified">Unqualified</span>: The backend and mode combination did not meet the applicable carrier or decode gate. Wsprry Pi blocks the combination by default. An operator with appropriate authorization may enable it with the explicit experimental override and remains responsible for RF-path safety, filtering, and compliance with applicable rules.
- <span class="qualification-status qualification-status--unavailable">Unavailable</span>: The backend cannot safely construct this output. Experimental overrides do not enable it.

For local qualification testing, use a conducted, suitably attenuated and filtered path into a receiver or SDR. Begin and end with a known-qualified control, verify the requested carrier and mode behavior, and confirm that RF output is disabled afterward. Use [`--allow-unqualified-frequency`](../Command_Line_Operations/transmitter_backends.md) only for a controlled test of an Untested or Unqualified combination; it cannot enable an Unavailable combination.

See [GPIO Band Capabilities and Signal Quality](../FAQ/why_12m_looks_noisy.md) for the GPIO qualification findings.
