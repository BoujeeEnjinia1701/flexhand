---
doc_id: FXH-REQ-001
title: FlexHand requirements
project: FlexHand
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
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
---

# FlexHand requirements

These requirements are checked by calculation in FXH-CAL-001. Five are met on paper, three are at risk, two are not met (R7 pack mass and R11 cuff pressure) and three cannot be verified until TRL 4. The targets are unchanged from v0.2: Amish decided on 2026-09-25 to keep the 30 N design load (FXH-DDR-001, D5) and to keep the 450 g pack target until a therapist has been consulted (D1). Proposed changes to R2, R5 and R11 raised by the calculations are listed in FXH-DDR-001 (N1 to N5) and are not applied here.

Table 1. Requirements and TRL 3 status.

| ID | Requirement | Target | Verification | TRL 3 status (FXH-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Move the four fingers through a useful range | MCP 0 to 70°, PIP 0 to 90°, within therapist-set limits | Tendon excursion calculation; later bench test on a finger model | Met: 24.8 mm excursion needed, 29.8 mm stroke |
| R2 | Extend fingers against moderate flexor tone | 30 N extensor tendon force per finger at the finger | Torque and friction calculation; published stiffness data | **At risk:** 0.467 N·m peak at the spool, 119 % of the gearbox's recommended continuous load (RMS 65 %); 30 N covers mild tone (MAS 1+) only, MAS 3 needs about 148 N |
| R3 | Limit force on the hand | Software limit 40 N per finger from motor current; mechanical breakaway at 60 N or less per tendon | Calculation; later bench test | **At risk:** current senses a finger pair, so one finger can reach 80 N before the pair limit trips; friction spreads the estimate from 32 % below to 18 % above the set value |
| R4 | Deliver a high repetition dose | 300 or more full flexion and extension cycles in a 60 min session | Speed calculation | Met: 448 cycles per hour at the fastest setting; holds for strokes up to 5 s |
| R5 | Move slowly and smoothly | Stroke time adjustable from 3 to 15 s (joint speed about 6 to 30 °/s); dwell at each end adjustable | Speed calculation; firmware sketch | **At risk:** fastest stroke at design load 3.3 s (2.6 s unloaded) |
| R6 | Run several sessions per charge | 3 or more 60 min sessions at design load | Power budget | Met: 3.9 sessions at 3.69 Wh each |
| R7 | Light enough to wear seated | Hand-side parts 120 g or less; forearm pack 450 g or less (pack target to be revisited with a therapist, D1) | Mass estimate, then weighing | **Not met:** hand 103 g (met); pack 675 g |
| R8 | Quick to put on and take off | A care partner dons it in 5 min or less and removes it in 1 min or less | Design review with users | Not verifiable at TRL 3; at risk on flexed, spastic fingers |
| R9 | Stop and release on demand | Physical stop cuts motor power within 100 ms; tendons released by hand in 10 s or less without tools | Calculation; later bench test | Not verifiable at TRL 3: stop in about 11 ms by calculation; release time needs a bench test |
| R10 | Fit most adult hands | Hand length 170 to 205 mm with three glove sizes and adjustable cuffs | Anthropometric check | Met on paper: sizes scaled 0.95, 1.00 and 1.15 from the model |
| R11 | Keep contact pressure tolerable | Mean pressure under a finger cuff 50 kPa or less at design load (proposed limit, to be set with a therapist) | Contact area calculation | **Not met:** 46 to 84 kPa; anchor cuffs limited to 12.2 to 18.6 mm by the middle phalanx length |
| R12 | Low cost and buildable | Parts cost $500 or less; no custom PCB for the first build | Priced BOM | Met: $281.90 |
| R13 | Record what was done | Device logs session time, cycle count and peak motor current; therapist limits cannot be changed from the user controls | Design review | Not verifiable at TRL 3: storage ample (1 MB holds decades of summaries) |

## Assumptions

- Design load: 30 N of extensor tendon force per finger at full extension (D5). Checked against the finger stiffness measured by [Heung et al., *Frontiers in Bioengineering and Biotechnology*, 2020](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2020.00111/full): it covers a finger with MAS 1+ tone with a margin of about 1.7, not a finger with MAS 3 tone. It is consistent in scale with the Columbia orthosis, whose single motor provides about 100 N peak for four fingers ([Park et al., arXiv 1802.06131](https://arxiv.org/abs/1802.06131)).
- Tendon excursion for 70° at the MCP and 90° at the PIP is 24.8 mm, taking dorsal moment arms of 10 mm and 8 mm; the stroke adds 5 mm for cuff compliance.
- Transmission efficiency is 0.694: capstan friction with a coefficient of 0.1 over 180° of sheath bend, and one idler at 95 %.
- The forearm rests on a support during sessions. The device is not designed to be worn while walking.
- Sessions are supervised by a care partner, at least until a therapist agrees otherwise.

> **Safety:** R3, R9 and R11 are safety requirements. A design that misses any of them must not be worn by a person, even at TRL 4 bench stage. R11 is not met and R3 is at risk.
