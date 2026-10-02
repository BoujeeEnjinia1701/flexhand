---
doc_id: FXH-DDR-001
title: FlexHand TRL 2 review decisions
project: FlexHand
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review points; list open items and new items from FXH-CAL-001
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'O1 (first clinical co-design partner) decided by Amish on 2026-10-02'
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items D1 to D8; items N1 to N5 accepted on 2026-09-25, see FXH-DDR-002); item O1 decided by Amish on 2026-10-02 (FXH-DEC-001)

## Context

The TRL 2 review note (`docs/REVIEW.md`, session of 2026-09-25, /populate) listed nine design choices marked "Proposed, awaiting Amish". On 2026-09-25 Amish reviewed the review points for every repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided as recommended. The item without a recommendation stays open. TRL 4 is on hold by the same instruction.

FlexHand does not use the portfolio's SwapCell pack, so the cross-cutting SwapCell interface decisions (wake method, charge-while-discharging mode, latch vibration rating, shared pack pricing) do not apply to this design.

## Options considered

Table 1. Items with a recommendation in the TRL 2 review.

| # | Item | Options | Recommendation |
| --- | --- | --- | --- |
| D1 | Motor route (drives R2 and R7) | (a) 25 mm 227:1 gearmotors on the forearm; (b) micro (N20) gearmotors with a 20 N force target; (c) bench-top motor unit with longer sheaths | (a) for the first build; revisit the 450 g pack target with a therapist, since the forearm rests on a support during sessions |
| D2 | Motor count | One motor for four fingers; two motors (one per finger pair); four motors | Two |
| D3 | Passive only or plan for active assist (pitch-level) | Passive motion only; passive plus an active-assist mode triggered by the user's effort | Keep the pitch as passive motion for TRL 3; record active assist as a later option |
| D4 | Cuff pressure fix (R11) | Wider padded cuffs; a distal anchor; a lower force limit | 20 mm cuffs with a soft liner, checked for PIP clearance at TRL 3 |
| D5 | Design load | 30 N per finger for mild to moderate flexor tone; higher or lower | Keep 30 N and check against published stiffness data |
| D6 | Thumb | Passive with an abduction spacer; actuated | Passive for TRL 3 |
| D7 | Actuation | Tendons through Bowden sheaths; pneumatic glove | Tendons |
| D8 | Pack voltage | 2S (7.4 V nominal) with 12 V rated motors; 3S | Keep 2S |

## Decision

- **D1.** Decided by Amish, 2026-09-25: go with recommendation. Two Pololu 4869 class 25D 227:1 gearmotors on the forearm. The 450 g pack target in R7 stays in FXH-REQ-001 until a therapist has been consulted; FXH-CAL-001 shows about 675 g, so R7 is not met.
- **D2.** Decided by Amish, 2026-09-25: go with recommendation. Two motors: index and middle on motor 1, ring and little on motor 2.
- **D3.** Decided by Amish, 2026-09-25: go with recommendation. Passive motion only for TRL 3. An active-assist mode (user effort sensed by motor current or surface EMG) is recorded as a later option. The pitch and problem lines in `project.yaml` are unchanged.
- **D4.** Decided by Amish, 2026-09-25: go with recommendation. Anchor cuffs up to 20 mm wide with a 2 mm soft liner, checked for PIP clearance. The check in FXH-CAL-001 (section H) shows that a 20 mm cuff does not fit on any middle phalanx with 3 mm clearance to the joint creases. The model therefore uses the widest cuff that fits (12.2 to 18.6 mm), and R11 is still not met. See N2.
- **D5.** Decided by Amish, 2026-09-25: go with recommendation. The design load stays 30 N per finger. The check against published stiffness data (FXH-CAL-001, section B) shows it covers mild tone (MAS 1+) with a margin of about 1.7 but not MAS 3, which needs about 148 N. See N1.
- **D6.** Decided by Amish, 2026-09-25: go with recommendation. Thumb held passively in abduction by a spacer.
- **D7.** Decided by Amish, 2026-09-25: go with recommendation. UHMWPE tendons in PTFE-lined Bowden sheaths.
- **D8.** Decided by Amish, 2026-09-25: go with recommendation. 2S Li-ion pack (7.2 V under load) driving 12 V rated motors.

