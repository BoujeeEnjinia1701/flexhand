---
doc_id: FXH-REQ-001
title: FlexHand requirements
project: FlexHand
doc_type: Requirements
version: "0.2"
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
---

# FlexHand requirements

These are first-pass requirements for the concept. Targets are proposals for review with a therapist and will be checked by calculation at TRL 3. The status column gives the TRL 2 estimate from the design precis (FXH-PRC-001); two requirements are not met and two are at risk.

Table 1. Requirements and concept status.

| ID | Requirement | Target | Verification (TRL 3 or later) | Concept status (estimate) |
| --- | --- | --- | --- | --- |
| R1 | Move the four fingers through a useful range | MCP 0 to 70°, PIP 0 to 90°, within therapist-set limits | Tendon excursion calculation; later bench test on a finger model | Met by design: about 25 mm tendon excursion needed, 35 mm provided |
| R2 | Extend fingers against moderate flexor tone | 30 N extensor tendon force per finger at the finger | Torque and friction calculation | Met, thin margin: 0.41 N·m at the spool, about 5 % above the gearbox's recommended continuous load |
| R3 | Limit force on the hand | Software limit 40 N per finger from motor current; mechanical breakaway at 60 N or less per tendon | Calculation; later bench test | By design, unverified |
| R4 | Deliver a high repetition dose | 300 or more full flexion and extension cycles in a 60 min session | Speed calculation | Met: about 6.4 cycles per min, about 385 per hour at design load |
| R5 | Move slowly and smoothly | Stroke time adjustable from 3 to 15 s (joint speed about 6 to 30 °/s); dwell at each end adjustable | Firmware sketch and speed calculation | Met by design |
| R6 | Run several sessions per charge | 3 or more 60 min sessions at design load | Power budget | Met, no margin: about 3.1 sessions |
| R7 | Light enough to wear seated | Hand-side parts 120 g or less; forearm pack 450 g or less | Mass estimate, then weighing | **Not met:** hand about 90 g (met), pack about 510 g |
| R8 | Quick to put on and take off | A care partner dons it in 5 min or less and removes it in 1 min or less | Design review with users | **At risk:** tendon cuffs on flexed, spastic fingers may be hard to fit |
| R9 | Stop and release on demand | Physical stop cuts motor power within 100 ms; tendons released by hand in 10 s or less without tools | Design review; later bench test | By design, unverified |
| R10 | Fit most adult hands | Hand length 170 to 205 mm with three glove sizes and adjustable cuffs | Anthropometric check | By design |
| R11 | Keep contact pressure tolerable | Mean pressure under a finger cuff 50 kPa or less at design load (proposed limit, to be set with a therapist) | Contact area calculation | **Not met:** about 100 kPa with 12 mm cuffs |
| R12 | Low cost and buildable | Parts cost $500 or less; no custom PCB for the first build | Priced BOM | Met: about $280 |
| R13 | Record what was done | Device logs session time, cycle count and peak motor current; therapist limits cannot be changed from the user controls | Design review | By design |

## Assumptions

- Design load: a finger with moderate flexor tone needs about 30 N of extensor tendon force to reach full extension at the set speed. This is an estimate consistent with the Columbia orthosis, whose single motor provides about 100 N peak for four fingers ([Park et al., arXiv 1802.06131](https://arxiv.org/abs/1802.06131)). It must be checked against published finger stiffness data at TRL 3.
- Tendon excursion for 70° at the MCP and 90° at the PIP is about 25 mm, taking dorsal moment arms of about 10 mm and 8 mm; 35 mm is allowed for cuff compliance and slack.
- Bowden sheath efficiency is about 73 %, from the capstan relation with a friction coefficient of 0.1 and a total bend of 180° (π rad).
- The forearm rests on a support during sessions. The device is not designed to be worn while walking.
- Sessions are supervised by a care partner, at least until a therapist agrees otherwise.

> **Safety:** R3, R9 and R11 are safety requirements. A design that misses any of them must not be worn by a person, even at TRL 4 bench stage.
