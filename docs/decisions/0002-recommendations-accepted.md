---
doc_id: FXH-DDR-002
title: FlexHand recommendations accepted
project: FlexHand
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of the TRL 3 recommendations (N1 to N5) and the changes made to the repo
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items N1 to N5); item O1 remains proposed, awaiting Amish

## Context

FXH-DDR-001 recorded the TRL 2 decisions D1 to D8 and listed five new items raised by the TRL 3 calculations (N1 to N5), each with a recommendation, plus one open item without a recommendation (O1). On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is therefore decided as recommended. Where an item offered several options, the recommended option is the decision. The item without a recommendation stays open. TRL 4 remains on hold by Amish's instruction, so no item is taken beyond paper design.

## Decision

Table 1. Items decided on 2026-09-25 and what changed in the repo.

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| N1 | Severity band and R2 wording | Decided by Amish, 2026-09-25: go with recommendation. Reword R2 to mild flexor tone (MAS 1 to 1+) and keep 30 N. | R2 in FXH-REQ-001 now reads "Extend fingers against mild flexor tone (MAS 1 to 1+)". The problem statement names mild tone as the first severity band. R2 stays at risk, now for the gearbox rating only. |
| N2 | Cuff pressure (R11) | Decided by Amish, 2026-09-25: go with recommendation (a). Add a fingertip thimble that shares the extensor load with the middle-phalanx cuff. | Open-tip TPU thimbles, 13.2 to 19.0 mm wide with a 2 mm liner, added to the model (`thimbles`), BOM line 21 ($4.00), the exploded view and FXH-DWG-001. Worst cuff pressure falls from 84 to 40 kPa (46 kPa on a small hand's little finger). R11 is met on paper. Hand-side mass rises from 103 to 115 g, still within 120 g. |
| N3 | Per-finger force limit (R3) | Decided by Amish, 2026-09-25: go with recommendation (a). A balance pulley in the anchor block so both tendons of a pair carry equal tension. | Four floating 693ZZ-class balance pulleys (BOM line 22, $4.00) in channels in the anchor block, which grows from 12 to 44 mm long for 32 mm of pulley travel. Worst single-finger force at the trip falls from 80 to 40 N. Each finger tendon now carries a stop bead so a free finger cannot run past its range when its partner is blocked. The extra pulley lowers transmission efficiency from 0.694 to 0.659 and raises peak spool torque from 0.467 to 0.492 N·m. R3 stays at risk for friction spread (27 to 47 N at a 40 N setting). |
| N4 | Pack mass (R7) | Decided by Amish, 2026-09-25: go with recommendation, (a) and (b), then (c). | (a) Ball-detent breakaway couplings replace the magnetic ones (8 x 5 g saved, 40 g). (b) The forearm cuff shell and liner are perforated with 12 mm holes (33 % open, 25 g saved). Pack mass falls from 675 to 639 g, still not meeting 450 g. (c) The therapist review of the 450 g target needs a clinical co-design partner (O1), so it is recorded as decided and pending O1; R7 keeps its 450 g target until then. |
| N5 | Stroke-time range (R5) | Decided by Amish, 2026-09-25: go with recommendation. Relax the lower limit to 4 s at design load. | R5 target changed from "3 to 15 s" to "4 to 15 s at design load". The fastest stroke at design load is 3.3 s (3.9 s with pessimistic friction), so R5 is met. At 4 s strokes the dose is 360 cycles per hour, so R4 still holds. |

Budget and pitch: no recommendation changed either. `budget_usd` stays at $500; parts rise from $281.90 to $289.90. The pitch and problem lines in `project.yaml` are unchanged.

## Still open

- **O1.** First clinical co-design partner: a stroke unit occupational therapy team, a community rehabilitation service or a university rehabilitation lab. No recommendation was made. Proposed, awaiting Amish. The therapist review of the pack-mass target (D1, N4 (c)) and of the 50 kPa pressure limit waits on this choice.

## Consequences

- FXH-PRB-001 moves to v0.4, FXH-PRC-001 to v0.4, FXH-REQ-001 to v0.4 and FXH-CAL-001 to v0.2. Drawing FXH-DWG-001 moves to Rev P2.
- Requirement status after the changes: 1 not met (R7 pack mass), 2 at risk (R2 gearbox rating, R3 friction spread), 7 met, 3 not verifiable at TRL 3.
- The load sharing between cuff and thimble is an assumption (shared in proportion to contact area). It, the balance pulley friction and the stop-bead setting need bench checks at TRL 4, which is on hold.
- Cross-repo actions: none.
- TRL 4 work (bench build of a finger-pair drive, pressure mapping, breakaway and release tests) is on hold by Amish's instruction.
