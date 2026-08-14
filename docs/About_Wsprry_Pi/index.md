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

| GPIO clock profile | Processor or package | Raspberry Pi models | <span class="no-break">PLLD</span> |
| --- | --- | --- | --- |
| Legacy | [`BCM2835`, `BCM2836`, `BCM2837`, and `BCM2837B0`](https://www.raspberrypi.com/documentation/computers/processors.html#bcm2835); [`RP3A0`](https://www.raspberrypi.com/documentation/computers/processors.html#rp3a0) contains a `BCM2710A1` die from the `BCM2837` family | Raspberry Pi 1 A, A+, B, and B+; Raspberry Pi 2 B; Raspberry Pi 3 A+, B, and B+; Raspberry Pi Zero, Zero W, and Zero 2 W; Compute Module 1, 3, and 3+ | 500 MHz |
| BCM2711 | [`BCM2711`](https://www.raspberrypi.com/documentation/computers/processors.html#bcm2711) | Raspberry Pi 4 B; Raspberry Pi 400; Compute Module 4 and 4S | 750 MHz |

Some Raspberry Pi 2 and Raspberry Pi 3 model revisions use different processors within the legacy profile. They retain the same 500 MHz PLLD category for Wsprry Pi GPIO transmission.

### Band qualification

| Band | GPIO: 500 MHz PLLD | GPIO: 750 MHz PLLD | Si5351 |
| --- | --- | --- | --- |
| 2200 m | <span class="qualification-status qualification-status--partial">Partial</span><sup>1</sup> | <span class="qualification-status qualification-status--qualified">Qualified</span><sup>1</sup> | <span class="qualification-status qualification-status--unqualified">Unqualified</span><sup>2</sup> |
| 630 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span><sup>3</sup> |
| 160 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span><sup>4</sup> |
| 80 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 60 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 40 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 30 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 22 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 20 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 17 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 15 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 12 m | <span class="qualification-status qualification-status--unqualified">Unqualified</span><sup>5</sup> | <span class="qualification-status qualification-status--unqualified">Unqualified</span><sup>5</sup> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 10 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 6 m | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 4 m | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 2 m | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span><sup>7</sup> |
| 1.25 m | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--unqualified">Unqualified</span><sup>6</sup> |
| 70 cm | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--unqualified">Unqualified</span><sup>6</sup> |

1. On 2200 m, the legacy 500 MHz PLLD profile is qualified for TONE, QRSS, FSKCW, and DFCW. Its WSPR test produced a usable carrier but no correct decodes in three frames, so the profile is Partial rather than fully Qualified. The BCM2711 profile is qualified for all four CW-family modes and WSPR; it uses the 54 MHz oscillator because the 750 MHz PLLD cannot represent the required divider.
2. Si5351 operation on 2200 m remains unqualified. WsprryPi's retained calculation uses a final R divider of 8 and an internal frequency above 1 MHz, similar to the [QRP Labs low-frequency Si5351 example](https://qrp-labs.com/synth/si5351ademo.html), which generates 136 kHz from 1.088 MHz followed by R/8. However, the commercial [QRP Labs Ultimate3S](https://qrp-labs.com/ultimate3/u3s.html) is a complete transmitter rather than a bare clock-generator output. Its documented RF chain applies a defined Si5351 load, BS170 buffering and power amplification, impedance transformation in the output network, and a band-specific seven-element low-pass filter, as shown in the [Ultimate3S assembly manual](https://qrp-labs.com/images/ultimate3s/assembly_u3s.pdf). That product demonstrates that the synthesis approach can work as part of a designed RF chain; it does not qualify WsprryPi's direct CLK0 arrangement on 2200 m.
3. The Si5351 backend is qualified on 630 m using CLK0 with a final R divider of 4. The qualification used a 475,700 Hz request, a 1,902,800 Hz internal MultiSynth output, and three independently decoded WSPR frames. The result applies to the tested WsprryPi signal-generation path; an appropriate band-specific low-pass filter remains required.
4. The Si5351 backend is qualified on 160 m using CLK0 at minimum 2 mA drive with no final R division. Follow-up testing placed the 1,838,100 Hz carrier within +0.381 Hz of the request with 99.17% of resolved transmitter-added power in the best 20 Hz. Three independently captured WSPR frames decoded correctly. The result applies to the tested WsprryPi signal-generation path; an appropriate band-specific low-pass filter remains required.
5. On 12 m, one of eight complete frames decoded on a Raspberry Pi Zero 2 W in the 500 MHz PLLD profile. None of nine frames decoded on a Raspberry Pi 4 in the 750 MHz PLLD profile. Neither result met the requirement for three consecutive decodes. The difference correlates with the tested clock profiles, but it does not establish the processor itself as the cause. This note does not apply to the separate Si5351 result.
6. Wsprry Pi does not support Si5351 transmission on 1.25 m or 70 cm. The Si5351A is specified for output frequencies up to 200 MHz, below both the 222 MHz and 432 MHz WSPR frequencies. The commercially available [QRP Labs Ultimate3S](https://qrp-labs.com/ultimate3/u3s.html) operates its Si5351A beyond that specification on 222 MHz, but QRP Labs explicitly reports that WSPR does not work there. Its advertised band coverage also stops at 222 MHz rather than extending to 70 cm. These bands do not have mainstream direct-output support among commercial Si5351 WSPR transmitters, and experimental operation in another product does not establish Wsprry Pi compatibility.
7. The Si5351 2 m qualification applies to the tested 27 MHz ATX-11 TCXO reference configuration. [QRP Labs selected 27 MHz](https://qrp-labs.com/images/synth/synth_assembly6.pdf) because its synthesis calculations preserve WSPR tone spacing through 145 MHz; QRP Labs states that its 25 MHz configuration does not. Wsprry Pi's current per-tone PLL-retune planner can calculate all four 2 m tones from a 25 MHz reference, but no 25 MHz configuration has completed Wsprry Pi's carrier, tone-spacing, and three-frame decode qualification. Use a 27 MHz reference for qualified 2 m operation. A 25 MHz reference remains unqualified, not proven incompatible.

- <span class="qualification-status qualification-status--qualified">Qualified</span>: The transmitter type produced usable output on that band during qualification testing.
- <span class="qualification-status qualification-status--partial">Partial</span>: At least one supported mode is qualified on that band and at least one other mode is not. Check the numbered note before transmitting.
- <span class="qualification-status qualification-status--unqualified">Unqualified</span>: The transmitter type did not meet the carrier or decode gate on that band. Do not use an unqualified combination. Some unsupported requests are rejected before RF activation; a selectable setting does not override the qualification table.

See [GPIO Band Capabilities and Signal Quality](../FAQ/why_12m_looks_noisy.md) for the GPIO qualification findings.
