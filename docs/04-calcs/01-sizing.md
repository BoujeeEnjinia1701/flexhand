---
doc_id: FXH-CAL-001
title: FlexHand sizing calculations
project: FlexHand
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (excursion, design load, torque, speed, force limit, energy, mass, cuff pressure, stop, cost)
---

# FlexHand sizing calculations

On paper, FlexHand meets five of its thirteen requirements, has three at risk, misses two and has three that cannot be verified at TRL 3. The two misses are the forearm pack mass, about 675 g against 450 g (R7), and cuff contact pressure, up to 84 kPa on the little finger against 50 kPa (R11). The three at risk are the force requirement (R2), where the gearbox runs 19 % above its recommended continuous load at the peak and the 30 N design load covers only mild flexor tone; the force limit (R3), because motor current measures a finger pair rather than a single finger; and the stroke-time range (R5), where the fastest stroke at design load is 3.3 s against 3 s. Energy is better than the TRL 2 estimate: about 3.9 sessions per charge. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [C2], is the line of that script's output that carries it.

> **Safety:** FlexHand is a research and educational prototype, not a medical device. These are first-principles estimates for a paper proof of concept. They do not show that the device is safe to wear. R3, R9 and R11 are safety requirements; R11 is not met and R3 is at risk, so nothing may be worn on the strength of this note. See FXH-PRC-001, Safety.

## Scope and method

The note checks every requirement in FXH-REQ-001 v0.3 against the design in FXH-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model, so the pack, spool, cuff and sheath dimensions used here are the ones in the STEP files and in drawing FXH-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is one 60 min seated session on a medium adult hand (model hand length about 179 mm), with the forearm resting on a support and the wrist near neutral. Each motor drives one finger pair (D2): motor 1 the index and middle fingers, motor 2 the ring and little fingers.

## Assumptions

Table 1. Main assumptions.

