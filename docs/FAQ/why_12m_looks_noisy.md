---
orphan: true
---
(why_12m_looks_noisy)=
# GPIO Band Capabilities and Signal Quality

Direct GPIO RF is not equally usable on every band. Conducted testing on a
Raspberry Pi 4 showed that the result is band-specific rather than a simple
upper-frequency limit.

:::{important}
Use the production `PWM_CLOCKS_PER_ITER_NOMINAL` value of 1000. Larger tested
values preserved a strong steady carrier on otherwise usable bands, but the
WSPR frames did not decode. A steady carrier alone does not prove that WSPR
modulation is usable.
:::

Current WsprryPi releases fail closed for direct GPIO requests in the 12 m,
6 m, and 2 m band ranges. The check uses the final requested RF frequency and
applies to named bands and arbitrary frequencies, WSPR and CW modes, scheduled
operation, command-line operation, and Test Tone. The request is rejected
before the transmitter is activated, with guidance to select Si5351 or a
GPIO-qualified band. The Si5351 backend is not subject to this GPIO policy.

## Tested GPIO Results

The following results apply to the tested Raspberry Pi 4 GPIO/GPCLK0 path.
They do not describe the separate Si5351 backend.

| Band | GPIO result with production pacing |
|---|---|
| 80 m | **Usable.** Prior steady-carrier and decoded-operation evidence. |
| 20 m | **Qualified.** All intended frames decoded; weak spectral replicas were also observed about 120 Hz from the intended signal. |
| 15 m | **Qualified.** All intended frames decoded. |
| 12 m | **Do not use.** No usable requested-frequency carrier; no frames decoded. |
| 10 m | **Qualified.** All intended frames decoded. |
| 6 m | **Do not use.** Transmitted power was dispersed across a broad spectral comb; no usable carrier. |
| 2 m | **Do not use.** No usable requested-frequency signal; also above the BCM2711 GPCLK approximate 125 MHz limit. |

The 15 m, 12 m, and 10 m sequence is important: 15 m works, 12 m fails, and
10 m works. The limitation is therefore not a monotonic frequency ceiling.
Divider selection and fractional scheduling interact differently at different
requested frequencies.

These are backend qualification results, not guaranteed RF specifications for
every Raspberry Pi or station. Oscillator accuracy, drift, phase noise,
harmonics, spurs, output power, and the attached RF chain remain
hardware-specific.

## Original-Generation Software Comparison

The `Legacy_1.2.3` software, which is close to the original WsprryPi
implementation, was also tested on the same Raspberry Pi 4 and Debian Trixie
platform. Its 12 m tone did not form a usable requested-frequency carrier, and
its 6 m tone formed a broad comb rather than a usable carrier. WSPR frame tests
were therefore not attempted. On this platform, reverting to the original
synthesis implementation does not recover either band; these results are not
evidence of a recent WsprryPi regression.

## Why 12 m and 6 m Fail

The GPIO backend synthesizes frequencies by switching between integer divider
states so their time average produces the requested WSPR tones. At some
frequencies, that switching produces an unfavorable distribution of energy.

- On 12 m, none of the tested pacing values produced a usable carrier at the
  requested frequency.
- On 6 m, the output was spread across a comb instead of being concentrated in
  one narrow channel. In the conducted measurement, the most useful 20 Hz
  region contained only about 1.7% of the resolved close-in transmitted power.
- On 2 m, no usable requested-frequency signal was found.

Visible comb teeth do not automatically mean the same failure on every band.
At 10 m, more than 99.5% of the resolved close-in power remained within one
20 Hz channel in the tested WSPR captures, and the frames decoded. The band
disposition is therefore based on usable modulation and decoding, not merely
on whether a spectrum display shows side products.

## Why Increasing the Pacing Value Does Not Help

The production pacing value is 1000 PWM clocks per iteration. Test builds at
4000 and 16000 retained strong unmodulated carriers on 20 m, 15 m, and 10 m,
but none of the attempted WSPR frames decoded at those larger values. The
divider states persisted too long for the receiver to recover the intended
WSPR tone average.

Increasing `PWM_CLOCKS_PER_ITER_NOMINAL` is therefore not a valid way to clean
up 12 m. It can make a steady tone appear convincing while making WSPR
modulation unusable.

## Filtering and Calibration

An appropriate band filter is required for any GPIO transmission. Filtering
suppresses harmonics and out-of-band switching products, but it cannot turn a
dispersed or absent requested-frequency carrier into a qualified WSPR signal.
See [Low-Pass Filter Requirements](lowpass-filter-justification.md).

Frequency calibration moves the output toward the intended frequency; it does
not cure band-specific synthesis artifacts. Calibration values are specific to
the Raspberry Pi and reference used to measure it. Do not copy another
station's PPM value as a project default.

Qualification does not authorize unlicensed or unfiltered on-air operation.
Use a shielded load and suitable attenuation for bench testing, and comply
with the rules that apply to your station.
