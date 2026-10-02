---
doc_id: FXH-DEC-001
title: FlexHand design decisions register
project: FlexHand
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from the review note, FXH-DDR-001 to FXH-DDR-003 and the build plan work
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: 'Amish approved the recommendations for all five open decisions on 2026-10-02 (FXH-DDR-003 accepted); moved to decisions made; value engineering states that the mass savings cannot close the R7 gap'
---

# FlexHand design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

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

The mass savings above add up to about 30 to 60 g and cannot close the 273 g gap between the 723 g pack and R7's 450 g target. They are to be tried before TRL 4 (decided 2026-10-02), but the therapist review of the target, which also treats the pack's load on a weak arm and shoulder as a safety question, decides it.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D8: 25 mm 227:1 gearmotors on the forearm, two motors, passive motion only, widest anchor cuffs with a soft liner, 30 N design load, passive thumb, tendons in Bowden sheaths, 2S pack | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | FXH-DDR-001 |
| 2026-09-25 | TRL 4 on hold for this repo | Amish, same instruction | `project.yaml` (trl_target), FXH-DDR-001 |
| 2026-09-25 | Items N1 to N5: R2 restated for mild tone, fingertip thimbles, balance pulleys with stop beads, ball-detent couplings and a perforated cuff, 4 s lower stroke limit at design load | Amish: "i accept all your recommendations, go with them across all repos." | FXH-DDR-002 |
| 2026-09-26 | FlexHand in the first batch of product renders | Amish chose the repo (no words recorded) | `docs/REVIEW.md`, session of 2026-09-26 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | FXH-DDR-003 (changes made under this instruction; accepted on 2026-10-02, below) |
| 2026-09-30 | Outstanding decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | This register |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register, Value engineering |
| 2026-10-02 | First clinical co-design partner: a university rehabilitation lab attached to a stroke service, introduced through the OpenRatio network; first candidate to approach: Shirley Ryan AbilityLab in Chicago, or a university rehabilitation program nearer Irving | Amish: "i approve your recommendations for all 555 open decisions." | FXH-DDR-001, O1 |
| 2026-10-02 | Design for construction accepted: changes C1 to C14 and their knock-on changes, as made; the release (C7) and the finger spread (C10) are confirmed separately in the next two rows | Amish: "i approve your recommendations for all 555 open decisions." | FXH-DDR-003, Tables 1 and 2 |
| 2026-10-02 | Tool-free release: the pull-out plate (option a). Pass mark set before the TRL 4 test: released in 10 s or less (R9) with a pull force that the co-design therapist agrees, before the test, a care partner can apply with one hand; the cam lever (option b) is the fallback if it fails | Amish: "i approve your recommendations for all 555 open decisions." | FXH-DDR-003, A1 |
| 2026-10-02 | Finger spread: option (a), cuffs that hold the fingers slightly spread, but nothing is worn until the co-design therapist has checked the spread on a range of hands with mild tone; switch to single-saddle cuffs if the spread raises tone or discomfort | Amish: "i approve your recommendations for all 555 open decisions." | FXH-DDR-003, A2 |
| 2026-10-02 | Forearm pack about 723 g: keep the 450 g target of R7 under therapist review, treating the pack as a safety question for that review (load on a weak arm and shoulder), and try the listed mass savings before TRL 4 | Amish: "i approve your recommendations for all 555 open decisions." | FXH-DDR-003, A3; FXH-DDR-002, N4 |
