# CW Mode Options

These options configure direct command-line transmissions using QRSS, FSKCW, or DFCW.

## Mode Selection

- `--mode <WSPR\|QRSS\|FSKCW\|DFCW>`  
  Select transmission mode.

- `--cw-message <text>`  
  Message to transmit in CW-based modes.

- `--cw-base-frequency <freq>`  
  Base RF frequency. Supports Hz, kHz, MHz, GHz suffixes.

- `--cw-shift-hz <hz>`  
  Frequency shift for FSK-based modes.

- `--cw-dot-seconds <seconds>`  
  Length of a Morse "dot".

## Timing

- `--cw-start-minute <0-59>`  
  Start minute for scheduled transmissions.

- `--cw-repeat-minutes <minutes>`  
  Interval between transmissions.

## Spacing

The `--cw-*` gap options are shared by QRSS and FSKCW. DFCW uses its own gap options.

- `--cw-intra-element-gap <multiple>`  
  QRSS/FSKCW gap between elements of a character.

- `--cw-inter-character-gap <multiple>`  
  QRSS/FSKCW gap between characters.

- `--cw-inter-word-gap <multiple>`  
  QRSS/FSKCW gap between words.

- `--dfcw-intra-element-gap <multiple>`

  DFCW gap between equal-duration dot and dash symbols (default: `0.333333` dot lengths).

- `--dfcw-inter-character-gap <multiple>`

  DFCW gap between characters (default: `1.0` dot lengths).

- `--dfcw-inter-word-gap <multiple>`

  DFCW gap between words (default: `3.0` dot lengths).

## Envelope Control

- `--cw-fade-shape <none\|linear\|raised_cosine>`  
  Shape of amplitude transitions.

- `--cw-fade-in-ms <ms>`  
  Fade-in duration.

- `--cw-fade-out-ms <ms>`  
  Fade-out duration.

- `--cw-fade-slice-ms <ms>`  
  Resolution of fade steps.
