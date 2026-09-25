---
doc_id: FXH-PRC-001
title: FlexHand design precis
project: FlexHand
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
---

# FlexHand design precis

FlexHand is a fingerless glove with tendon cuffs on the four fingers, driven through Bowden sheaths by two small gearmotors in a pack strapped to the forearm. Each motor turns a two-groove spool that pulls a flexor tendon while paying out the matching extensor tendon, so one motor moves a pair of fingers both ways. First-order numbers suggest about 385 full finger cycles per hour at the design load, about three 60 min sessions per charge and about $280 in parts. The concept misses two requirements: the forearm pack is about 510 g against 450 g (R7), and cuff contact pressure is about 100 kPa against 50 kPa (R11).

![Hero render](../media/hero.png)

*Figure 1. FlexHand on a left forearm and hand, palm down. Device parts are colored; the grey forearm and hand are for scale.*

## How it works

1. **Set up.** A therapist sets range-of-motion end points, stroke time, dwell and force limit for each finger pair. The limits are stored on the controller and cannot be changed from the user's buttons.
2. **Don.** A care partner slides on the fingerless glove, closes the finger cuffs over the proximal and middle phalanges, clips the thumb spacer and straps the pack to the forearm. The tendons clip into the anchor block at the front of the pack.
3. **Cycle.** On start, each gearmotor turns its spool one way to pull the palmar (flexor) tendons and close the fingers, pauses, then turns back to pull the dorsal (extensor) tendons and open them. The encoder tracks position against the set end points.
4. **Limit.** The motor drivers report current, which is roughly proportional to tendon force. If force passes the limit, the motor stops and backs off. A magnetic breakaway coupling on each tendon separates if force exceeds about 60 N.
5. **Stop.** A red latching stop button on the pack cuts motor power. A quick-release lever on the anchor block frees all tendons by hand, because the high-ratio gearboxes cannot be back-driven.
6. **Log.** The controller records session time, cycle count and peak current for the therapist.

![Energy flow](../media/flow.png)

*Figure 2. Energy flow for one 60 min session at the design load, in Wh. All values are estimates.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

Table 1. Main components.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Forearm cuff | 3D-printed PETG half shell with foam liner and two 38 mm hook-and-loop straps | Spreads the pack load over the dorsal forearm |
| 2 | Pack base | 3D-printed PETG, about 147 x 90 x 42 mm | Saddles onto the cuff |
| 3 | Gearmotors (2) | 25 mm, 227:1 metal gearmotor, 12 V rated, with 48 CPR encoder (Pololu 4869 class), run at 7.4 V | Replaces the scaffold's micro (N20) motors; see key design choices. Proposed, awaiting Amish |
| 4 | Spools (2) | Two-groove spool, 10 mm core diameter | Flexor wound one way, extensor the other |
| 5 | Li-ion pack | 2S1P 18650, about 2,500 mAh, with 2S protection board | About 18 Wh |
| 6 | Controller | ESP32-S3 module (Seeed XIAO ESP32S3 class) | Limits, logging, optional Bluetooth for the therapist view |
| 7 | Motor drivers (2) | DRV8874 H-bridge with current-sense output | Force limit through motor current |
| 8 | Pack lid | 3D-printed PETG with status LED window | |
| 9 | Emergency stop | 16 mm latching mushroom switch in the motor supply | Hardware cut, not a firmware input |
| 10 | Sheath anchor block | Printed block with sheath stops, eight magnetic breakaway couplings, slack springs and a quick-release lever | Tool-free release (R9) |
| 11 | Bowden sheaths (8) | PTFE-lined 4 mm housing, about 350 mm | Carry tendons across the wrist so wrist posture does not change finger position much |
| 12 | Base glove | Fingerless, breathable, three sizes | Carries the plates; palm left mostly open |
| 13 | Dorsal plate | TPU 95A, sheath stops for the four extensor lines | |
| 14 | Palmar plate | TPU 95A, sheath stops for the four flexor lines | |
| 15 | Finger cuffs (8) | TPU 95A rings, 12 mm wide, padded, on proximal and middle phalanges | Middle cuff anchors the tendons; proximal cuff guides them |
| 16 | Tendons (8) | 0.8 mm braided UHMWPE line | One flexor and one extensor per finger |
| 17 | Thumb spacer | TPU ring and web block | Holds the thumb abducted, out of the fingers' path |

Motor 1 drives the index and middle fingers; motor 2 drives the ring and little fingers.

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with callouts matching `bom/bom.csv`. Lines 18 and 19 of the BOM (charger, wiring and consumables) are not modeled.*

![Cutaway](../media/cutaway.png)

*Figure 4. Section through the motor pack, seen from the little-finger side: cells with the controller and drivers above them (left) and the two gearmotors (right).*

## First-order numbers

All values are estimates for concept review and will be checked by calculation at TRL 3.

