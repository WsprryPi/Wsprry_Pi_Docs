# Configuration Troubleshooting

## Troubleshooting CW Configuration Saves

When a QRSS, FSKCW, or DFCW message would take longer than its configured repeat interval, Setup marks the Message field invalid and displays **Save failed** with the calculated duration and repeat interval. The invalid draft remains in the browser so it can be corrected, but it is not applied to the running configuration. Autosave resumes automatically when the adjusted duration is less than or equal to the repeat interval.

This inline state identifies a timing problem that can be corrected on the Setup page. Other configuration reload failures that cannot be tied safely to an editable field may still appear in the general reload-failure dialog and may require checking the application log or configuration file.

See {ref}`cw-message-too-long` for the duration inputs and correction steps.

## GPIO RF Output Conflicts

When the GPIO transmitter backend is selected, its configured GPIO4 or GPIO20 RF output cannot also be assigned to an enabled Band GPIO, Transmit LED, Shutdown Button, or Amp Control. Setup marks both conflicting controls with `GPION is reserved by GPIO RF Output.` and keeps the invalid draft visible without saving it.

Resolve the conflict by changing either pin, disabling the ordinary GPIO role, or selecting the Si5351 backend. The reservation depends on the selected backend, not the **Transmit** switch, so turning transmission off does not release the GPIO RF output pin. Disabled ordinary roles may retain their pin values.

(startup-transmission-is-inhibited)=
## Startup Transmission Is Inhibited

At every daemon start, WsprryPi attempts to disable the selected transmitter backend before it starts services or schedules any transmission. If the safe state cannot be confirmed, the daemon continues running for diagnosis but blocks all transmission paths. This startup inhibition is separate from the saved **Transmit** switch and **Enable on Boot** policy.

Review the WsprryPi log for the startup-quiescence error, then check the hardware selected on the **Setup > Transmitter** page:

- For **Si5351**, verify the configured I2C bus and address, device wiring and power, and that the device is visible to the operating system.
- For **GPIO**, verify that the Raspberry Pi model supports direct GPIO-clock transmission, that the configured transmit pin is GPIO4 or GPIO20, and that the service has the permissions required to access the Pi peripherals.

Also correct any configuration error identified in the log. The daemon deliberately does not clear this safety latch after an INI reload, mode change, or transmission-toggle change.

After correcting the cause, restart the service:

```console
sudo systemctl restart wsprrypi.service
```

Then confirm in the log that the configured backend was selected without a startup-inhibition error. After a successful restart, the saved **Enable on Boot** policy determines whether transmission scheduling is enabled.

Do not repeatedly restart the service without correcting the reported cause. If the failure persists, leave transmission disabled and collect a support bundle from **Maintenance** before requesting help.

## Pi 5 RP1 Route Is Unavailable or Mismatched

Leave transmission disabled when the route panel reports **Unavailable**,
**Staged**, **Mismatch**, or **Rollback required**. Do not edit boot files or
enable both overlays manually.

Check that `rp1-gpclk-dkms` version `1.0.0-1` is installed for the running
kernel, the module exposes `/dev/rp1-gpclk0`, both packaged overlays are
present, and exactly one Wsprry Pi-owned route is configured. Requested,
persisted, configured, and active routes must all be GPIO4 or all be GPIO20.
Eligibility and cleanup must also be accepted; Wsprry Pi does not fall back to
another route or backend.

For **Staged**, use the offered reboot or rollback action. For **Mismatch** or
**Rollback required**, preserve the displayed state and collect a support
bundle before making manual changes. The bundle includes package, DKMS,
module, device, overlay, boot-fragment, and journal evidence when readable.
