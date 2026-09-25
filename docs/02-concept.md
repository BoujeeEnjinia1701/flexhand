---
doc_id: FXH-PRC-001
title: FlexHand design precis
project: FlexHand
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update; decisions of FXH-DDR-001 recorded, motors turned along the forearm with idlers, numbers from FXH-CAL-001, parametric model and drawing FXH-DWG-001
---

# FlexHand design precis

FlexHand is a fingerless glove with tendon cuffs on the four fingers, driven through Bowden sheaths by two gearmotors in a pack strapped to the forearm. Each motor turns a two-groove spool that pulls a flexor tendon while paying out the matching extensor tendon, so one motor moves a pair of fingers both ways. The TRL 3 calculations (FXH-CAL-001) give about 448 finger cycles per hour at the design load, about 3.9 sessions of 60 min per charge and $281.90 in parts. The design misses two requirements: the forearm pack is about 675 g against 450 g (R7), and cuff contact pressure reaches 84 kPa on the little finger against 50 kPa (R11). The force requirement, the force limit and the stroke-time range are at risk (R2, R3, R5).

![Hero render](../media/hero.png)

*Figure 1. FlexHand on a left forearm and hand, palm down. Device parts are colored; the grey forearm and hand are for scale.*

## How it works

1. **Set up.** A therapist sets range-of-motion end points, stroke time, dwell and force limit for each finger pair. The limits are stored on the controller and cannot be changed from the user's buttons.
2. **Don.** A care partner slides on the fingerless glove, closes the finger cuffs over the proximal and middle phalanges, clips the thumb spacer and straps the pack to the forearm. The tendons clip into the anchor block at the front of the pack.
3. **Cycle.** On start, each gearmotor turns its spool one way to pull the palmar (flexor) tendons and close the fingers, pauses, then turns back to pull the dorsal (extensor) tendons and open them. The encoder tracks position against the set end points.
4. **Limit.** The motor drivers report current, which is roughly proportional to the combined tendon force of a finger pair. If force passes the limit, the motor stops and backs off. A magnetic breakaway coupling on each tendon separates if force exceeds about 60 N.
5. **Stop.** A red latching stop button on the pack lid cuts motor power. A quick-release lever on the anchor block frees all tendons by hand, because the high-ratio gearboxes hold their position when unpowered.
6. **Log.** The controller records session time, cycle count and peak current for the therapist.

![Energy flow](../media/flow.png)

*Figure 2. Energy flow for one 60 min session at the design load, in Wh, from FXH-CAL-001. All values are estimates.*

## Main components

Numbers match the exploded view (Figure 3), drawing FXH-DWG-001 and `bom/bom.csv`.

Table 1. Main components.

