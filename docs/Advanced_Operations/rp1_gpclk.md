# Raspberry Pi 5 RP1 GPCLK

Wsprry Pi can optionally use the released `rp1-gpclk-dkms` version `1.0.0-1`
provider for direct GPIO clock output on Raspberry Pi 5. This is an
installation and runtime compatibility path, not evidence that a transmitter,
band, power level, filter, or RF chain is qualified.

## Route identities

GPIO4 (header pin 7) and GPIO20 (header pin 38) are separate boot-selected
routes. Wsprry Pi tracks five distinct facts:

- **Requested**: the operator's current draft or transaction request.
- **Persisted**: the route saved in Wsprry Pi configuration.
- **Configured**: the route selected by Wsprry Pi's owned boot fragment.
- **Active**: the route reported by the loaded provider.
- **Eligible**: exact package, UAPI, compatibility, route, capability, and
  cleanup checks permit provider acquisition.

Transmission is blocked unless all route identities match and eligibility is
confirmed. There is no automatic route or backend fallback.

## Change a route

1. Stop transmission and wait for committed work, cancellation, cleanup,
   provider leases, and backend transactions to finish.
2. Open **Setup > Transmitter**, select GPIO4 or GPIO20, and review Requested
   and Active.
3. Select **Apply route and reboot**, or select **Cancel** to discard the draft.
4. After restart, confirm the panel reports the selected route as Active.

Wsprry Pi owns only its bounded boot fragment. It journals every mutating phase,
uses generation checks and atomic replacement, and preserves the prior owned
state for rollback. A process failure or unsuccessful reboot request keeps
transmission disabled until reconciliation or rollback succeeds.

## Diagnostic evidence

Runtime status reports the expected package identity and the route facts known
to the running application. Unknown active, eligibility, cleanup, or journal
facts remain explicitly unknown rather than being inferred.

A support bundle adds independent read-only host evidence under
`bundle/hardware/rp1-gpclk` and the corresponding command reports. Review the
package version, current-kernel DKMS status, `modinfo`, device presence, overlay
digests, owned boot fragment, and route journal together. Package installation
or a successful DKMS build does not by itself prove live eligibility or RF
qualification.
