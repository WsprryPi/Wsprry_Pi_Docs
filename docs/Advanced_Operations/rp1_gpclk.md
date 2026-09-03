# Raspberry Pi 5 RP1 GPCLK

On Raspberry Pi 5-family systems, the Wsprry Pi installer resolves, installs,
and validates a compatible RP1-GPCLK-DKMS provider and its route-management
service. Installation establishes neutral administration: neither GPIO4 nor
GPIO20 is selected, the transmission consumer remains absent, and output is
disabled. The `/dev/rp1-gpclk` endpoint normally appears only after an operator
selects and applies a route. Si5351 remains a separate backend choice.

## Installation and ownership

Use the normal Wsprry Pi installer. Do not manually install an additional RP1
provider over an installer-managed one. A repeat installation verifies exact
ownership and identity, safely recovers an existing owned route or neutral
runtime, updates or validates the provider and application, and restores neutral
administration. Foreign, modified, mixed, or unproven provider state is
preserved and reported as a failure for operator review.

Normal uninstall removes the RP1 provider and runtime administration only when
the ownership record and installed identity still match. It does not remove or
adopt an unproven provider. Retained installer failure details and a support
bundle are the preferred evidence when recovery is refused.

Installing the provider does not select a route, change GPIO state, or start a
transmission.

Runtime checks establish application compatibility, not qualification of a
transmitter, band, power level, filter, or RF chain. RP1 development output
requires a current, bounded operation confirmation; saving a route or starting
the application does not authorize transmission.

## Route identities

GPIO4 (header pin 7) and GPIO20 (header pin 38) are separate boot-selected
routes. Wsprry Pi tracks five distinct facts:

- **Requested**: the operator's current draft or transaction request.
- **Persisted**: the route saved in Wsprry Pi configuration.
- **Configured**: the boot route reported by the managed route service.
- **Active**: the route reported by the loaded provider.
- **Eligible**: runtime protocol, capability, route, exclusive ownership, and
  cleanup checks permit the requested operation. Package versions and build
  labels are not an application provisioning whitelist.

Transmission is blocked unless all route identities match and eligibility is
confirmed. There is no automatic route or backend fallback.

## Change a route

1. Stop transmission and wait for committed work, cancellation, cleanup,
   provider leases, and backend transactions to finish.
2. Open **Setup > Transmitter**, select GPIO4 or GPIO20, and review Requested
   and Active.
3. Select **Apply route and reboot**, or select **Cancel** to discard the draft.
4. After restart, confirm the panel reports the selected route as Active.

The application delegates route changes to the managed route service through
its bounded interface. The manager handles boot configuration and rollback;
Wsprry Pi checks transaction generations and reconciles the reported route.
A process failure or unsuccessful reboot request keeps transmission disabled
until reconciliation or rollback succeeds. If the manager is unavailable,
leave transmission disabled and follow the troubleshooting guidance below.

## Diagnostic evidence

Runtime status reports the route facts known to the running application.
Unknown active, eligibility, cleanup, or journal
facts remain explicitly unknown rather than being inferred.

A support bundle adds independent read-only host evidence under
`bundle/hardware/rp1-gpclk` and the corresponding command reports. It records
endpoint presence, route-manager socket state, a route-journal inventory, and
the persisted route when readable. It does not attest provider packages or
overlay hashes. A support bundle does not establish RF qualification.
