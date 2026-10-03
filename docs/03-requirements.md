---
doc_id: FXH-REQ-001
title: FlexHand requirements
project: FlexHand
doc_type: Requirements
version: "0.7"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with concept status
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from FXH-CAL-001; decisions of FXH-DDR-001 applied (design load kept, R7 target kept pending therapist review, 20 mm cuff limit)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); R2 reworded to mild tone, R5 lower limit 4 s at design load, status from FXH-CAL-001 v0.2
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status from FXH-CAL-001 v0.3 for the constructable design (FXH-DDR-003); R12 reported against the value-engineering target
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Decisions of 2026-10-02 (FXH-DEC-001): R9 release pull force agreed with the therapist before the test; R7 pack target reviewed as a safety question; no wearing before the finger spread check. No status changed'
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R7 value updated to 712 g after the mass savings tried on 2026-10-02; status unchanged (not met)"
---

# FlexHand requirements

These requirements are checked by calculation in FXH-CAL-001 v0.3, for the constructable design of FXH-DDR-003. Seven are met on paper, two are at risk (R2 and R3), one is not met (R7, forearm pack mass) and three cannot be verified until TRL 4. On 2026-09-25 Amish accepted the recommendations raised by the TRL 3 calculations (FXH-DDR-002): R2 now names mild flexor tone (N1), and the lower end of the R5 stroke-time range is 4 s at design load (N5). The fingertip thimble (N2), the balance pulleys (N3) and the lighter couplings and perforated cuff (N4) are in the design. The 450 g pack target stays until a therapist has reviewed it, which waits on the choice of a clinical co-design partner (FXH-DDR-001, D1 and O1).

Table 1. Requirements and TRL 3 status.

| ID | Requirement | Target | Verification | TRL 3 status (FXH-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Move the four fingers through a useful range | MCP 0 to 70°, PIP 0 to 90°, within therapist-set limits | Tendon excursion calculation; later bench test on a finger model | Met: 24.8 mm excursion needed, 29.8 mm stroke |
| R2 | Extend fingers against mild flexor tone (MAS 1 to 1+) (N1) | 30 N extensor tendon force per finger at the finger | Torque and friction calculation; published stiffness data | **At risk:** 30 N covers the 18 N a MAS 1+ finger needs; 0.492 N·m peak at the spool, 125 % of the gearbox's recommended continuous load (RMS 68 %, peak 63 % of intermittent) |
| R3 | Limit force on the hand | Software limit 40 N per finger from motor current; mechanical breakaway at 60 N or less per tendon | Calculation; later bench test | **At risk:** the balance pulleys (N3) keep both fingers of a pair at equal tension, so the pair limit holds each finger to 40 N (was up to 80 N); friction still spreads the force from 27 to 47 N at a 40 N setting |
| R4 | Deliver a high repetition dose | 300 or more full flexion and extension cycles in a 60 min session | Speed calculation | Met: 445 cycles per hour at full speed; 360 at the 4 s lower stroke limit; holds for strokes up to 5 s |
| R5 | Move slowly and smoothly | Stroke time adjustable from 4 to 15 s at design load (N5), down to 3 s at lighter loads; joint speed 30 °/s or less; dwell at each end adjustable | Speed calculation; firmware sketch | Met: fastest stroke at design load 3.3 s (3.9 s with pessimistic friction; 2.6 s unloaded) |
| R6 | Run several sessions per charge | 3 or more 60 min sessions at design load | Power budget | Met: 3.8 sessions at 3.80 Wh each |
| R7 | Light enough to wear seated | Hand-side parts 120 g or less; forearm pack 450 g or less (pack target to be revisited with a therapist, D1, treating the pack's load on a weak arm and shoulder as a safety question; decided 2026-10-02) | Mass estimate, then weighing | **Not met:** hand 117 g (met); pack 712 g in the constructable design (639 g in the concept, 675 g before N4) |
| R8 | Quick to put on and take off | A care partner dons it in 5 min or less and removes it in 1 min or less | Design review with users | Not verifiable at TRL 3; at risk on flexed, spastic fingers |
| R9 | Stop and release on demand | Physical stop cuts motor power within 100 ms; tendons released by hand in 10 s or less without tools, with a pull force that the co-design therapist agrees, before the TRL 4 test, a care partner can apply with one hand (decided 2026-10-02) | Calculation; later bench test | Not verifiable at TRL 3: stop in about 11 ms by calculation; release time needs a bench test |
| R10 | Fit most adult hands | Hand length 170 to 205 mm with three glove sizes and adjustable cuffs | Anthropometric check | Met on paper: sizes scaled 0.95, 1.00 and 1.15 from the model |
| R11 | Keep contact pressure tolerable | Mean pressure under a finger cuff or thimble 50 kPa or less at design load (proposed limit, to be set with a therapist) | Contact area calculation | Met on paper: 23 to 40 kPa on the medium hand, 46 kPa worst on a small hand's little finger, with the fingertip thimble sharing the load (N2; was 46 to 84 kPa); load sharing assumed, to check at TRL 4 |
| R12 | Low cost and buildable | Parts cost against the USD 500 value-engineering target (a control target, not a limit); no custom PCB for the first build | Priced BOM | Estimated cost USD 304.90, USD 195.10 under the target; no custom PCB |
| R13 | Record what was done | Device logs session time, cycle count and peak motor current; therapist limits cannot be changed from the user controls | Design review | Not verifiable at TRL 3: storage ample (1 MB holds decades of summaries) |

## Assumptions

- Design load: 30 N of extensor tendon force per finger at full extension (D5). Checked against the finger stiffness measured by [Heung et al., *Frontiers in Bioengineering and Biotechnology*, 2020](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2020.00111/full): it covers a finger with MAS 1+ tone with a margin of about 1.7, not a finger with MAS 3 tone. It is consistent in scale with the Columbia orthosis, whose single motor provides about 100 N peak for four fingers ([Park et al., arXiv 1802.06131](https://arxiv.org/abs/1802.06131)).
- Tendon excursion for 70° at the MCP and 90° at the PIP is 24.8 mm, taking dorsal moment arms of 10 mm and 8 mm; the stroke adds 5 mm for cuff compliance.
- Transmission efficiency is 0.659: capstan friction with a coefficient of 0.1 over 180° of sheath bend, one idler at 95 % and one balance pulley at 95 %.
- The extensor load of each finger is shared by the middle-phalanx cuff and the fingertip thimble in proportion to their contact areas.
- The forearm rests on a support during sessions. The device is not designed to be worn while walking.
- Sessions are supervised by a care partner, at least until a therapist agrees otherwise.

> **Safety:** R3, R9 and R11 are safety requirements. A design that misses any of them must not be worn by a person, even at TRL 4 bench stage. R11 is met only on paper and R3 is at risk, so nothing may be worn on the strength of these numbers. Nothing is worn either until the co-design therapist has checked the finger spread the cuffs need on a range of hands with mild tone (FXH-DEC-001, 2026-10-02).
