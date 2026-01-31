<!-- Grammar and spelling checked -->
# FAQ and Known Errors

- [FAQ and Known Errors](#faq-and-known-errors)
  - [Install Error ``bash: line 1: syntax error near unexpected token `<'``](#install-error-bash-line-1-syntax-error-near-unexpected-token-)
  - [or `curl: (22) The requested URL returned error: 404`](#or-curl-22-the-requested-url-returned-error-404)
  - [WSPR-15 Support](#wspr-15-support)
  - [Why 12m Looks "Noisy" on the Raspberry Pi - Summary](#why-12m-looks-noisy-on-the-raspberry-pi---summary)
    - [1. Observations](#1-observations)
    - [2. Why Test‑Tone Is Clean but WSPR Looks Noisy](#2-why-testtone-is-clean-but-wspr-looks-noisy)
      - [Test‑Tone Mode](#testtone-mode)
      - [WSPR Mode](#wspr-mode)
    - [3. Why 12m is Worse Than Other Bands](#3-why-12m-is-worse-than-other-bands)
    - [4. Why Raspberry Pi 4 Is Much Worse Than Pi 1/2/3](#4-why-raspberry-pi-4-is-much-worse-than-pi-123)
      - [GPIO Hardware](#gpio-hardware)
      - [Clocking Architecture](#clocking-architecture)
      - [PWM Clock Rate](#pwm-clock-rate)
    - [5. What Was Changed in the Software](#5-what-was-changed-in-the-software)
      - [Improvements Made](#improvements-made)
    - [6. Is This "Fixed" Without an LPF?](#6-is-this-fixed-without-an-lpf)
      - [Important Reality Check](#important-reality-check)
    - [7. Final Takeaway](#7-final-takeaway)
  - [Low‑pass filter justification (why an LPF matters even if the "carrier looks clean")](#lowpass-filter-justification-why-an-lpf-matters-even-if-the-carrier-looks-clean)
      - [1) Spur spacing / "comb" structure ↔ block cadence](#1-spur-spacing--comb-structure--block-cadence)
      - [2) Skirt "height" ↔ switching activity + segment statistics](#2-skirt-height--switching-activity--segment-statistics)
      - [3) "Count actual switching" ↔ expected energy distribution](#3-count-actual-switching--expected-energy-distribution)
      - [A practical "prove it on the Hantek" procedure](#a-practical-prove-it-on-the-hantek-procedure)


## Install Error ``bash: line 1: syntax error near unexpected token `<'``
## or `curl: (22) The requested URL returned error: 404`
If this happens, the DNS redirect (vanity URL) I use to make the install command shorter and easier to type may have broken.

**Explanation:** The installation command line uses an application called `curl` to download the target URL.  The pipe operator (`|`) redirects that to whatever follows, in this case, `sudo` (run as root) and `bash` (the command interpreter) to make the bash script run as soon as it downloads.  If the redirect breaks somehow, a regular HTML page will be sent instead of the bash script.  Bash doesn't know what to do with HTML (the `<` in the first position of the first line), so it simply refuses to do anything.

You may use the following longer and more challenging to type, command instead (one line):

```bash
curl -L https://raw.githubusercontent.com/WsprryPi/WsprryPi/main/scripts/install.sh | sudo bash
```

## WSPR-15 Support

I have removed WSR-15 support in version 2.x.

WSPR-15 (“Weak Signal Propagation Reporter” with a 15-minute transmit/receive cycle) was introduced in January 2013 as part of the experimental WSPR-X software suite.  By stretching the standard 2-minute cycle to 15 minutes, WSPR-15 lowers the symbol rate to about 0.183 Hz tone spacing (versus 1.4648 Hz in standard WSPR), narrowing the occupied bandwidth to ≈ 0.7 Hz.  This yields roughly a 9 dB sensitivity improvement, making it particularly attractive for very low-frequency (LF, MF) beacon work where Doppler shifts are minimal.

Sources:

- https://de.wikipedia.org/wiki/Weak_Signal_Propagation_Reporter
- https://www.scribd.com/document/358388839/WSPR-X-Users-Guide

Current Support and Viability

- Software support is scarce.  The only decoders that handle WSPR-15 are the legacy WSPRX program and the now-unmaintained WSPR-X client.  Mainstream WSJT-X releases (e.g., WSJT-X 2.7) implement only the standard 2-minute WSPR protocol and offer no WSPR-15 option
- Network integration is limited.  The central WSPRnet database and most reporting services expect the standard WSPR2 format; uploading or mapping WSPR-15 spots generally requires unofficial workarounds (for example, using wsprdaemon’s mode-designator code “2” for WSPR15) and sees only niche community use.  Source: https://wsprdaemon.org/wspr-field-names.html
- Modern alternatives outperform it.  Within WSJT-X, the FST4W family (e.g., FST4W-120) achieves similar or better sensitivity than standard WSPR—with FST4W-120 about 1.4 dB more sensitive—and is fully supported, actively developed, and widely adopted on LF/MF bands.  The WSJT-X author explicitly recommends migrating LF/MF propagation tests from JT9/WSPR to FST4/FST4W for sensitivity and ease of use.  Source: https://wsjt.sourceforge.io/FST4_Quick_Start.pdf

Bottom line: While WSPR-15 still “works” if you can run WSPRX or WSPR-X and manage manual uploads, it remains a niche, legacy protocol with minimal software and network support.  For new or ongoing weak-signal experiments—especially on LF/MF bands—you’ll find greater viability and community backing in the FST4W modes (or stick with the standard 2-minute WSPR2 on HF).

## Why 12m Looks "Noisy" on the Raspberry Pi - Summary

### 1\. Observations

- **Test tone at 24.926 MHz (12m)** looks _clean_ on the scope.
- **WSPR transmission on 12m** appears to be _noise_ or "hash".
- Other bands (10 m, 15 m, etc.) appear cleaner under similar conditions.
- The effect is much stronger on **Raspberry Pi 4** than on older Pis.
- No LPF or passive filtering is present; probing is directly on **GPIO 4**.

This behavior is **expected** given how the signal is generated and the differences in Pi 4 hardware.

### 2\. Why Test‑Tone Is Clean but WSPR Looks Noisy

#### Test‑Tone Mode

- Generates a **single, constant frequency**.
- No fractional scheduling.
- No rapid switching between tones.
- GPIO outputs a steady divider → narrow spectrum (aside from harmonics).

#### WSPR Mode

- Uses **four closely spaced tones**.
- Each symbol duration is generated by **fractional switching** between two adjacent divider values (f0 / f1) to hit the exact desired frequency.
- This results in _many rapid GPIO transitions_ within each symbol.

Without filtering, these transitions appear as:

- Broadband energy on a scope
- "Noise‑like" waveform instead of a clean sinusoid

### 3\. Why 12m is Worse Than Other Bands

12m sits in a **bad corner case**:

- High enough frequency that GPIO edges are extremely sharp in phase terms.
- Small divider differences → **fine‑grained fractional dithering**.
- Fractional scheduling creates very short segments:
  - A few PWM clocks of f0
  - Followed by a few PWM clocks of f1
- These tiny segments behave like **phase noise / wideband FM**.

Other bands:

- Larger divider gaps or different ratios.
- Fractional error spreads more benignly.
- Less visible broadband hash on a scope.

### 4\. Why Raspberry Pi 4 Is Much Worse Than Pi 1/2/3

#### GPIO Hardware

- Pi 4 GPIO edges are **much faster** (sub‑2 ns rise time).
- Faster edges → more high‑frequency content → more visible noise.

#### Clocking Architecture

- Pi 4 uses multiple high‑speed PLL domains:
  - PLLD_PER
  - PWM clock
  - Core / VPU clocks
- Fractional scheduling errors are no longer "blurred" by slow hardware.

#### PWM Clock Rate

- Pi 4 PWM clock ≈ **500 MHz** domain.
- Tiny timing errors become real RF events.
- Older Pis had slower clocks and unintentionally smoothed things out.

**Net effect:**  
Pi 4 exposes exactly what the math is doing.

### 5\. What Was Changed in the Software

The original scheduler:

- Used round() each iteration.
- Produced unpredictable tiny segments.
- Randomized iteration length.
- Generated high‑rate, irregular tone switching.

#### Improvements Made

- **Fixed‑Point Bresenham Scheduler**
  - Error‑accumulator style scheduling.
  - Exact long‑term frequency ratio.
  - Deterministic behavior.
- **Predictable Toggle Cadence**
  - Fixed block size (PWM_CLOCKS_PER_ITER_NOMINAL).
  - No random jitter.
- **Tail Clamp**
  - If the remaining clocks are small, send only **one tone**.
  - Prevents end‑of‑symbol micro‑toggles.
- **Tiny‑Segment Merge**
  - If n_f0 or n_f1 < threshold:
    - Merge the entire block into one tone.
  - Eliminates 2-10‑clock fragments.
- **Extensive Debug Instrumentation**
  - Counts actual switches.
  - Logs tiny / zero‑length segments.
  - Proves why 12m is noisy before.

These changes **significantly reduce broadband hash**, especially on Pi 4.

### 6\. Is This "Fixed" Without an LPF?

No - and that's expected.

#### Important Reality Check

- GPIO RF output is **not a DAC**.
- It is a fast square‑wave source.
- Software can reduce _unnecessary modulation artifacts_, but cannot remove harmonics.

A **low‑pass filter is mandatory** for:

- Legal operation
- Spectral cleanliness
- Making Pi 4 look as good as Pi 1/2/3 did "bare."

With a proper LPF:

- The 12m WSPR signal will look clean.
- The remaining differences between bands largely disappear.

### 7\. Final Takeaway

- 12m looks noisy because **fractional dithering + fast GPIO edges** were fully exposed on Pi 4.
- The issue is **not** a bad frequency, band bug, or calibration error.
- Software changes addressed _avoidable_ noise:
  - Tiny segments
  - Randomized timing
  - Unpredictable switching
- Pi 4 is simply more honest - and less forgiving - than older Pis.
- With the current scheduler **and** a proper LPF, the signal is correct.

**In short:**  
Nothing is "wrong" with 12m. The Pi 4 just stopped hiding the physics.

## Low‑pass filter justification (why an LPF matters even if the "carrier looks clean")

Even when the _time‑domain_ carrier (or a steady hold‑tone) looks clean, the dithering used to realize fractional frequency steps is effectively a **high‑rate two‑tone FSK inside each symbol**. That produces:

- **Discrete sidebands / spurs** at the block cadence and its harmonics (if cadence is periodic).
- A **noise‑like skirt** if cadence is randomized (spreading the energy).

An LPF (or band‑pass filtering appropriate to 12m) helps because most of the unwanted energy is **outside the intended narrow WSPR signal bandwidth**. In practice:

- A 12m LPF will strongly attenuate **higher‑order images** and **harmonics** from PWM and switching.
- It will also reduce **wideband hash** that extends beyond the WSPR occupied bandwidth.

Important nuance: an LPF will _not_ remove _in‑band_ phase noise or close‑in modulation products. However, the "noisy" look we typically see on a scope FFT for this kind of GPIO/PWM transmitter (especially with no filtering) is dominated by **out‑of‑band switching energy and images**, which a proper LPF will suppress substantially.

If you're transmitting on-air (even for testing), a real LPF is not optional - it's the difference between "usable narrowband signal" and "spraying energy across the band".

The debug output already provides the knobs and observables to explain what the FFT shows. Here's how they map.

#### 1) Spur spacing / "comb" structure ↔ block cadence

From the debug line:

- iter/s~31156 is essentially the **block rate**, which is approximately:
  - block_rate ≈ f_pwm_clk / PWM_CLOCKS_PER_ITER_NOMINAL

With f_pwm_clk ≈ 500,000,992 Hz and typical PWM_CLOCKS_PER_ITER_NOMINAL ≈ 16,000, the frequency lands right around **31.25 kHz**, matching the reported iter/s~31156.

What does that mean on the FFT?:

- If the dithering cadence is regular, we tend to see **sidebands** spaced at about **±31 kHz**, **±62 kHz**, **±93 kHz**, etc. around the carrier (and around any images).
- If the application randomized the block length, the energy that would have formed discrete spurs becomes a **broader skirt** (energy spread into nearby bins).

#### 2) Skirt "height" ↔ switching activity + segment statistics

These counters are the most directly useful:

- switches/s: how many **tone transitions per second** the application is creating.
- seg\[min,max\] and avgseg: how long each contiguous tone segment lasts.
- tiny(<20): how often the application produces **very short segments**.
- blocks\[tot,2tone,1tone\] and merged\[tail,tiny\]: how often it successfully avoided forced two‑segment blocks and eliminated pathological tails.

How that translates:

- More switches/s → more high‑rate modulation → **more broadband energy**.
- Smaller min_seg (especially values like 1-20) → **sharp edges / short impulses** → noticeably **higher wideband hash**, making the carrier "look noisy".
- Higher blocks\[1tone\] + higher merged\[...\] → fewer forced transitions → a visibly **cleaner skirt** at moderate offsets.

#### 3) "Count actual switching" ↔ expected energy distribution

The f0clk and f1clk counters (and frac\[f0,f1\]) tell us the _actual_ duty split between the two tones. That helps us distinguish:

- A legitimate ratio outcome (average frequency correct), versus
- A pathological case where the ratio is right but achieved via many tiny switching events, which is where the **skirt gets ugly**.

If we see:

- frac\[f0,f1\] close to ratio, but
- switches/s very high, and/or min_seg very small,

…then we're in the regime where the average is correct, but the waveform has lots of edges, which shows up as skirts.

#### A practical "prove it on the Hantek" procedure

- **Fix the scope configuration** (same FFT span, RBW, averaging, window) so changes are comparable.
- Run with WSPR_DEBUG_DITHER=1 and record a few debug lines for a steady symbol or a short run.
- On the FFT, measure:
  - Noise floor at fixed offsets (e.g., ±5 kHz, ±10 kHz, ±20 kHz, ±50 kHz, ±100 kHz),
  - Any visible spur spacing (look for ~31 kHz periodicity).
- Change exactly one parameter at a time:
  - PWM_CLOCKS_PER_ITER_NOMINAL (changes comb spacing),
  - tiny_thresh / tail‑merge behavior (changes tiny segments and skirts).
- Verify correlation:
  - If the PWM_CLOCKS_PER_ITER_NOMINAL increases, iter/s goes down, and the spur spacing should move inward (comb tighter).
  - If tail/segment clamping increases blocks\[1tone\] and reduces tiny, the near‑carrier skirt should drop.

This gives us a clean story: **what the scheduler is doing** (counters) produces **predictable modulation artifacts** (FFT), and the new tail‑merge logic specifically targets the worst‑case short segments that drive broadband "hash".
