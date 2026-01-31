---
orphan: true
---
(lowpass-filter-justification)=
# Low Pass Filter Requirements
Or, *Why a low-pass filter is required even if the carrier looks clean*

> NOTE: This document was split out of the main FAQ for readability.

Even when the *time‑domain* carrier (or a steady hold‑tone) looks clean, the dithering used to realize fractional frequency steps is effectively a **high‑rate two‑tone FSK inside each symbol**. That produces:

- **Discrete sidebands / spurs** at the block cadence and its harmonics (if cadence is periodic).
- A **noise‑like skirt** if cadence is randomized (spreading the energy).

An LPF (or band‑pass filtering appropriate to 12m) helps because most of the unwanted energy is **outside the intended narrow WSPR signal bandwidth**. In practice:

- A 12m LPF will strongly attenuate **higher‑order images** and **harmonics** from PWM and switching.
- It will also reduce **wideband hash** that extends beyond the WSPR occupied bandwidth.

Important nuance: an LPF will *not* remove *in‑band* phase noise or close‑in modulation products. However, the "noisy" look we typically see on a scope FFT for this kind of GPIO/PWM transmitter (especially with no filtering) is dominated by **out‑of‑band switching energy and images**, which a proper LPF will suppress substantially.

If you're transmitting on-air (even for testing), a real LPF is not optional - it's the difference between "usable narrowband signal" and "spraying energy across the band".

The debug output already provides the knobs and observables to explain what the FFT shows. Here's how they map.

(1-spur-spacing--comb-structure--block-cadence)=
## 1) Spur spacing / "comb" structure ↔ block cadence

From the debug line:

- iter/s~31156 is essentially the **block rate**, which is approximately:
  - block_rate ≈ f_pwm_clk / PWM_CLOCKS_PER_ITER_NOMINAL

With f_pwm_clk ≈ 500,000,992 Hz and typical PWM_CLOCKS_PER_ITER_NOMINAL ≈ 16,000, the frequency lands right around **31.25 kHz**, matching the reported iter/s~31156.

What does that mean on the FFT?:

- If the dithering cadence is regular, we tend to see **sidebands** spaced at about **±31 kHz**, **±62 kHz**, **±93 kHz**, etc. around the carrier (and around any images).
- If the application randomized the block length, the energy that would have formed discrete spurs becomes a **broader skirt** (energy spread into nearby bins).

(2-skirt-height--switching-activity--segment-statistics)=
## 2) Skirt "height" ↔ switching activity + segment statistics

These counters are the most directly useful:

- switches/s: how many **tone transitions per second** the application is creating.
- seg\[min,max\] and avgseg: how long each contiguous tone segment lasts.
- tiny(<20): how often the application produces **very short segments**.
- blocks\[tot,2tone,1tone\] and merged\[tail,tiny\]: how often it successfully avoided forced two‑segment blocks and eliminated pathological tails.

How that translates:

- More switches/s → more high‑rate modulation → **more broadband energy**.
- Smaller min_seg (especially values like 1-20) → **sharp edges / short impulses** → noticeably **higher wideband hash**, making the carrier "look noisy".
- Higher blocks\[1tone\] + higher merged\[...\] → fewer forced transitions → a visibly **cleaner skirt** at moderate offsets.

(3-count-actual-switching--expected-energy-distribution)=
## 3) "Count actual switching" ↔ expected energy distribution

The f0clk and f1clk counters (and frac\[f0,f1\]) tell us the *actual* duty split between the two tones. That helps us distinguish:

- A legitimate ratio outcome (average frequency correct), versus
- A pathological case where the ratio is right but achieved via many tiny switching events, which is where the **skirt gets ugly**.

If we see:

- frac\[f0,f1\] close to ratio, but
- switches/s very high, and/or min_seg very small,

…then we're in the regime where the average is correct, but the waveform has lots of edges, which shows up as skirts.

(a-practical-prove-it-on-the-hantek-procedure)=
## A practical "prove it on the Hantek" procedure

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
