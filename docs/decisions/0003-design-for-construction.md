---
doc_id: FXH-DDR-003
title: FlexHand design for construction
project: FlexHand
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Accepted by Amish on 2026-10-02, including the recommendations for A1 to A3 with their conditions'
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations for A1 to A3 in Table 3, now decided as recommended, with the conditions below, and recorded in the design decisions register (FXH-DEC-001).

## Context

On 2026-09-30 Amish asked for every repo to get an illustrated prototype build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The concept model of FXH-DDR-002 showed what FlexHand does, and its calculations stand, but many of its parts could not be made, fitted or fixed as drawn. A build123d check of the concept model found parts that overlapped (spools and idlers, the electronics boards, the sheaths and the wrist, the finger cuffs of neighbouring fingers), parts that floated with no fixing (the pack on the cuff, the motors, the cells, the boards, the anchor block), mechanisms with no parts (the quick-release lever, the couplings, springs and stop beads in the anchor block) and one missing part (a 5 V supply for the controller).

The changes keep what FlexHand does: two gearmotors on the forearm, antagonistic spools, idlers, four floating balance pulleys, eight tendons in Bowden sheaths, eight ball-detent breakaway couplings, a hardware stop button, a tool-free release, padded cuffs and thimbles, the same motors, cells, electronics, strokes, forces, speeds and cuff contact areas. Nothing here changes the pitch. The model now runs 203 constructability checks (`python cad/src/model.py --check`): no two parts overlap, no part enters the forearm or hand, every joint touches, every clearance holds, and the release plate's path is clear. All 203 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| C1 | The pack sat on the cuff with no fixing, and at the elbow end the cuff cut 0.7 mm into the pack floor. Two of the three saddle ribs stood over cuff holes. | The pack floor is raised 4 mm. The three ribs sit on the solid strips between hole columns (18.5, 86.5 and 154.5 mm from the cuff's elbow end), each with two screw bosses 9 mm either side of the top line. Six M3 x 8 button-head screws go up through 3.4 mm holes in the shell into heat-set inserts in the bosses. The liner has a 6.5 mm hole over each screw head and is glued in after the pack is fitted. | The pack must not move on the cuff under the sheath reaction (up to about 180 N along the forearm). Screws through the shell into printed bosses are the simplest fixing that can be undone; the strips between holes leave the perforation as it was. |
| C2 | The straps were drawn inside the liner, where they overlapped it. | Each strap lies over the shell, passes through the gap under the pack between two ribs, steps off the shell edge and wraps the skin under the forearm. Straps moved to 52.5 and 120.5 mm from the cuff's elbow end. | This is how a strap holds a half shell; the ribs keep the straps from sliding. |
| C3 | The gearmotors floated 1.5 mm above the floor with no fixing. | A 3 mm bulkhead printed in the pack base carries each gearbox face on two M3 x 6 countersunk screws; a cradle rib under the motor cans with a cable tie holds their rear ends. Motor axes moved from 15 to 13.5 mm either side of the centre line. | The gearbox face is the motor's intended mounting face; the bulkhead takes the spool torque. Moving the motors inward makes room for the idlers (C4). |
| C4 | The idlers cut into the 20 mm spool flanges and had no pins or supports; the spool had no way to grip the shaft. | Spool flanges 14 mm; a 4 mm hub with an M3 set screw (spool 16 mm long). Each idler runs on a 3 mm steel pin: the lower one in a printed post on the floor, the upper one under a printed shelf from the side wall. Each spool line leaves its idler 31.25 mm from the centre line and the pack through a 3 mm hole. | A 14 mm flange still stands 1.6 mm above the single layer of 0.8 mm line; the idlers then clear the flanges by 0.75 mm. |
| C5 | The rear bay did not fit: the battery board overlapped the controller, the cells sat 1 mm above the floor, the boards floated with nothing under them, the charger's port went through a solid wall, and the stop button sat 2 mm from the motors with no room for the encoder cable. The controller (an ESP32-S3 module) had no 5 V supply: it cannot take the 7.4 to 8.4 V pack voltage. | Cells in printed saddles; a 2 mm electronics tray (BOM line 23) on four posts, screwed down, holds the cells through a foam pad; the boards are laid out on the tray without overlap; a USB-C opening in the rear wall; the cells and stop button move toward the elbow so there is a 6 mm gap behind the motors. A 5 V step-down regulator is added (BOM line 25). | Every part now has a seat and a fixing. The regulator is the missing part the circuit needs. |
| C6 | The anchor block (44 mm) could not hold what the concept puts in it. Its 40 mm channels gave the balance pulleys 32 mm of travel but left no room for the eight couplings, eight slack springs and eight stop beads; its channels sat 6 mm inboard of the tendon exits; its sheath stops were 3 mm apart for 4 mm sheaths; and it had no fixing to the pack. | The block is 53 mm long, 88 mm wide and the full pack height, with four 15 x 7 mm channels lined up with the tendon exits. Each channel holds, from the back: the spool line's slack spring, the balance pulley (30 mm of travel against a 29.8 mm stroke) and the two finger lines' couplings side by side. Four M3 x 8 screws from inside the pack hold it to the front wall. A pocket underneath saves mass. | The channel holds the hardware that moves with the line; nothing fits beside it. Moving the pack toward the elbow (C8) keeps the block's front 7 mm short of the wrist. |
| C7 | The quick-release lever had no mechanism. | The eight sheath ends sit in four pucks in a cover on the front of the block. The pucks press on a red release plate in a 3.4 mm gap between block and cover. Pulling the plate's finger loop toward the thumb side slides it out (its two slots let it pass the tendons); the pucks and sheath ends then slide back into the channels and all eight tendons go slack at once. | One pull, by hand, no tools, at one place on the pack: the release does what the concept's lever was for. The form changed from a lever to a pull loop, so it is also listed for Amish's confirmation (Table 3, A1). |
| C8 | Knock-on of C1, C3, C5 and C6. | The pack is 168 mm long (was 160); its elbow end is 24 mm and its front 16 mm further toward the elbow; the cuff (still 174 mm long) moves 20 mm toward the elbow, ending 28 mm short of the elbow. | Room for the bulkhead, the spool hub, the encoder cable and the longer block without the block reaching the wrist. |
| C9 | Slack springs (eight) and stop beads (eight) had no place. | Four slack springs, one in each spool line behind its pulley. The eight stop beads are crimped on the tendons at the hand end, between each plate's stop block and the first cuff, where they stop against the block. | The balance pulley gives both tendons of a pair the same motion, so one spring per spool line takes up the same 1.2 mm mismatch. A bead at the hand end limits its finger to its own range exactly as before and is easy to set. |
| C10 | The finger cuffs were full 4.5 mm rings on fingers drawn 1.5 mm apart, so the cuffs of neighbouring fingers overlapped each other and the fingers; the tendons had no eyelets or end fixings; the cuffs had no way to close. | Cuffs and thimbles are padded saddles top and bottom over the same 62 % contact arc, with 1 mm TPU side bands; cuffs have a slit closed by a 6 mm hook-and-loop strip; eyelets and end tabs carry the tendons. The glove holds the fingers slightly spread (finger centres 24, 24 and 22.5 mm apart, was 19.5, 19.5 and 19). | Cuff widths and contact areas are unchanged, so the pressure results (R11) stand. The spread is how the device must be worn; it is also listed for confirmation with a therapist (Table 3, A2). |
| C11 | The sheaths ended on the hand plates with no stop, and the flexor sheaths passed through the wrist; the plates had no fixing to the glove. | Each plate carries a printed stop block with four ferrule seats; plates are stitched to the glove through rows of 1.5 mm holes. Sheath routes are redrawn: extensors over the back of the wrist, flexors down the side and under the wrist, none touching the hand, the glove or another sheath. | A sheath needs a seat at both ends to work; stitching is the usual way to fix a part to a glove. |
| C12 | The thumb spacer's block sat inside the thumb and the glove; the glove overlapped the forearm and fingers. | The spacer's ring moves 6 mm along the thumb and its block sits in the web space, shaped to the thumb and stitched to the glove's side. The glove ends at the wrist crease and the knuckles and has a thumb opening. | The spacer now holds the thumb out from outside it. |
| C13 | No fixings were listed. | BOM line 24, a fixing kit: 18 heat-set inserts, 26 screws and 8 steel pins; line 19 no longer covers fasteners. | Every joint names its fixing. |
| C14 | The couplings' 4 mm ball and spring (BOM line 10) cannot fit inside a body small enough for two couplings to sit side by side in a channel. | Each coupling is 6.8 mm across: two 2 mm steel balls in holes in the socket, pressed into a groove round the plug's stem by a ring of 0.4 mm spring wire. | Keeps a ball-detent breakaway on every tendon (N4) within the channel; the wire sets the pull-out force. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Forearm pack about 723 g (was 639 g): pack base 105 g (was 79 g), anchor block parts 71 g printed (was 39 g), screws, inserts and pins 27 g (was 10 g allowed), tray 7 g, regulator 3 g. Hand side 117 g (was 115 g). R7: pack not met (further from 450 g), hand met [G2], [G4]. | Parts added for construction; the earlier fastener allowance was low. |
| Cost | Estimated cost of the constructable design USD 303.90 (was USD 289.90): lines 2, 15 and 19 repriced, lines 23 to 25 added. Value-engineering target USD 500: USD 196.10 under it [J1]. | Parts added for construction. |
| Drawing | FXH-DWG-001 Rev P3; making sketches FXH-DWG-101 to 116 added. | Follows the model. |
| Documents | FXH-CAL-001 v0.3, FXH-PRC-001 v0.5, FXH-REQ-001 v0.5: masses, cost wording, pack size and the release updated. No requirement changed status. | Follows the model. |
| Forces, speeds, energy, pressure | Unchanged: the spool radius, strokes, motors, cells, transmission and cuff contact areas are as before [A1] to [F3], [H2], [H3]. | |

