---
doc_id: FXH-CAL-001
title: FlexHand sizing calculations
project: FlexHand
doc_type: Calculation
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (excursion, design load, torque, speed, force limit, energy, mass, cuff pressure, stop, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); balance pulleys, fingertip thimbles, ball-detent couplings, perforated cuff, R2 and R5 restated; all results recomputed
- version: "0.3"
  date: '2026-10-01'
  author: Amish Chadha
  change: Constructable design (FXH-DDR-003); masses recomputed from the new parts, cost reported against the value-engineering target
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'R9 target wording in the requirement table follows the decision of 2026-10-02 (release pull force agreed with the therapist); no result changed'
---

# FlexHand sizing calculations

On paper, FlexHand now meets seven of its thirteen requirements, has two at risk, misses one and has three that cannot be verified at TRL 3. This version applies the decisions Amish accepted on 2026-09-25 (FXH-DDR-002): a fingertip thimble on each finger, a balance pulley on each spool line, ball-detent breakaway couplings, a perforated forearm cuff, R2 restated for mild flexor tone and a 4 s lower stroke limit at design load. Version 0.3 recomputes the masses and cost for the constructable design of FXH-DDR-003. The one miss is the forearm pack mass, about 723 g against 450 g (R7). The two at risk are the force requirement (R2), where the gearbox runs 25 % above its recommended continuous load at the peak, and the force limit (R3), where sheath friction spreads the force at a given current setting. Cuff pressure (R11) is now met on paper, at 40 kPa worst on the medium hand. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [C2], is the line of that script's output that carries it.

> **Safety:** FlexHand is a research and educational prototype, not a medical device. These are first-principles estimates for a paper proof of concept. They do not show that the device is safe to wear. R3, R9 and R11 are safety requirements; R11 is met only on paper under an assumed load sharing and R3 is at risk, so nothing may be worn on the strength of this note. See FXH-PRC-001, Safety.

## Scope and method

The note checks every requirement in FXH-REQ-001 v0.5 against the design in FXH-PRC-001 v0.5 and the parametric model `cad/src/model.py`. The script imports the model, so the pack, spool, cuff and sheath dimensions used here are the ones in the STEP files and in drawing FXH-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is one 60 min seated session on a medium adult hand (model hand length about 179 mm), with the forearm resting on a support and the wrist near neutral. Each motor drives one finger pair (D2): motor 1 the index and middle fingers, motor 2 the ring and little fingers. Each spool line runs to a floating balance pulley in the anchor block, which splits it into the two finger tendons of the pair (N3).

## Assumptions

Table 1. Main assumptions.

