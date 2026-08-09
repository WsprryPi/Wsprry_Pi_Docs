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

Qualification is specific to the transmitter type and band.

| Band | GPIO | Si5351 |
| --- | --- | --- |
| 2200 m | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--unqualified">Unqualified</span> |
| 630 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--unqualified">Unqualified</span> |
| 160 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--unqualified">Unqualified</span> |
| 80 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 60 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 40 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 30 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 22 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 20 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 17 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 15 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 12 m | <span class="qualification-status qualification-status--unqualified">Unqualified</span>\* | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 10 m | <span class="qualification-status qualification-status--qualified">Qualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 6 m | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 4 m | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 2 m | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--qualified">Qualified</span> |
| 1.25 m | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--unqualified">Unqualified</span> |
| 70 cm | <span class="qualification-status qualification-status--unqualified">Unqualified</span> | <span class="qualification-status qualification-status--unqualified">Unqualified</span> |

\* The 12 m GPIO result is based on testing with two Raspberry Pi processors. On a Raspberry Pi Zero 2 W with a `BCM2837`-compatible processor and 32-bit OS, one of five complete captured frames decoded. The other four did not, so the result did not meet the requirement for three consecutive decodes. On the Raspberry Pi 4 with a `BCM2711` processor, none of nine frames decoded across the three tested pacing settings, including 0 of 3 at the production setting. This note does not apply to the separate Si5351 status.

The 2200 m, 630 m, 160 m, 12 m Si5351, and 1.25 m results were completed in [Issue 390](https://github.com/WsprryPi/WsprryPi/issues/390) using conducted, attenuated testing. GPIO 630 m and 160 m and Si5351 12 m each produced three consecutive correct WSPR decodes. GPIO 2200 m and Si5351 630 m and 160 m did not produce usable requested-frequency carriers. The Si5351 planner rejected 2200 m and 1.25 m before RF activation. These results apply to the tested Raspberry Pi 4 GPIO and Raspberry Pi 5 Si5351/27 MHz TCXO paths; they are not universal RF specifications for every station.

- <span class="qualification-status qualification-status--qualified">Qualified</span>: The transmitter type produced usable output on that band during qualification testing.
- <span class="qualification-status qualification-status--unqualified">Unqualified</span>: The transmitter type did not meet the carrier or decode gate on that band. Do not use an unqualified combination. Some unsupported requests are rejected before RF activation; a selectable setting does not override the qualification table.
- <span class="qualification-status qualification-status--untested">Untested</span>: No qualification result is available for that band and transmitter type.

See [GPIO Band Capabilities and Signal Quality](../FAQ/why_12m_looks_noisy.md) for the GPIO qualification findings.