*Table 3. Proposed, then accepted by Amish as recommended on 2026-10-02, with the conditions added in the recommendation column.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The tool-free release is now a pull-out plate with a finger loop, not a lever (C7). It changes the form of a safety feature, so Amish should confirm it. | (a) the pull-out plate, with its pull force and release time measured at TRL 4 against R9's 10 s; (b) a cam lever that drives the same plate out (more parts, lower pull force). | (a); move to (b) only if the measured pull force is too high for a care partner. Accepted 2026-10-02, with the pass mark set before the TRL 4 test: released in 10 s or less (R9) with a pull force that the co-design therapist agrees, before the test, a care partner can apply with one hand. |
| A2 | The cuffs need the fingers held slightly spread (C10). Spastic fingers may resist being spread. | (a) accept, and ask the co-design therapist (O1) to check it; (b) single-saddle cuffs that fit fingers at rest, with higher pressure (R11 at risk on the little finger). | (a). Accepted 2026-10-02 with a condition: nothing is worn until the co-design therapist has checked the spread on a range of hands with mild tone; switch to (b) if the spread raises tone or discomfort. |
| A3 | The pack is now about 723 g against the 450 g target of R7 (639 g before). | (a) keep the target under review with a therapist as already decided (N4 (c), waiting on O1) and weigh at TRL 4; (b) look for mass now (see the value-engineering savings in the register). | (a), with the savings in the register tried before TRL 4. Accepted 2026-10-02; the therapist review treats the pack mass as a safety question (load on a weak arm and shoulder). The listed savings come to about 30 to 60 g and cannot close the 273 g gap on their own. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan FXH-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status is unchanged in count: 1 not met (R7, now 723 g), 2 at risk (R2, R3), 7 met, 3 not verifiable at TRL 3 (FXH-CAL-001 v0.3). R12 is reported against the value-engineering target.
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept's pack, anchor block, lever and cuffs; they need updating on Amish's Mac, where Blender is.
- With A1 to A3 accepted: the release plate's pass mark is set before the TRL 4 test (10 s or less, with a pull force the co-design therapist agrees a care partner can apply one-handed), the cam lever being the fallback; nothing is worn until the therapist has checked the finger spread; the pack target stays under therapist review as a safety question. The build plan's release check and safety stop S6 carry these conditions (FXH-BLD-001 v0.2).
- Bought parts must be checked against the model when bought (gearbox face holes and shaft length, stop button depth, cell size, board sizes); these are listed in the design decisions register.