Budget and pitch: the TRL 2 review made no recommendation to change either, so `budget_usd` stays at $500 and the pitch and problem lines are unchanged.

Items that remained open (no recommendation was made, so they stayed "Proposed, awaiting Amish" until Amish decided them on 2026-10-02):

- **O1.** First clinical co-design partner: a stroke unit occupational therapy team, a community rehabilitation service or a university rehabilitation lab. No recommendation; portfolio guidance is that community designs pick co-design partners per area later. Decided by Amish, 2026-10-02, as recommended in FXH-DEC-001: a university rehabilitation lab attached to a stroke service, introduced through the OpenRatio network; first candidate to approach: Shirley Ryan AbilityLab in Chicago, or a university rehabilitation program nearer Irving.

New items raised by FXH-CAL-001 at TRL 3. Amish accepted all recommendations later on 2026-09-25 ("i accept all your recommendations, go with them across all repos"); the changes are recorded in FXH-DDR-002:

- **N1.** Severity band and R2 wording. Options: (a) reword R2 to "mild flexor tone (MAS 1 to 1+)" and keep 30 N; (b) raise the design load toward moderate tone (MAS 2 to 3 needs about 80 to 150 N), which needs larger motors and makes R7 worse. Recommendation: (a) for the first build. Decided by Amish, 2026-09-25: go with recommendation (FXH-DDR-002).
- **N2.** Cuff pressure (R11). Options: (a) add a fingertip thimble that shares the extensor load with the middle-phalanx cuff (about 23 to 40 kPa); (b) a lower force limit on the little finger; (c) review the 50 kPa limit with a therapist. Recommendation: (a). Decided by Amish, 2026-09-25: go with recommendation (FXH-DDR-002).
- **N3.** Per-finger force limit (R3). Current sensing sees the sum of a finger pair, so one finger could carry up to 80 N before a 40 N per finger limit trips. Options: (a) a balance pulley in the anchor block so both tendons of a pair carry equal tension; (b) set the pair limit to 40 N total; (c) rely on the 60 N breakaway. Recommendation: (a). Decided by Amish, 2026-09-25: go with recommendation (FXH-DDR-002).
- **N4.** Pack mass (R7), about 675 g against 450 g. Options: (a) ball-detent breakaways instead of magnets (about 40 g lighter); (b) a lighter, perforated cuff shell; (c) a relaxed target agreed with a therapist (see D1); (d) move the cells to a pouch on the forearm support. Recommendation: (a) and (b), then (c). Decided by Amish, 2026-09-25: go with recommendation (FXH-DDR-002); (c) waits on O1.
- **N5.** Stroke-time range (R5). The fastest extension at design load is about 3.3 s against the 3 s lower limit. Recommendation: relax the lower limit to 4 s at design load, which is also gentler; R4 still holds for strokes up to 5 s. Decided by Amish, 2026-09-25: go with recommendation (FXH-DDR-002).

## Consequences

- FXH-PRB-001, FXH-PRC-001 and FXH-REQ-001 move to v0.3: the decided choices are no longer "proposed", and the requirement status comes from FXH-CAL-001.
- The TRL 3 layout places the gearmotors along the forearm with the spools at the front and idlers turning the tendons forward; this narrows the pack to 76 mm (FXH-DWG-001).
- R7 and R11 are not met; R2, R3 and R5 are at risk. Items N1 to N5 were applied to the design after Amish accepted them (FXH-DDR-002).
- TRL 4 work (test articles, bench tests, build procedures) is on hold by Amish's instruction.
