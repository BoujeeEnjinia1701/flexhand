---
doc_id: FXH-DEC-001
title: FlexHand design decisions register
project: FlexHand
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from the review note, FXH-DDR-001 to FXH-DDR-003 and the build plan work
---

# FlexHand design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | First clinical co-design partner | A stroke unit occupational therapy team; a community rehabilitation service; a university rehabilitation lab | None yet | Nothing in the TRL 3 build; the therapist reviews in items 4 and 5 wait on it | FXH-DDR-001, O1 |
| 2 | Accept the design-for-construction changes | (a) accept C1 to C14 as made; (b) ask for changes to any of them | (a) | The whole build plan | FXH-DDR-003, Table 1 |
| 3 | Confirm the pull-out release plate as the tool-free release, in place of the concept's undefined lever | (a) pull-out plate, with pull force and release time measured at TRL 4 against R9's 10 s; (b) a cam lever that drives the same plate (more parts, lower pull force) | (a); move to (b) only if the measured pull is too high for a care partner | Release plate, cover and pucks (build plan 3.15 to 3.17, step 15) | FXH-DDR-003, A1 |
| 4 | The cuffs need the fingers held slightly spread by the glove; spastic fingers may resist it | (a) accept, and have the co-design therapist check it; (b) single-saddle cuffs that fit fingers at rest, with higher pressure (R11 at risk on the little finger) | (a) | Finger cuffs and thimbles (build plan 3.12, 3.13) | FXH-DDR-003, A2 |
| 5 | Forearm pack about 723 g against R7's 450 g target (639 g in the concept) | (a) keep the target under therapist review as already decided (N4 (c), waiting on item 1) and weigh at TRL 4; (b) look for mass now, starting with the savings below | (a), trying the mass savings below before TRL 4 | Pack base, anchor block, fixings | FXH-DDR-003, A3; FXH-DDR-002, N4 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The gearbox face's two M3 holes: spacing (17 mm assumed), how deep a screw may go, and the shaft length (12.5 mm assumed) | They set the bulkhead holes, the 6 mm screw length and how far the spool hub reaches onto the shaft | FXH-DDR-003, C3, C4 |
| 2 | The motor length with its encoder (71 mm assumed) and where the encoder cable leaves | Sets the 6 mm cable gap behind the motors | FXH-DDR-003, C5 |
| 3 | The stop button's body depth (18 mm assumed), bezel and nut | Its body sits between the cells and the motors | FXH-DDR-003, C5 |
| 4 | The sizes of the controller, driver, charger, battery board and regulator modules, and the charger's USB-C port position | They are laid out on the tray, and the port must meet the rear wall opening | FXH-DDR-003, C5 |
| 5 | The cells' length with any protection fitted (65 mm assumed) | The saddles and tray posts leave 0.5 mm at each end | FXH-DDR-003, C5 |
| 6 | The sheath housing's outside diameter (4 mm) and its ferrules' (about 5 mm) | They set the puck, stop block and cover holes | FXH-DDR-003, C7, C11 |
| 7 | The glove's size and stretch against the plate and spacer positions | Plates and spacer are stitched where the model puts them | FXH-DDR-003, C11, C12 |
| 8 | The breakaway couplings' pull-out force (about 60 N) and the stop-bead settings | Set and recorded at TRL 4 | FXH-DDR-002, N3, N4 |

## Value engineering

Value-engineering target: USD 500 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 303.90 (USD 196.10 under the target), from `bom/bom.csv` [J1]. Main cost drivers and savings worth trying:

- **Gearmotors, USD 107.90 (36 %).** The largest line and 214 g of the pack's mass. Worth pricing a lighter 20 to 25 mm gearmotor class with encoder that still carries 0.49 N·m peak; any change reopens R2 and the torque calculation.
- **Battery, stop button and electronic modules, about USD 68.** Standard modules; little to save in cost, but a single dual-channel driver board would save one board, its wiring and a few grams.
- **Anchor block and its hardware, USD 18 plus fixings.** The printed parts are 71 g. A thinner-walled block with the channels as separate tubes, or printing it in a lighter material, is worth trying for mass.
- **Fixing kit, USD 10, 27 g.** Plastic or aluminium screws where loads are small (lid, tray, cover) would save about 8 g.
- **Pack base, 105 g.** Lower infill and thinner ribs could save 10 to 20 g; to check against the motor torque reaction.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D8: 25 mm 227:1 gearmotors on the forearm, two motors, passive motion only, widest anchor cuffs with a soft liner, 30 N design load, passive thumb, tendons in Bowden sheaths, 2S pack | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | FXH-DDR-001 |
| 2026-09-25 | TRL 4 on hold for this repo | Amish, same instruction | `project.yaml` (trl_target), FXH-DDR-001 |
| 2026-09-25 | Items N1 to N5: R2 restated for mild tone, fingertip thimbles, balance pulleys with stop beads, ball-detent couplings and a perforated cuff, 4 s lower stroke limit at design load | Amish: "i accept all your recommendations, go with them across all repos." | FXH-DDR-002 |
| 2026-09-26 | FlexHand in the first batch of product renders | Amish chose the repo (no words recorded) | `docs/REVIEW.md`, session of 2026-09-26 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | FXH-DDR-003 (changes made under this instruction, open for review: item 2) |
| 2026-09-30 | Outstanding decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | This register |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register, Value engineering |