| # | Component | Choice | Notes |
| --- | --- | --- | --- |
| 1 | Forearm cuff | 3D-printed PETG half shell, 2 mm, with 4 mm EVA foam liner and two 38 mm hook-and-loop straps | Spreads the pack load over the dorsal forearm |
| 2 | Pack base | 3D-printed PETG, 160 x 76 mm, 2 mm walls, three saddle ribs | Saddles onto the cuff |
| 3 | Gearmotors (2) | 25D x 71L mm, 227:1, 12 V rated, 48 CPR encoder (Pololu 4869), run at 7.2 V | Axes along the forearm at 15 mm each side of center (D1) |
| 4 | Spools (2) | Two-groove spool, 10 mm core, 20 mm flanges, 12 mm wide | Flexor wound one way, extensor the other |
| 5 | Li-ion pack | Two 2,500 mAh 18650 cells across the rear of the pack, with 2S protection board | 18 Wh (D8) |
| 6 | Controller | ESP32-S3 module (Seeed XIAO ESP32S3 class) | Limits, logging, optional Bluetooth for the therapist view |
| 7 | Motor drivers (2) | DRV8874 H-bridge with current-sense output | Force limit through motor current |
| 8 | Pack lid | 3D-printed PETG, 2 mm, with stop button opening and LED window | |
| 9 | Emergency stop | 16 mm latching mushroom switch in the motor supply, between the cells and the motors | Hardware cut, not a firmware input |
| 10 | Sheath anchor block | Printed block with sheath stops, eight magnetic breakaway couplings, slack springs and a quick-release lever | Tool-free release (R9) |
| 11 | Bowden sheaths (8) | PTFE-lined 4 mm housing, about 100 mm each | Carry tendons across the wrist so wrist posture does not change finger position much |
| 12 | Base glove | Fingerless, breathable, three sizes | Carries the plates; palm left mostly open |
| 13 | Dorsal plate | TPU 95A, 2.5 mm, sheath stops for the four extensor lines | |
| 14 | Palmar plate | TPU 95A, 2.5 mm, sheath stops for the four flexor lines | |
| 15 | Finger cuffs (8) | TPU 95A with 2 mm padded liner: 12 mm guide cuffs on the proximal phalanges, anchor cuffs 12.2 to 18.6 mm wide on the middle phalanges | Anchor cuffs are as wide as the phalanx allows (D4); R11 not met |
| 16 | Tendons (8) | 0.8 mm braided UHMWPE line | One flexor and one extensor per finger |
| 17 | Thumb spacer | TPU ring and web block | Holds the thumb abducted, out of the fingers' path (D6) |
| 18 | USB-C charger | 2S charger module in the rear of the pack | Charge only when not worn |
| 19 | Wiring and consumables | Wire, connectors, fasteners | Not modeled |
| 20 | Idler bearings (4) | 623ZZ class, 10 mm, axis vertical | Turn each tendon pair from the spool toward the anchor block |

Motor 1 drives the index and middle fingers and its sheaths run on the thumb (radial) side; motor 2 drives the ring and little fingers on the ulnar side.

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with callouts matching `bom/bom.csv`. Line 19 of the BOM (wiring and consumables) is not modeled.*

![Cutaway](../media/cutaway.png)

*Figure 4. Section through the motor pack on its centerline, seen from the side: cells with the electronics tray above them at the rear (left), the emergency stop, one gearmotor with its spool and idlers, and the anchor block at the front (right).*

## TRL 3 numbers

All values are estimates from FXH-CAL-001; the tags in brackets are the script's output lines.

Table 2. Key numbers.

| Quantity | Value | Requirement |
| --- | --- | --- |
| Tendon excursion needed, stroke | 24.8 mm, 29.8 mm [A1], [A2] | R1 met |
| Design load | 30 N per finger; covers MAS 1+ tone, MAS 3 needs about 148 N [B1] | R2 at risk |
| Transmission efficiency | 0.694 (0.469 pessimistic) [C1] | |
| Peak spool torque | 0.467 N·m, 119 % of the gearbox's continuous rating, 60 % of intermittent; RMS 0.255 N·m [C2], [C4] | R2 at risk |
| Force limit | 0.55 A trip for 40 N per finger, sensed per finger pair [E1], [E2] | R3 at risk |
| Stroke and cycle | Extension 3.26 s, flexion 2.77 s, cycle 8.03 s [D2] | R5 at risk |
| Repetitions | 448 per hour [D3] | R4 met |
| Energy per session | 3.69 Wh; 3.9 sessions per 18 Wh charge [F2], [F3] | R6 met |
| Mass on the hand | 103 g [G4] | R7 hand part met |
| Mass of forearm pack | 675 g [G2] | **R7 not met** |
| Cuff contact pressure | 46 to 84 kPa [H2] | **R11 not met** |
| Stop time | About 11 ms [I1] | R9 not verifiable at TRL 3 |
| Parts cost | $281.90 [J1] | R12 met |

## Key design choices

Amish decided D1 to D8 on 2026-09-25 (FXH-DDR-001) by accepting the TRL 2 recommendations.

