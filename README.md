# InkFrame
Repurposing a Kindle 4 into a distraction-free e-ink art frame, with documentation of tooling, POSIX fixes, and Kindle firmware limitations.

## Planned but Not Completed (Documented for Completeness)

This repository intentionally documents **work that was planned, designed, and partially implemented**, even when it was not carried through to a final production setup.

These decisions were made consciously, based on platform behavior and stability considerations, not due to lack of feasibility or implementation effort.

---

### InkFrame Autostart (System-Level Slideshow)

The original InkFrame concept aimed to implement a fully autonomous slideshow that:

- started automatically at boot
- bypassed the Kindle UI entirely
- rendered images directly to the framebuffer
- rotated images at fixed time intervals
- selected images based on time-of-day buckets
- ran continuously without user interaction

The runtime logic (`inkframe.sh`) and installation logic (`run.sh` / `runme.sh`) were fully written and tested in isolation.

What prevented completion was **not scripting logic**, but system integration reliability.

---

### OTA-Based Installation Workflow

The planned installation path relied on custom OTA update packages built with KindleTool to:

- remount the root filesystem as writable
- install init scripts under `/etc/init.d`
- register boot-time execution via `/etc/rc5.d`
- restore the filesystem to read-only

Despite valid package generation and correct device targeting, the Kindle 4 OTA system proved unreliable for iterative development:

- failed updates were cached internally
- the “Update Your Kindle” menu frequently became unavailable
- failures occurred silently without actionable diagnostics

Further pursuit would have required deeper reverse-engineering of the OTA system or recovery-mode installation.

---

### Launchpad / Script Hook Automation

An alternative approach considered using Launchpad-style script hooks to trigger installation scripts at boot.

This was intentionally not pursued further in order to:

- avoid introducing additional dependencies
- minimize moving parts on a fragile platform
- prevent layering hacks on top of unreliable OTA behavior

The project goal shifted toward reducing system complexity rather than increasing it.

---

### SSH-Based Manual Installation

A direct SSH-based installation path was considered as a technically viable fallback:

- manual placement of init scripts
- direct filesystem modification
- full control over boot-time behavior

This approach was intentionally deferred because:

- it increases the barrier to entry for others
- it requires persistent network configuration
- it introduces higher risk for casual experimentation

The final solution favored approaches that could be reproduced without root shell access.

---

### Continuous Slideshow While Awake

Another planned feature was continuous image rotation while the device remained awake, independent of sleep state.

This was deprioritized due to:

- e-ink refresh limitations
- increased power consumption
- the need for a long-running background process
- higher likelihood of UI interference

The screensaver-based approach aligned better with the physical characteristics of e-ink.

---

### Time-of-Day Awareness

Time-based image selection (morning/day/night) was implemented in the InkFrame runtime logic but not carried forward into the final solution.

This was a deliberate trade-off:

- the screensaver mechanism does not expose time hooks
- adding time awareness would require reintroducing background services
- reliability was prioritized over contextual behavior

The design remains documented for future experimentation.

---

### Why These Items Are Preserved Here

All of the above were:

- technically feasible
- partially or fully implemented
- blocked by platform behavior rather than design flaws

They are documented here to:

- preserve context
- prevent re-discovery of the same limitations
- show the full decision-making process
- clarify that the final solution was chosen, not defaulted to

This repository values **traceability over minimalism**.

---

### Future Revisit Possibilities

Any of the above approaches could be revisited if:

- the device is accessed via SSH exclusively
- recovery-mode installation is acceptable
- the project targets experimentation rather than stability

For the stated goal of a reliable e-ink art frame, they were intentionally left archived.