| Area | Assumption | Basis |
| --- | --- | --- |
| Joint range | MCP 0 to 70°, PIP 0 to 90° (R1); DIP not driven | FXH-REQ-001 |
| Moment arms | Extensor 10 mm at the MCP and 8 mm at the PIP; flexor 11 mm and 8 mm | Engineering estimate with cuffs and liner; to measure on a finger model |
| Tendon force | Extension rises linearly from 3 N to 30 N per finger over the stroke (joint stiffness is close to linear with angle); flexion 5 N per finger | D5 design load; stiffness data below |
| Finger stiffness | MCP 0.089 and PIP 0.092 N·m/rad for a MAS 1+ subject; 0.631 and 0.753 N·m/rad for a MAS 3 subject | [Heung et al., *Frontiers in Bioengineering and Biotechnology*, 2020](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2020.00111/full); small sample |
| Transmission | Capstan friction in the sheath, μ = 0.10 over 180° total bend; one idler at 95 %. Pessimistic case μ = 0.15 over 270° (flexed wrist) | Handbook range for UHMWPE on PTFE |
| Spool | 10 mm core, 0.8 mm line, first-layer effective radius 5.4 mm | Model |
| Gearmotor | Pololu 4869, 227:1, 12 V: 35 rpm and 0.10 A no load, 1.8 A and 2.35 N·m (24 kg·cm) stall, 0.39 N·m recommended continuous and 0.78 N·m intermittent, 107 g; linear DC model | [Pololu 4869 specifications](https://www.pololu.com/product/4869/specs), checked 2026-09-25 |
| Supply | 7.2 V at the motor under load (2S pack less driver drop); two 2,500 mAh 18650 cells, 18 Wh, 80 % usable | D8 |
| Controller | 0.40 W continuous for ESP32-S3, idle drivers, LED and regulator | Estimate |
| Cycle | Full-voltage strokes (fastest setting), 1 s dwell at each end; full torque held with motor current during the extended dwell | Conservative: the gearbox may hold without current |
| Cuff contact | Mean pressure = design tendon force / (cuff width x contact arc); contact arc 62 % of finger circumference; 3 mm clearance from each joint crease; phalanx shares 47, 28 and 25 % of finger length | Contact-area method named in R11; phalanx shares are typical adult values, to confirm with anthropometric data |
| Materials | PETG 1.27, TPU 1.21, PA12 1.01, EVA foam 0.07 g/cm³; printed parts solid except the anchor block (40 % fill) | Typical |

## A. Tendon excursion (R1)

- The extensor tendon must travel 24.8 mm to take the MCP through 70° and the PIP through 90°; the flexor travels 26.0 mm, a mismatch of 1.2 mm that the slack spring on each tendon takes up [A1].
- With 5 mm allowed for cuff and liner compliance, the stroke is 29.8 mm, or 0.88 turns of the spool. One layer of line in each groove holds about 95 mm, so the line never stacks [A2].
- **R1 is met.**

## B. Design load against published stiffness (basis of R2)

Heung and colleagues measured finger joint stiffness in people after stroke. To hold a finger straight from full flexion, a single extensor tendon crossing both joints must supply the larger of the MCP and PIP moments divided by their moment arms.

- A finger with MAS 1+ tone needs about 18.1 N; a finger with MAS 3 tone needs about 147.9 N [B1].
- The 30 N design load therefore covers PIP stiffness up to 0.153 N·m/rad, about 1.7 times the MAS 1+ value [B2].
- **Consequence:** 30 N suits mild flexor tone (MAS 1 to 1+), not the "moderate" tone in the R2 wording. Moderate to severe tone needs roughly 80 to 150 N per finger, which this drive cannot supply within the gearbox rating. FXH-DDR-001 item N1 proposes rewording R2.

## C. Transmission and torque (R2)

- Transmission efficiency is 0.694 at neutral wrist and 0.469 in the pessimistic case [C1].
- At 30 N per finger, the spool line carries 86.5 N, which at 5.4 mm is a peak torque of 0.467 N·m: 119 % of the gearbox's recommended continuous load and 60 % of its intermittent limit. The pessimistic case gives 0.692 N·m, still inside the intermittent limit [C2]. The TRL 2 estimate of 0.41 N·m left out the idler and the line radius.
- At 7.2 V the linear motor model gives R = 6.67 Ω, kt = 1.384 N·m/A and a stall torque of 1.36 N·m; the peak is 34 % of stall [C3].
- The peak lasts only at the end of the extension stroke and during the dwell. The RMS torque over a full cycle is 0.255 N·m, 65 % of the continuous rating [C4].
- **R2 is at risk:** the drive delivers the 30 N target, but the peak exceeds the continuous gearbox rating, and the target covers mild tone only (section B).

## D. Speed, cycle and dose (R4, R5)

- At 7.2 V with no load the spool turns at 20.2 rpm and the tendon moves at 11.4 mm/s, so an unloaded stroke takes 2.61 s [D1].
- At design load the fastest extension takes 3.26 s (3.76 s in the pessimistic case) and flexion 2.77 s. With 1 s dwell at each end, a cycle takes 8.03 s [D2].
- That is 7.47 cycles per minute, or 448 per hour. R4 (300 per hour) still holds with strokes as slow as 5.0 s [D3].
- At the fastest extension the MCP moves at 21.5 °/s and the PIP at 27.6 °/s, inside the 30 °/s limit in the safety section [D4].
- **R4 is met.** **R5 is at risk:** strokes from 3.3 to 15 s are available at design load, but the 3 s end of the range is reached only at lighter loads. FXH-DDR-001 item N5 proposes a 4 s lower limit at design load.

## E. Force limit (R3)

- A 40 N per finger limit on a pair corresponds to 0.623 N·m at the spool and a trip current of 0.550 A. The peak design current is 0.437 A, so the limit sits about 26 % above normal running [E1].
- Motor current measures the pair. If one finger is slack, the other can carry up to 80 N before the pair limit trips; the 60 N breakaway coupling acts first [E2].
- Sheath friction varies with wrist posture and wear. A current limit set for 40 N means 27 to 47 N at the fingers across friction coefficients of 0.15 to 0.05 [E3].
- **R3 is at risk:** the per-finger software limit cannot be enforced from pair current alone, and friction spreads the force estimate from about 32 % below to 18 % above the set value. The breakaway force cannot be verified until TRL 4. FXH-DDR-001 item N3 proposes a balance pulley so both fingers of a pair carry equal tension.

## F. Energy (R6)

- Per motor and cycle: 6.93 J for extension, 3.11 J for flexion and 3.15 J to hold the fingers extended for 1 s at 0.44 A [F1].
- Per 60 min session at 448 cycles: motors 3.29 Wh, of which 0.46 Wh reaches the spool shafts and 0.32 Wh the finger joints; controller 0.40 Wh; total 3.69 Wh, an average of 3.69 W and 0.51 A [F2].
- The 18 Wh pack gives 14.4 Wh usable, or 3.9 sessions per charge [F3]. The gearmotor runs far from its efficiency peak at this voltage and load, so most of the energy is lost in the motor and gearbox (Figure 2 of FXH-PRC-001).
- **R6 is met,** with a margin of about 30 %. The TRL 2 estimate of 3.1 sessions assumed a higher motor power.

## G. Mass (R7)

Table 2. Forearm pack mass [G1], [G2].

| Part | Mass |
| --- | --- |
| Forearm cuff: PETG shell 76.2 g, EVA liner 5.9 g, two straps 16.0 g | 98.1 g |
| Pack base 79.4 g, lid 30.2 g (PETG) | 109.6 g |
| Gearmotors (2) | 214.0 g |
| Spools 4.0 g, idler bearings 6.0 g | 10.0 g |
| Cells (2) and BMS | 95.0 g |
| Controller, drivers and charger | 13.0 g |
| Emergency stop | 20.0 g |
| Anchor block with 8 magnetic couplings and 8 slack springs | 76.3 g |
| Wiring and fasteners | 25.0 g |
| Half of the sheaths (0.83 m in total, 29 g) | 14.4 g |
| **Forearm pack** | **675 g (1.49 lb)** |

Table 3. Hand-side mass [G3], [G4].

| Part | Mass |
| --- | --- |
| Base glove (bought) | 40.0 g |
| Dorsal and palmar plates (TPU) | 15.2 g |
| Finger cuffs (8, TPU) and liners | 25.2 + 2.7 g |
| Thumb spacer, tendons | 4.2 + 1.4 g |
| Half of the sheaths | 14.4 g |
| **Hand side** | **103 g** |

- **R7 is not met:** the hand side (103 g) is within 120 g, but the forearm pack is about 675 g against 450 g. The TRL 2 estimate of 510 g used a lighter motor mass (95 g against the datasheet 107 g), left out the magnets of the breakaway couplings (56 g) and underestimated the printed housing and cuff.
- The gearmotors alone are 214 g. Lighter breakaways, a perforated cuff shell and a thinner saddle could remove about 80 to 100 g, which is still well over 450 g. D1 already calls for the 450 g target to be revisited with a therapist; FXH-DDR-001 item N4 lists the options.

## H. Cuff contact pressure (R11) and fit (R10)

- The TRL 2 basis, 30 N over a 12 mm by 25 mm patch, gave 100 kPa [H1].
- D4 called for 20 mm anchor cuffs checked for PIP clearance. The middle phalanges of the medium hand are 18.2 to 24.6 mm long. With 3 mm clearance to each joint crease, the widest cuff that fits is 16.4 mm (index), 18.6 mm (middle), 17.0 mm (ring) and 12.2 mm (little); a 20 mm cuff fits on none of them [H2].

Table 4. Anchor cuff pressure at 30 N, medium hand [H2].

| Finger | Middle phalanx | Cuff width | Contact arc | Pressure | Width for 50 kPa |
| --- | --- | --- | --- | --- | --- |
| Index | 22.4 mm | 16.4 mm | 35.1 mm | 52 kPa | 17.1 mm |
| Middle | 24.6 mm | 18.6 mm | 35.1 mm | 46 kPa | 17.1 mm |
| Ring | 23.0 mm | 17.0 mm | 33.1 mm | 53 kPa | 18.1 mm |
| Little | 18.2 mm | 12.2 mm | 29.2 mm | 84 kPa | 20.5 mm |

- On a small hand the little finger reaches 96 kPa; on a large hand 60 kPa [H3].
- A fingertip thimble that shares the extensor load with the middle-phalanx cuff would give 26, 23, 26 and 40 kPa [H4]. This is FXH-DDR-001 item N2 and is not modeled.
- **R11 is not met:** only the middle finger is under 50 kPa. The mean-pressure metric also ignores skin shear and edge pressure, so even a met value would need a bench check at TRL 4.
- **R10 is met on paper:** three glove sizes scaled at 0.95, 1.00 and 1.15 from the model cover hand lengths of 170 to 205 mm, with cuff widths set per size [H3]. A fit trial is still needed.

## I. Stop and release (R9)

- The stop switch opens the motor supply. The 100 µF bulk capacitance keeps the motors turning for about 0.8 ms, contact opening takes up to about 5 ms and the rotor runs down in about 5 ms, so motion stops in about 11 ms against 100 ms [I1].
- The gearboxes hold the fingers where they stop. The tool-free release lever must free all tendons in 10 s or less; this is a design intent that cannot be checked until TRL 4.
- **R9 is not verifiable at TRL 3,** although the stop time is met by calculation.

## J. Cost (R12)

- The BOM has 20 lines, all priced, for $281.90 against the $500 budget (56 %) [J1]. Only the gearmotor price was checked with the supplier; the rest are indicative.
- **R12 is met.** No custom PCB is needed: the controller and drivers are carrier modules.

## K. Session log (R13)

- A 32-byte summary per session (start time, duration, cycle count, peak current per motor, limit settings) at three sessions a day fills 1 MB of flash in about 10,417 days, far longer than any study [K1].
- Locking the therapist limits against the user buttons is a firmware design point, beyond the scope of this note.
- **R13 is not verifiable at TRL 3.**

## Results

Table 5. Requirement status at TRL 3, not met first.

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R7 | Mass | Hand 103 g; pack 675 g | Hand 120 g or less; pack 450 g or less | **Not met** |
| R11 | Cuff contact pressure | 84 kPa worst (little finger); index 52, middle 46, ring 53 kPa | 50 kPa or less | **Not met** |
| R2 | Extend against flexor tone | 30 N delivered; 0.467 N·m peak (119 % of continuous rating), 0.255 N·m RMS; covers MAS 1+ only | 30 N per finger | At risk |
| R3 | Limit force on the hand | 0.55 A pair trip; one finger may reach 80 N before it trips; friction spread -32 to +18 % | 40 N per finger (software); 60 N breakaway | At risk |
| R5 | Slow, smooth, adjustable stroke | 3.3 to 15 s at design load; 2.6 s unloaded | 3 to 15 s | At risk |
| R1 | Finger range | 24.8 mm needed; 29.8 mm stroke | MCP 70°, PIP 90° | Met |
| R4 | Repetition dose | 448 cycles per hour | 300 or more | Met |
| R6 | Sessions per charge | 3.9 (3.69 Wh each) | 3 or more | Met |
| R10 | Fit adult hands | S, M, L sizes at 0.95, 1.00 and 1.15 scale | Hand length 170 to 205 mm | Met |
| R12 | Parts cost | $281.90 | $500 or less | Met |
| R8 | Donning and removal | Not calculable | 5 min on, 1 min off | Not verifiable at TRL 3 |
| R9 | Stop and release | Power cut in about 11 ms; release by design | 100 ms; 10 s release | Not verifiable at TRL 3 |
| R13 | Session log | About 10,417 days of summaries in 1 MB | Time, cycles, peak current; locked limits | Not verifiable at TRL 3 |

## Changes to earlier estimates

- Peak spool torque rose from 0.41 to 0.467 N·m (idler loss and line radius added).
- Cycle rate rose from about 385 to 448 per hour, and sessions per charge from about 3.1 to 3.9, because the linear motor model at the lighter average load gives more speed and less power than the TRL 2 estimate.
- Pack mass rose from about 510 to 675 g (datasheet motor mass, breakaway magnets, printed housing and cuff).
- Cuff pressure fell from 100 kPa to 46 to 84 kPa with the widest cuffs that fit, but R11 is still not met.
- The TRL 3 layout turns the gearmotors to lie along the forearm with the spools at the front and idlers turning the tendons forward. The 71 mm gearmotor with a spool did not fit across a pack narrow enough for the forearm; the new pack is 160 by 76 mm.