- **Tendons and Bowden sheaths rather than pneumatic soft actuators (D7).** Tendons need no pump or valves, run from a small battery and keep the hand light. The Columbia orthosis and Exo-Glove Poly show that tendon drives work for this task.
- **Two motors, one per finger pair, each with an antagonistic spool (D2).** One motor per pair moves the fingers both ways. Flexor and extensor excursions differ by about 1.2 mm, which a slack spring on each tendon in the anchor block takes up.
- **25 mm gearmotors on the forearm (D1).** The micro (N20) route could not carry the torque, and a bench-top unit departs from the wrist-mounted pitch. The 25 mm motors are the main cause of the R7 overrun, and the 450 g target is to be revisited with a therapist.
- **Motors along the forearm (TRL 3 layout).** At TRL 2 the motors lay across the forearm, but a 71 mm gearmotor with its spool needs about 84 mm, which forced a pack wider than the forearm. Turning the motors to lie along the forearm, with the spools at the front and a small idler turning each tendon pair forward, gives a 76 mm wide pack. The idlers cost about 5 % in efficiency.
- **Passive motion only (D3).** An active-assist mode triggered by the user's own effort is recorded as a later option; it is not part of this design.
- **Anchor cuffs as wide as the phalanx allows (D4).** The 20 mm cuff recommended at TRL 2 does not fit on any middle phalanx with clearance for PIP flexion. See the open questions.
- **Thumb passive (D6).** A spacer holds the thumb abducted.
- **Force limiting in three layers.** Firmware current limit, a mechanical breakaway coupling on each tendon, and a hardware stop switch with a manual tendon release.
- **2S Li-ion pack (D8).** Enough for about 3.9 sessions and charged by USB-C. The portfolio's 48 V SwapCell pack is far larger than needed and is not used.

## Safety

> **Safety:** FlexHand is a research and educational prototype. It is not a medical device, has not been cleared or approved by any regulator, and must not be used to diagnose or treat any person. Any use on a person needs a supervising therapist, informed consent and, in a research setting, ethics review.

- **Joint injury.** Forcing a spastic or contracted finger can injure joints, tendons or skin. Range limits and force limits are set by a therapist, start low, and are enforced in firmware with a mechanical breakaway as backup. Movement is slow (30 °/s or less; about 28 °/s at the PIP at the fastest setting) to avoid provoking a stretch reflex. The current limit acts on a finger pair, so one finger can carry more than its share until the breakaway separates (R3 at risk).
- **Reduced sensation.** Many users cannot feel pressure or pain in the affected hand. Check the skin under every cuff before and after each session, and stop at any redness that does not fade within 30 min. R11 is not met, so this design must not be worn until cuff pressure is reduced.
- **Entrapment.** The gearboxes hold their position when unpowered. If power fails with the fingers flexed, the hand stays closed until the tendons are released. The quick-release lever and a care partner within reach are required.
- **Pinch points and moving parts.** Spools, idlers and tendons are inside the pack; keep the lid closed while powered. Keep hair and loose clothing away from the tendon path.
- **Lithium-ion cells.** Use a protected 2S pack, charge only when not worn, on a non-combustible surface, and stop using a pack that is swollen, damaged or hot.
- **Electrical.** The pack runs at 8.4 V or less; there is no mains connection while worn.
- **Data.** Session logs are health data. Keep them on the device and the therapist's computer; share only with consent.

## Open questions

These arise from FXH-CAL-001 and are proposed, awaiting Amish (FXH-DDR-001, N1 to N5), except the first.

- First clinical co-design partner (O1). Proposed, awaiting Amish.
- Reword R2 to mild flexor tone (MAS 1 to 1+), or raise the design load toward moderate tone at the cost of mass (N1).
- Add a fingertip thimble that shares the extensor load with the middle-phalanx cuff, which would bring every finger under 50 kPa (N2).
- Add a balance pulley so both tendons of a pair carry equal tension and the current limit acts per finger (N3).
- Reduce pack mass: lighter breakaways, a perforated cuff shell, and a pack target agreed with a therapist (N4).
- Relax the lower stroke-time limit to 4 s at design load (N5).

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html). General arrangement: [FXH-DWG-001](../cad/drawings/FXH-DWG-001.pdf).
