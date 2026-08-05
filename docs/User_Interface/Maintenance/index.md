# Maintenance Card

The maintenance page allows you to perform tasks that are not necessarily related to the business of transmitting WSPR or QRSS modes, but that you may need from time to time.

![Maintenance Page](maintenance.png)

## Repair Configuration

In rare cases, you may find that your configuration is present and readable but has missing sections or is otherwise not fully functional. If you hand-edit your INI, for example, and mistakenly delete sections or keys.

![Repair Configuration](repair.png)

When you press the "Repair current configuration" button, you will not be prompted before execution because it is considered a safe operation. A stock configuration file will be created, and your current configuration values will be applied on top. Missing or invalid data will be restored from the stock configuration.

![Configuration Repaired](repaired.png)

After this action, you should review all your settings to ensure they are still correct.

## Reset to Stock

This process is helpful if your INI file is damaged on disk or completely missing.

![Reset Configuration](reset.png)

Unlike the Repair Configuration button, it does not preserve existing user values. It copies a new stock `wsprrypi.ini` file in place of your current one if it exists, and reloads the configuration shipped with the application.

When you press the "Reset to defaults" button, you will be presented with a confirmation modal because this will destroy your existing configuration.

![Reset Confirmation](confirmation.png)

Confirm the action, and the process will complete and return the status.

![Reset Complete](reset_complete.png)

You will need to reconfigure all of your preferences before continuing to transmit.

## Test Tone

A test tone is useful for checking the transmit path, calibration, and tuning.
Connect the transmitter to a suitable dummy load or attenuated test path before
starting. Keep the test brief, and select **End** as soon as the check is
complete.

![Test Tone](test_tone.png)

Select **Test tone** to open the manual tone controls. This does not change the
frequency saved in Setup.

### Choose the frequency source

Choose one of these frequency sources:

- **WSPR band** uses a canonical band entry supplied by the connected
  controller. The preview shows the WSPR dial frequency and the resulting RF
  frequency after the WSPR offset is applied.
- **Custom RF frequency** accepts an exact, whole-number frequency in Hz. This
  value is the RF frequency; no WSPR offset is added.

![Test Tone frequency-source controls with Custom RF frequency selected](test_tone_frequency_source.jpg)

The example above shows the safe disconnected state: the frequency source and
exact RF preview remain visible, while **Start** and **End** are unavailable.

The WSPR band list is controller-authorized rather than a fixed list in the
browser. **Start** remains unavailable until the controller is connected, its
catalog is available, a valid frequency source is selected, and normal
transmission interlocks permit a test tone. A disabled button is visually
muted and cannot be selected.

If scheduled WSPR or CW-family transmission is enabled, the page prompts you
to stop and disable it before starting a test tone.

![Disable Transmissions](disable_transmissions.png)

You must re-enable normal transmissions on the Operations page after testing.

### Read the result

Before **Start**, the frequency summary is a preview of the request. After the
controller replies, the execution status reports what the controller actually
committed. When the committed frequency matches the preview, the status does
not repeat the full dial-frequency, offset, and RF-frequency calculation.

The execution status calls out information that changes what you should do,
including:

- a committed frequency that differs from the request;
- controller selector details or warnings;
- a rejected or failed start; and
- whether **End** remains available for recovery.

After the controller confirms a successful stop, the status reads **Test Tone
ended.** **Start** becomes available again when the connection, catalog,
selection, and interlocks still permit it.

### Recover from an uncertain result

If a Start or End request times out, or the connection drops before the result
is confirmed, the browser cannot safely claim whether RF is active. Follow the
status guidance and reconnect if necessary. **End** remains available whenever
the tone may still be active, including after reconnect or when the WSPR catalog
is unavailable. Use **End** to request a confirmed stop before attempting
another Start.

Send one Test Tone action at a time and wait for its result before selecting
another action. Start and End requests are not transactionally serialized.


## Update Checker

The Wsprry Pi UI will automatically check the running version against releases on GitHub.  When a new version is available, you will see a pop-up directing you to the [Releases page](https://github.com/WsprryPi/WsprryPi/releases/).

![Update Available Modal](update_avail.png)

You may also check manually on the Maintenance page, and force an immediate check.

![Force Update Check](manual_update_check.png)

You may dismiss the modal, and the footer will continue to quietly remind you that an update is available.

![Update Available Footer](update_footer.png)

You may also choose to "Never check again" either in the modal, or by selecting "About" in the footer.

![About - Never Check](about_update.png)

If you choose to never check again and wish to re-enable the checking, the opposite setting is available in the "About" footer, as well as in the update check section in the maintenance panel.

Technical information on the update check process is available in the [WsprryPi Automatic Update Polling](update_check.md) technical page.

## Support Bundle

Use **Support Bundle** when a developer asks for diagnostic information about your Wsprry Pi installation. The Maintenance workflow creates the archive locally, lets you opt in to an active I²C bus scan when needed, downloads the completed `.tar.gz` through your browser, and removes the retained Pi-side copy after successful receipt.

Review the archive before sharing it. See [Create and Share a Support Bundle](support_bundle.md) for the complete collection inventory, privacy guidance, download and cleanup behavior, and instructions for attaching the bundle to a GitHub issue.

```{toctree}
:maxdepth: 1
:hidden:

Create and Share a Support Bundle <support_bundle>
```