Table 2. First-order numbers.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Tendon force at the finger, design load | 30 N per finger, 60 N per spool | Assumption, see FXH-REQ-001 | R2 |
| Bowden efficiency | about 73 % | Capstan, μ = 0.1, 180° total bend | |
| Tendon force at the spool | about 82 N | 60 N / 0.73 | |
| Spool torque | about 0.41 N·m | 82 N at 5 mm radius | R2 met on stall margin (about 28 % of stall at 7.4 V); about 5 % above the gearbox's recommended 0.39 N·m continuous load, within its 0.78 N·m intermittent limit ([Pololu 4869](https://www.pololu.com/product/4869)) |
| Motor speed under load | about 15.5 rpm | 35 rpm and 2.35 N·m stall at 12 V, scaled to 7.4 V, linear speed and torque line | |
| Extension stroke | about 4.3 s | 35 mm excursion at about 8 mm/s | R5 met |
| Cycle time | about 9.3 s | 4.3 s extend, about 3 s flex at lower load, 1 s dwell at each end | |
| Repetitions | about 6.4 per min, about 385 per hour | | R4 met |
| Average electrical power | about 4.7 W | Two motors at about 2.7 W each while moving, 80 % duty, 0.4 W controller and drivers | |
| Sessions per charge | about 3.1 | 18 Wh pack, 80 % usable, 4.7 Wh per session | R6 met, no margin |
| Mass on the hand | about 90 g | Glove 40 g, plates 16 g, cuffs 16 g, spacer 6 g, tendons and sheath ends 12 g | R7 hand part met |
| Mass of forearm pack | about 510 g | Motors about 190 g, cells and protection 105 g, housing 75 g, cuff and straps 60 g, anchor block 25 g, wiring and charger 20 g, other 35 g | **R7 pack part not met** |
| Cuff contact pressure | about 100 kPa | 30 N over a 12 mm x 25 mm contact patch | **R11 not met**; 20 mm wide cuffs with a 35 mm arc give about 43 kPa |
| Parts cost | about $280 | Indicative prices, see `bom/bom.csv` | R12 met |

## Key design choices

All of these are proposed, awaiting Amish.

- **Tendons and Bowden sheaths rather than pneumatic soft actuators.** Tendons need no pump or valves, run from a small battery and keep the hand light. Pneumatic gloves are softer on the skin but need a compressor. The Columbia orthosis and Exo-Glove Poly show that tendon drives work for this task.
- **Two motors, one per finger pair, each with an antagonistic spool.** One motor per pair moves the fingers both ways, which halves the motor count against separate flexor and extensor motors. Options: one motor for all four fingers (lighter, cheaper, no per-finger tuning), two motors (proposed), or four motors (per-finger limits, about 200 g heavier and about $130 more). Flexor and extensor excursions are not equal, so a slack spring in the anchor block takes up the difference.
- **25 mm gearmotors rather than micro (N20) gearmotors.** The scaffold listed micro gearmotors. The 1000:1 micro metal gearmotor has about 1 N·m stall torque at 12 V, but its maker advises keeping load well under about 0.25 N·m ([Pololu 5228](https://www.pololu.com/product/5228)), below the 0.41 N·m this concept needs. The 25 mm class meets the torque but causes the pack mass overrun (R7). Options: (a) 25 mm motors and accept a heavier pack, (b) micro motors with a lower 20 N force target, (c) a bench-top motor unit with longer sheaths. Recommendation: (a) for the first build, with the pack mass target revisited with a therapist.
- **Motors on the forearm, not the hand.** Keeps the hand side under 100 g. The pitch calls for a wrist-mounted pack; the pack sits on the forearm just behind the wrist.
- **Thumb passive.** A spacer holds the thumb abducted. Thumb actuation roughly doubles complexity and is out of scope for this concept.
- **Force limiting in three layers.** Firmware current limit, a mechanical breakaway coupling on each tendon, and a hardware stop switch with a manual tendon release.
- **2S Li-ion pack.** Enough for about three sessions and charged by USB-C. The portfolio's 48 V SwapCell pack is far larger than needed and is not used.

## Safety

> **Safety:** FlexHand is a research and educational prototype. It is not a medical device, has not been cleared or approved by any regulator, and must not be used to diagnose or treat any person. Any use on a person needs a supervising therapist, informed consent and, in a research setting, ethics review.

- **Joint injury.** Forcing a spastic or contracted finger can injure joints, tendons or skin. Range limits and force limits are set by a therapist, start low, and are enforced in firmware with a mechanical breakaway as backup. Movement is slow (30 °/s or less) to avoid provoking a stretch reflex.
- **Reduced sensation.** Many users cannot feel pressure or pain in the affected hand. Check the skin under every cuff before and after each session, and stop at any redness that does not fade within 30 min. R11 is not yet met, so this concept must not be worn until cuff pressure is reduced.
- **Entrapment.** The gearboxes cannot be back-driven. If power fails with the fingers flexed, the hand stays closed until the tendons are released. The quick-release lever and a care partner within reach are required.
- **Pinch points and moving parts.** Spools and tendons are inside the pack; keep the lid closed while powered. Keep hair and loose clothing away from the tendon path.
- **Lithium-ion cells.** Use a protected 2S pack, charge only when not worn, on a non-combustible surface, and stop using a pack that is swollen, damaged or hot.
- **Electrical.** The pack runs at 8.4 V or less; there is no mains connection while worn.
- **Data.** Session logs are health data. Keep them on the device and the therapist's computer; share only with consent.

## Open questions for TRL 3

- Measure or find published finger extension stiffness for moderate flexor tone to confirm the 30 N design load.
- Confirm the cuff design that meets R11 (wider cuffs, softer liners, or a distal anchor) without blocking PIP flexion.
- Decide the motor route and pack mass target (see key design choices). Proposed, awaiting Amish.
- Check that the slack spring handles the flexor and extensor excursion mismatch across the full range.
- Decide whether to plan for an active-assist mode (user effort sensed by motor current or surface EMG). This changes the pitch. Proposed, awaiting Amish.
- Identify a clinical partner for co-design of limits, donning and session length.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