| Area | Assumption | Basis |
| --- | --- | --- |
| Joint range | MCP 0 to 70°, PIP 0 to 90° (R1); DIP not driven | FXH-REQ-001 |
| Moment arms | Extensor 10 mm at the MCP and 8 mm at the PIP; flexor 11 mm and 8 mm | Engineering estimate with cuffs and liner; to measure on a finger model |
| Tendon force | Extension rises linearly from 3 N to 30 N per finger over the stroke (joint stiffness is close to linear with angle); flexion 5 N per finger | D5 design load; stiffness data below |
| Finger stiffness | MCP 0.089 and PIP 0.092 N·m/rad for a MAS 1+ subject; 0.631 and 0.753 N·m/rad for a MAS 3 subject | [Heung et al., *Frontiers in Bioengineering and Biotechnology*, 2020](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2020.00111/full); small sample |
| Transmission | Capstan friction in the sheath, μ = 0.10 over 180° total bend; one idler at 95 %; one balance pulley at 95 %. Pessimistic case μ = 0.15 over 270° (flexed wrist) | Handbook range for UHMWPE on PTFE; bearing pulleys estimated |
| Spool | 10 mm core, 0.8 mm line, first-layer effective radius 5.4 mm | Model |
| Gearmotor | Pololu 4869, 227:1, 12 V: 35 rpm and 0.10 A no load, 1.8 A and 2.35 N·m (24 kg·cm) stall, 0.39 N·m recommended continuous and 0.78 N·m intermittent, 107 g; linear DC model | [Pololu 4869 specifications](https://www.pololu.com/product/4869/specs), checked 2026-09-25 |
| Supply | 7.2 V at the motor under load (2S pack less driver drop); two 2,500 mAh 18650 cells, 18 Wh, 80 % usable | D8 |
| Controller | 0.40 W continuous for ESP32-S3, idle drivers, LED and regulator | Estimate |
| Cycle | Full-voltage strokes (fastest setting), 1 s dwell at each end; full torque held with motor current during the extended dwell. R5 lower limit 4 s at design load | Conservative: the gearbox may hold without current; N5 |
| Cuff contact | Mean pressure = design tendon force / ((anchor cuff width + thimble width) x contact arc), that is, the cuff and the thimble share the load in proportion to area; contact arc 62 % of finger circumference; 3 mm clearance from each joint crease; phalanx shares 47, 28 and 25 % of finger length | Contact-area method named in R11; load sharing assumed (N2), to check at TRL 4; phalanx shares are typical adult values |
| Materials | PETG 1.27, TPU 1.21, PA12 1.01, EVA foam 0.07 g/cm³; printed parts solid except the anchor block (40 % fill); ball-detent coupling 2 g (magnetic 7 g) | Typical; coupling masses estimated |

## A. Tendon excursion (R1)

- The extensor tendon must travel 24.8 mm to take the MCP through 70° and the PIP through 90°; the flexor travels 26.0 mm, a mismatch of 1.2 mm that the slack spring on each tendon takes up [A1].
- With 5 mm allowed for cuff and liner compliance, the stroke is 29.8 mm, or 0.88 turns of the spool. One layer of line in each groove holds about 95 mm, so the line never stacks [A2].
- **R1 is met.**

## B. Design load against published stiffness (basis of R2)

Heung and colleagues measured finger joint stiffness in people after stroke. To hold a finger straight from full flexion, a single extensor tendon crossing both joints must supply the larger of the MCP and PIP moments divided by their moment arms.

- A finger with MAS 1+ tone needs about 18.1 N; a finger with MAS 3 tone needs about 147.9 N [B1].
- The 30 N design load therefore covers PIP stiffness up to 0.153 N·m/rad, about 1.7 times the MAS 1+ value [B2].
- **Consequence:** 30 N suits mild flexor tone (MAS 1 to 1+). Moderate to severe tone needs roughly 80 to 150 N per finger, which this drive cannot supply within the gearbox rating. Amish accepted the recommendation to restate R2 for mild tone (N1, FXH-DDR-002), so R2 now matches the design load.

## C. Transmission and torque (R2)

- Transmission efficiency is 0.659 at neutral wrist and 0.445 in the pessimistic case [C1]. The balance pulley (N3) costs about 5 % against v0.1 (0.694).
- At 30 N per finger, the spool line carries 91.0 N, which at 5.4 mm is a peak torque of 0.492 N·m: 125 % of the gearbox's recommended continuous load and 63 % of its intermittent limit. The pessimistic case gives 0.728 N·m, still inside the intermittent limit [C2].
- At 7.2 V the linear motor model gives R = 6.67 Ω, kt = 1.384 N·m/A and a stall torque of 1.36 N·m; the peak is 36 % of stall [C3].
- The peak lasts only at the end of the extension stroke and during the dwell. The RMS torque over a full cycle is 0.269 N·m, 68 % of the continuous rating [C4].
- **R2 is at risk:** the drive delivers the 30 N target, which covers mild tone as R2 now states, but the peak exceeds the continuous gearbox rating.

## D. Speed, cycle and dose (R4, R5)

- At 7.2 V with no load the spool turns at 20.2 rpm and the tendon moves at 11.4 mm/s, so an unloaded stroke takes 2.61 s [D1].
- At design load the fastest extension takes 3.31 s (3.86 s in the pessimistic case) and flexion 2.78 s. With 1 s dwell at each end, a cycle takes 8.08 s [D2].
- That is 7.42 cycles per minute, or 445 per hour. R4 (300 per hour) still holds with strokes as slow as 5.0 s [D3].
- At the fastest extension the MCP moves at 21.2 °/s and the PIP at 27.2 °/s, inside the 30 °/s limit in the safety section [D4].
- At the 4 s lower stroke limit that R5 now sets at design load (N5), the dose is 360 cycles per hour [D5].
- **R4 is met.** **R5 is met:** even with pessimistic friction the fastest stroke at design load (3.9 s) is quicker than the 4 s lower limit, so the full 4 to 15 s range is available by slowing the motor.

## E. Force limit (R3)

- A 40 N per finger limit on a pair corresponds to 0.655 N·m at the spool and a trip current of 0.573 A. The peak design current is 0.455 A, so the limit sits about 26 % above normal running [E1].
- With the balance pulley (N3), both tendons of a pair carry the same tension, so the pair limit holds each finger to 40 N. Without it, one finger could carry 80 N while its partner is slack [E2].
- Sheath friction varies with wrist posture and wear. A current limit set for 40 N means 27 to 47 N at the fingers across friction coefficients of 0.15 to 0.05 [E3].
- The floating pulley has 30 mm of free travel in its channel, more than the 29.8 mm stroke. If one finger of a pair is blocked, the pulley lets the other move up to 59.6 mm, twice its range. Each finger tendon therefore carries a crimped stop bead that meets its sheath stop at the end of that finger's set range [E4]. The encoder sees only the pulley position.
- **R3 is at risk:** the per-finger limit now holds in principle, but friction spreads the force estimate from about 32 % below to 18 % above the set value, and the breakaway force and stop beads cannot be verified until TRL 4.

## F. Energy (R6)

- Per motor and cycle: 7.29 J for extension, 3.18 J for flexion and 3.28 J to hold the fingers extended for 1 s at 0.46 A [F1].
- Per 60 min session at 445 cycles: motors 3.40 Wh, of which 0.48 Wh reaches the spool shafts and 0.32 Wh the finger joints; controller 0.40 Wh; total 3.80 Wh, an average of 3.80 W and 0.53 A [F2].
- The 18 Wh pack gives 14.4 Wh usable, or 3.8 sessions per charge [F3]. The gearmotor runs far from its efficiency peak at this voltage and load, so most of the energy is lost in the motor and gearbox (Figure 2 of FXH-PRC-001).
- **R6 is met,** with a margin of about 27 %.

## G. Mass (R7)

Table 2. Forearm pack mass of the constructable design [G1], [G2].

| Part | Mass |
| --- | --- |
| Forearm cuff, perforated: PETG shell 51.9 g, EVA liner 4.0 g, two straps 16.0 g | 71.9 g |
| Pack base 105.3 g (with bulkhead, cradle, saddles and posts), lid 31.6 g, electronics tray 6.7 g (PETG) | 143.6 g |
| Gearmotors (2) | 214.0 g |
| Spools 2.8 g, idler bearings 6.0 g | 8.8 g |
| Cells (2) and BMS | 95.0 g |
| Controller, drivers, charger and 5 V regulator | 16.0 g |
| Emergency stop | 20.0 g |
| Anchor block (53 mm, 40 % infill), release plate, cover and pucks | 71.2 g |
| 8 ball-detent couplings and 4 slack springs | 20.0 g |
| Balance pulleys (4) | 6.0 g |
| Wiring | 15.0 g |
| Screws, inserts and pins (from the model's volumes) | 27.0 g |
| Half of the sheaths (0.85 m in total, 29 g) | 14.7 g |
| **Forearm pack** | **723 g (1.59 lb)** |

Table 3. Hand-side mass [G3], [G4].

| Part | Mass |
| --- | --- |
| Base glove (bought) | 40.0 g |
| Dorsal and palmar plates with sheath stop blocks (TPU) | 21.0 g |
| Finger cuffs (8, TPU) and liners | 21.7 + 1.7 g |
| Fingertip thimbles (4, TPU) and liners | 10.3 + 1.0 g |
| Thumb spacer, tendons and stop beads | 4.0 + 2.3 g |
| Half of the sheaths | 14.7 g |
| **Hand side** | **117 g** |

- N4 savings: ball-detent couplings save 40 g against the magnetic couplings, and 12 mm perforations (33 % open) save 25.4 g of cuff shell [G5].
- The constructable design (FXH-DDR-003) adds about 84 g to the pack against v0.2: the motor bulkhead, cradle, cell saddles, tray posts and raised floor (pack base 105 g, was 79 g), the longer anchor block with its release plate, cover and pucks (71 g printed, was 39 g), screws, inserts and pins counted from the model (27 g, against 10 g allowed before), the tray (7 g) and the regulator (3 g). Four slack springs replace eight (4 g less).
- **R7 is not met:** the hand side (117 g) is within 120 g, but the forearm pack is about 723 g against 450 g (639 g in v0.2). The gearmotors alone are 214 g. The remaining step in N4, a pack target agreed with a therapist, waits on the choice of a clinical co-design partner (O1); savings worth trying are listed in the design decisions register.

## H. Cuff contact pressure (R11) and fit (R10)

- The TRL 2 basis, 30 N over a 12 mm by 25 mm patch, gave 100 kPa [H1].
- D4 called for 20 mm anchor cuffs checked for PIP clearance. With 3 mm clearance to each joint crease, the widest cuff that fits on the middle phalanx is 16.4 mm (index), 18.6 mm (middle), 17.0 mm (ring) and 12.2 mm (little); a 20 mm cuff fits on none of them. Alone, these cuffs give 46 to 84 kPa [H2].
- N2 adds an open-tip thimble on each distal phalanx, from 3 mm beyond the DIP crease to the tip, and runs the extensor tendon on to it past the anchor cuff so the two share the load.

Table 4. Anchor cuff plus thimble pressure at 30 N, medium hand [H2].

| Finger | Middle phalanx, cuff | Distal phalanx, thimble | Contact arc | Pressure (cuff alone) |
| --- | --- | --- | --- | --- |
| Index | 22.4 mm, 16.4 mm | 20.0 mm, 17.0 mm | 35.1 mm | 26 kPa (52) |
| Middle | 24.6 mm, 18.6 mm | 22.0 mm, 19.0 mm | 35.1 mm | 23 kPa (46) |
| Ring | 23.0 mm, 17.0 mm | 20.5 mm, 17.5 mm | 33.1 mm | 26 kPa (53) |
| Little | 18.2 mm, 12.2 mm | 16.2 mm, 13.2 mm | 29.2 mm | 40 kPa (84) |

- On a small hand the little finger reaches 46 kPa (96 kPa with the cuff alone); on a large hand 29 kPa [H3].
- **R11 is met on paper:** every finger in every size is at or under 46 kPa. Two cautions remain: the load split between cuff and thimble is assumed, not calculated from finger mechanics, and the mean-pressure metric ignores skin shear and edge pressure. Both need a bench check at TRL 4.
- **R10 is met on paper:** three glove sizes scaled at 0.95, 1.00 and 1.15 from the model cover hand lengths of 170 to 205 mm, with cuff and thimble widths set per size [H3]. A fit trial is still needed.

## I. Stop and release (R9)

- The stop switch opens the motor supply. The 100 µF bulk capacitance keeps the motors turning for about 0.8 ms, contact opening takes up to about 5 ms and the rotor runs down in about 5 ms, so motion stops in about 11 ms against 100 ms [I1].
- The gearboxes hold the fingers where they stop. The tool-free release (a pull-out plate on the anchor block, FXH-DDR-003) must free all tendons in 10 s or less; this is a design intent that cannot be checked until TRL 4.
- **R9 is not verifiable at TRL 3,** although the stop time is met by calculation.

## J. Cost (R12)

- Value-engineering target: USD 500 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 303.90 (USD 196.10 under the target) [J1]. The BOM has 25 lines, all priced; FXH-DDR-003 added the tray (line 23), a fixing kit (line 24) and a 5 V regulator (line 25) and repriced lines 2, 15 and 19. Only the gearmotor price was checked with the supplier; the rest are indicative.
- **R12: under the value-engineering target by USD 196.10.** No custom PCB is needed: the controller and drivers are carrier modules.

## K. Session log (R13)

- A 32-byte summary per session (start time, duration, cycle count, peak current per motor, limit settings) at three sessions a day fills 1 MB of flash in about 10,417 days, far longer than any study [K1].
- Locking the therapist limits against the user buttons is a firmware design point, beyond the scope of this note.
- **R13 is not verifiable at TRL 3.**

## Results

Table 5. Requirement status at TRL 3, not met first.

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R7 | Mass | Hand 117 g; pack 723 g | Hand 120 g or less; pack 450 g or less | **Not met** |
| R2 | Extend against mild flexor tone | 30 N delivered, 18 N needed at MAS 1+; 0.492 N·m peak (125 % of continuous rating), 0.269 N·m RMS | 30 N per finger (MAS 1 to 1+) | At risk |
| R3 | Limit force on the hand | 0.57 A pair trip; balance pulleys hold each finger to 40 N; friction spread 27 to 47 N | 40 N per finger (software); 60 N breakaway | At risk |
| R1 | Finger range | 24.8 mm needed; 29.8 mm stroke | MCP 70°, PIP 90° | Met |
| R4 | Repetition dose | 445 cycles per hour at full speed; 360 at 4 s strokes | 300 or more | Met |
| R5 | Slow, smooth, adjustable stroke | Fastest 3.3 s at design load (3.9 s pessimistic) | 4 to 15 s at design load | Met |
| R6 | Sessions per charge | 3.8 (3.80 Wh each) | 3 or more | Met |
| R10 | Fit adult hands | S, M, L sizes at 0.95, 1.00 and 1.15 scale | Hand length 170 to 205 mm | Met |
| R11 | Cuff contact pressure | 23 to 40 kPa (medium hand); 46 kPa worst (small hand, little finger) | 50 kPa or less | Met on paper |
| R12 | Parts cost | USD 303.90 | Value-engineering target USD 500 | Under the target by USD 196.10 |
| R8 | Donning and removal | Not calculable | 5 min on, 1 min off | Not verifiable at TRL 3 |
| R9 | Stop and release | Power cut in about 11 ms; release by design | 100 ms; 10 s release at a pull force agreed with the therapist | Not verifiable at TRL 3 |
| R13 | Session log | About 10,417 days of summaries in 1 MB | Time, cycles, peak current; locked limits | Not verifiable at TRL 3 |

## Changes to earlier estimates

Table 6. Changes from v0.2 to v0.3 (FXH-DDR-003, constructable design).

| Quantity | v0.2 | v0.3 | Cause |
| --- | --- | --- | --- |
| Forearm pack mass | 639 g | 723 g | Bulkhead, cradle, tray, longer anchor block, release plate, fixings counted from the model |
| Hand-side mass | 115 g | 117 g | Sheath stop blocks on the plates; saddle cuffs |
| Balance pulley free travel | 32 mm | 30 mm | Couplings and springs now share the channel |
| Parts cost | USD 289.90 | USD 303.90 | BOM lines 23 to 25 added, 2, 15 and 19 repriced |

Forces, speeds, energy and pressures are unchanged: the spool radius, motors, cells, transmission and cuff contact areas are as in v0.2.

Table 7. Changes from v0.1 to v0.2 (FXH-DDR-002).

| Quantity | v0.1 | v0.2 | Cause |
| --- | --- | --- | --- |
| Transmission efficiency | 0.694 | 0.659 | Balance pulley (N3) |
| Peak spool torque | 0.467 N·m (119 %) | 0.492 N·m (125 %) | Balance pulley |
| Cycles per hour, full speed | 448 | 445 | Balance pulley |
| Sessions per charge | 3.9 | 3.8 | Balance pulley |
| Worst single-finger force at the trip | 80 N | 40 N | Balance pulley |
| Forearm pack mass | 675 g | 639 g | Ball-detent couplings, perforated cuff (N4); longer anchor block |
| Hand-side mass | 103 g | 115 g | Thimbles (N2) |
| Worst cuff pressure | 84 kPa (96 kPa small hand) | 40 kPa (46 kPa small hand) | Thimbles (N2) |
| Parts cost | USD 281.90 | USD 289.90 | BOM lines 21 and 22 |
| R2, R5 targets | Moderate tone; 3 to 15 s | Mild tone; 4 to 15 s at design load | N1, N5 |

Earlier, from TRL 2 to v0.1: peak torque rose from 0.41 N·m (idler loss and line radius added), pack mass from about 510 g (datasheet motor mass, magnets, housing), and the gearmotors were turned to lie along the forearm with idlers, giving a 160 by 76 mm pack.
