---
doc_id: FXH-BLD-001
title: FlexHand prototype build plan
project: FlexHand
doc_type: Build plan
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan; design made constructable (FXH-DDR-003)
---

# FlexHand prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

> **Safety:** FlexHand is a research and educational prototype, not a medical device. It pulls on fingers that may be spastic or unable to feel, its gearboxes hold position when unpowered, and it carries a lithium-ion pack. This plan builds and bench-checks a prototype; nothing in it allows the device to be worn by a person. Follow the safety stops in section 6.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order. The pictures in this plan show the right-hand device; a left-hand device is its mirror image.*

The prototype is one FlexHand for a medium adult hand: a printed motor pack screwed onto a perforated forearm cuff, with an anchor block on its front end, and a fingerless glove carrying two plates, a thumb spacer, eight finger cuffs and four fingertip thimbles. Eight tendons run from the anchor block to the fingers inside eight Bowden sheaths. Figure 1 shows the 26 components in the order you make or fit them. Seventeen are made: fourteen 3D prints (pack base, anchor block, cuff shell, tray, lid, spools, dorsal and palmar plates, thumb spacer, finger cuffs, thimbles, pucks, release plate and cover), the cut foam liner, eight small breakaway couplings and the sheaths cut from bicycle shift housing. Everything else is bought: two gearmotors, bearings, cells, small electronic modules, the stop button, the glove, the straps, tendon line and fixings. The work is 3D printing in PETG and TPU, pressing in heat-set inserts, light drilling and tapping, stitching, tying and crimping line, and wiring bought modules. The parts cost about USD 304, from the bill of materials.

## 2. What changed to make it buildable

The concept showed what FlexHand does; many of its parts could not be made or fixed as drawn. Each change below keeps what FlexHand does, and all of them are recorded in decision record FXH-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Pack on the cuff | No fixing; the cuff cut into the pack floor | Floor raised 4 mm; six screws up through the cuff into inserts in the pack's ribs (Figure 3) | The pack must not move under the sheaths' push |
| Straps | Inside the foam liner | Over the cuff, under the pack between its ribs, then round the forearm (Figure 11) | How a strap holds a half shell |
| Gearmotors | Floating, no fixing | A printed bulkhead holds each gearbox face on two screws; a cradle holds the motor's rear (Figure 4) | The gearbox face is the motor's mounting face |
| Spools and idlers | Idlers cut into 20 mm spool flanges; no pins | 14 mm flanges and a set-screw hub; idlers on steel pins in a printed post and shelf (Figure 5) | Every part has room and a support |
| Rear bay | Boards overlapping and floating; cells loose; no 5 V supply for the controller | Cells in saddles under a screwed-down tray; boards laid out on the tray; a 5 V regulator added (Figure 6) | Every part has a seat and a fixing |
| Anchor block | 44 mm long, no room for couplings and springs, channels not in line with the tendons, no fixing | 53 mm long, 88 mm wide, four channels in line with the tendon exits, screwed to the pack (Figures 8 and 9) | The channel must hold everything that moves with the line |
| Quick release | A lever with no mechanism | A red release plate with a finger loop: pull it out and all eight sheaths and tendons go slack (Figure 9) | One pull, by hand, with no tools |
| Slack springs and stop beads | Eight of each, with no place | Four springs, one per pulley line; the stop beads at the hand end (Figure 19) | Same effect, with room for both |
| Finger cuffs and thimbles | Full rings that overlapped the next finger's; no tendon eyelets; no closure | Padded saddles top and bottom with thin sides, eyelets and end tabs, a hook-and-loop closure; fingers held slightly apart by the glove (Figure 24) | Same contact areas, and they fit side by side |
| Hand plates and sheaths | Sheaths ending on the plates with no stop; flexor sheaths through the wrist | Printed stop blocks on the plates; sheaths routed round the wrist (Figure 19) | A sheath needs a seat at both ends |
| Pack and cuff position | Pack 160 mm long | Pack 168 mm long, moved 16 to 24 mm toward the elbow; cuff moved 20 mm | Room for the bulkhead and longer block, which still stops 7 mm short of the wrist |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Thumb side" and "little-finger side" are as worn, palm down; "elbow end" and "wrist end" are along the forearm. Print tolerance is 0.2 mm on fits and 0.5 mm elsewhere unless a step says otherwise; drawings do not carry tolerances before TRL 4. Every printed part is printed in PETG unless its section says TPU or PA12.

### 3.1 Pack base

![Figure 2. Making sketch of the pack base](../cad/drawings/FXH-DWG-101.png)

*Figure 2. Pack base making sketch (FXH-DWG-101).*

**What it is and what it is made from.** The open box that carries the motors, spools, idlers, cells and electronics, with three saddle ribs underneath that sit on the cuff. PETG, printed, four perimeters, 30 % infill.

**How to make it.**

1. Print it open side up, 168 long and 76 wide, with 2 mm walls and a 2.5 mm floor. Use supports only under the three saddle ribs, which follow the cuff's curve underneath.
2. Clean the eight 3 mm and 3.4 mm holes in the front wall with a drill held in the fingers: two pairs of tendon exit holes 31.25 to each side of the centre line, 5.4 above and below the motor axis height; four screw holes 14 to each side, 6 above and below it.
3. Check the bulkhead holes: an 8 mm shaft hole 13.5 to each side of centre, 14 above the floor, and a 3.4 mm hole 8.5 either side of each shaft hole, countersunk on the front face.
4. Press in ten M3 heat-set inserts (5 mm long) with a soldering iron at about 230 °C: six from below into the rib bosses (9 to each side of the centre line) and four from above into the lid bosses.
5. Check that a 3 mm pin drops into the hole in each idler post and through each idler shelf.

**How it fits the parts next to it.**

![Figure 3. Joint 1: pack rib on the cuff shell](05-build-plan/joint-01.png)

*Figure 3. Each rib sits on the cuff shell; a button-head screw goes up through the shell into the insert in the rib's boss. The liner has a hole over the screw head.*

![Figure 4. Joint 3: motor in its cradle and bulkhead](05-build-plan/joint-03.png)

*Figure 4. The gearbox face sits flat on the back of the bulkhead, held by two countersunk screws from the front; the motor's rear sits in the cradle with a cable tie. The spool hub runs 0.5 mm in front of the bulkhead.*

![Figure 5. Joint 4: the idlers](05-build-plan/joint-04.png)

*Figure 5. The lower idler turns on a pin in a post from the floor; the upper idler on a pin pushed down through a shelf from the side wall. Each turns its spool line forward to its exit hole.*

![Figure 6. Joint 5: cells and tray](05-build-plan/joint-05.png)

*Figure 6. The cells sit in printed saddles; the tray rests on four posts 1 mm above them, with a foam pad between, and its four screws hold the cells down.*

The three ribs sit on the cuff shell at 18.5, 86.5 and 154.5 from the cuff's elbow end, on the solid strips between hole columns; the straps pass through the gap between floor and cuff between the ribs. The anchor block's back face sits flat on the front wall. The lid sits on the wall tops.

**Check before moving on.** A gearmotor slides into the cradle and its face sits flat on the bulkhead with both screw holes in line; the floor is flat within 0.5 mm.

### 3.2 Anchor block

![Figure 7. Making sketch of the anchor block](../cad/drawings/FXH-DWG-102.png)

*Figure 7. Anchor block making sketch (FXH-DWG-102).*

**What it is and what it is made from.** The block on the front of the pack in which each spool line's balance pulley shares its pull between two fingers. PETG, printed, four perimeters, 40 % infill.

**How to make it.**

1. Print it standing on its back face (the face that goes against the pack) so the four channels print as upright tunnels. It is 53 long, 88 wide and 31 tall.
2. Check the channels: 15 wide by 7 tall, centred 31.25 to each side of the centre line and 5.4 above and below the motor axis height, open at both ends. A 15 by 7 gauge must slide through each.
3. Press in eight M3 inserts: four in the back face (14 to each side of centre, 6 above and below the motor axis height) for the pack screws, and four in the front face (30 to each side, 2.8 from the bottom and 2.5 from the top) for the cover screws.

**How it fits the parts next to it.**

![Figure 8. Joint 6: anchor block on the pack front wall](05-build-plan/joint-06.png)

*Figure 8. Four cap screws from inside the pack go through the front wall into the block's inserts. The pack's exit holes open into the block's channels.*

![Figure 9. Joint 7: inside a channel](05-build-plan/joint-07.png)

*Figure 9. Inside one channel, from the pack end: the spool line and its slack spring, the balance pulley, one breakaway coupling for each finger, then the release plate, the sheath puck in its pocket in the cover, and the two sheaths.*

The back face sits flat on the pack front wall, with the channels in line with the exit holes. The release plate slides in a 3.4 gap between the front face and the cover. Each balance pulley rides in its channel with 30 of travel, more than the 29.8 stroke.

**Check before moving on.** Held against the pack's front wall, a 2 mm rod through each exit hole enters its channel without touching the sides.

### 3.3 Forearm cuff shell

![Figure 10. Making sketch of the forearm cuff shell](../cad/drawings/FXH-DWG-103.png)

*Figure 10. Forearm cuff shell making sketch (FXH-DWG-103).*

**What it is and what it is made from.** The perforated half shell that spreads the pack's weight over the back of the forearm. PETG, printed, 2 mm wall.

**How to make it.**

1. Print it lying on its back on tree supports: a half cone 174 long, inside radius 41 at the elbow end and 35 at the wrist end, with its edges 8 below the forearm's centre line.
2. Check the 70 holes of 12 mm, on a grid every 17 along and every 25° round.
3. Check the six 3.4 mm screw holes, 9 to each side of the top line at 18.5, 86.5 and 154.5 from the elbow end. They sit on the solid strips between hole columns.
4. Break every edge so nothing sharp can touch the skin.

**How it fits the parts next to it.**

![Figure 11. Joint 2: straps under the pack](05-build-plan/joint-02.png)

*Figure 11. Each strap lies over the shell, passes through the gap under the pack between two ribs, then wraps the skin under the forearm.*

The pack's ribs sit on its top with six M3 x 8 button-head screws coming up from inside (Figure 3). The liner is glued inside it after the pack is on. The two straps lie over it, 52.5 and 120.5 from the elbow end.

**Check before moving on.** On a forearm form or a 70 to 80 mm tube, the shell does not rock, and the six screw holes line up with the pack's rib bosses.

### 3.4 Cuff liner

![Figure 12. Making sketch of the cuff liner](../cad/drawings/FXH-DWG-104.png)

*Figure 12. Cuff liner making sketch (FXH-DWG-104).*

**What it is and what it is made from.** The 4 mm foam lining of the cuff shell. EVA foam sheet, 4 mm, with a self-adhesive back.

**How to make it.**

1. Lay the shell on its side on the foam and trace its inside edge while rolling it over; the pattern is a curved band 174 wide. Cut 2 mm inside the line and check the fit in the shell.
2. Mark and cut a 6.5 mm hole over each of the six screw heads.
3. After it is stuck in (step 4), punch the 12 mm holes through the shell's holes so they line up.

**How it fits the parts next to it.** Stuck to the inside of the shell, edge to edge, with the six screw heads in its holes.

**Check before moving on.** No foam stands proud of the shell's edges and no screw head can be felt through it.

### 3.5 Spools (make 2)

![Figure 13. Making sketch of the spool](../cad/drawings/FXH-DWG-105.png)

*Figure 13. Spool making sketch (FXH-DWG-105).*

**What it is and what it is made from.** The two-groove drum on each motor shaft: one groove pulls the extensor line while the other pays out the flexor line. PA12 from a print service (PETG works for a first build).

**How to make it.**

1. Print two, 16 long: a 4 mm hub, then three 1.5 mm flanges of 14 mm diameter with two 3.75 mm grooves on a 10 mm core between them.
2. Open the bore to a snug fit on the motor's 4 mm shaft with its flat.
3. Drill 2.5 mm across the hub and tap M3 for a set screw that bears on the shaft flat.
4. Drill a 1 mm hole through the core beside one flange in each groove, for tying the line.

**How it fits the parts next to it.** The hub sits 0.5 in front of the bulkhead, set screw on the shaft flat (Figure 4). The rear groove takes the extensor line, which leaves the top of the groove toward the side wall; the front groove takes the flexor line, which leaves the bottom of its groove (Figure 5).

**Check before moving on.** The flanges run true when the shaft is turned by hand.

### 3.6 Breakaway couplings (make 8)

![Figure 14. Making sketch of the breakaway coupling](../cad/drawings/FXH-DWG-106.png)

*Figure 14. Breakaway coupling making sketch (FXH-DWG-106), drawn larger than full size.*

**What it is and what it is made from.** A two-part link in each finger's line that pulls apart if that tendon's pull passes about 60 N. Socket and plug in PA12 from a print service (or turned brass), two 2 mm steel balls and a ring of 0.4 mm spring wire.

**How to make it.**

1. Socket, 6.8 across and 6 long: a 3.3 mm bore 4 deep from the front, a 1.4 mm hole through the back for the pulley line, two 2.05 mm holes across it 4 from the back, and a groove 3 mm deep round the outside over those holes.
2. Plug: a 6.8 head 4 long with a 1.4 mm hole for the tendon, and a 3.2 stem 3.8 long with a groove round it.
3. Push the stem into the socket, drop a ball into each hole, and spring the wire ring into the outside groove over them.
4. Check the pull-out force on a spring balance and mark each coupling; a thicker or thinner wire ring raises or lowers it. The aim is about 60 N; the force is set and recorded at TRL 4.

**How it fits the parts next to it.** One in each finger's line just in front of its balance pulley, two side by side in each channel (Figure 9). The socket is tied to the line round the pulley; the plug is tied to the tendon.

**Check before moving on.** Each plug pulls out and clicks back by hand at its set force.

### 3.7 Electronics tray

![Figure 15. Making sketch of the electronics tray](../cad/drawings/FXH-DWG-107.png)

*Figure 15. Electronics tray making sketch (FXH-DWG-107).*

**What it is and what it is made from.** A flat plate over the cells that carries the electronic modules. PETG, printed, 2 mm, solid.

**How to make it.**

1. Print it flat, 37.5 by 71 by 2.
2. Check the four 2.2 mm holes, 4 in from each end and 34.5 to each side of the centre line.
3. Lay out the modules on it with double-sided foam tape: in the row at the elbow end, from the thumb side, the charger (its USB-C port to the rear wall), the controller and motor driver 1; in the front row, the battery board and motor driver 2.
4. Wire the modules as Figure 16 shows, leaving the cell leads free.

![Figure 16. Block-level wiring](05-build-plan/wiring.png)

*Figure 16. Block-level wiring with wire sizes. No circuit board is laid out at this stage.*

**How it fits the parts next to it.** It rests on the four posts in the rear bay, 1 mm over the cells with a 1 mm foam pad between, and four M2.2 x 8 self-tapping screws hold it (Figure 6). The charger's port lines up with the opening in the rear wall.

**Check before moving on.** Every wire continues end to end; with the cells out, the battery board's pack terminals read open to every other rail.

### 3.8 Pack lid

![Figure 17. Making sketch of the pack lid](../cad/drawings/FXH-DWG-108.png)

*Figure 17. Pack lid making sketch (FXH-DWG-108).*

**What it is and what it is made from.** The cover over the pack, carrying the stop button. PETG, printed, 2 mm, solid.

**How to make it.**

1. Print it flat, 168 by 76 by 2, top face down.
2. Check the 19 mm stop button hole on the centre line, 51.2 from the elbow end, the 3 mm LED window over the controller, and the four 3.4 mm screw holes, 51 and 119 from the elbow end, 32.5 to each side of the centre line.

**How it fits the parts next to it.** On the wall tops; four M3 x 8 pan-head screws into the lid bosses. The stop button goes through it from above, its bezel on the lid and its nut below.

**Check before moving on.** The stop button's nut tightens with the bezel flat on the lid.

### 3.9 Dorsal plate

![Figure 18. Making sketch of the dorsal plate](../cad/drawings/FXH-DWG-109.png)

*Figure 18. Dorsal plate making sketch (FXH-DWG-109).*

**What it is and what it is made from.** The plate on the back of the hand where the four extensor sheaths end. TPU 95A, printed, 100 % infill.

**How to make it.**

1. Print it plate side down: 50 by 60 by 2.5, with a stop block 8 by 56 by 6.5 on its wrist edge.
2. Check the four 5.2 mm seats, 5 deep from the block's wrist face, and the 1.6 mm tendon holes on through. The seats are 24 and 8 to the thumb side and 8 and 23 to the little-finger side of centre, 3.25 above the plate.
3. Check the 1.5 mm stitching holes, 3 in from the edge, every 6.

**How it fits the parts next to it.**

![Figure 19. Joint 8: extensor sheath in the dorsal stop block](05-build-plan/joint-08.png)

*Figure 19. The sheath's ferrule sits in its seat; the tendon goes on through to the finger. The crimped bead stops against the block at the end of that finger's range.*

Stitched to the back of the glove over the hand, block toward the wrist.

**Check before moving on.** A sheath ferrule pushes fully into each seat.

### 3.10 Palmar plate

![Figure 20. Making sketch of the palmar plate](../cad/drawings/FXH-DWG-110.png)

*Figure 20. Palmar plate making sketch (FXH-DWG-110).*

**What it is and what it is made from.** The plate on the palm, next to the wrist crease, where the four flexor sheaths end. TPU 95A, printed, 100 % infill.

**How to make it.**

1. Print it plate side down: 34 by 60 by 2.5, with a stop block 8 by 56 by 6.5 on its wrist edge, on the outside face.
2. Check the four 5.2 mm seats and 1.6 mm tendon holes, at the same spacing as the dorsal plate, and the stitching holes.

**How it fits the parts next to it.** Stitched to the palm of the glove next to the wrist crease, block toward the wrist; the flexor sheaths end in its seats as in Figure 19.

**Check before moving on.** With the glove on a hand form, the hand still closes round a 40 mm tube.

### 3.11 Thumb spacer

![Figure 21. Making sketch of the thumb spacer](../cad/drawings/FXH-DWG-111.png)

*Figure 21. Thumb spacer making sketch (FXH-DWG-111).*

**What it is and what it is made from.** A ring on the thumb joined to a block in the web space, which holds the thumb out of the fingers' path. TPU 95A, printed, 100 % infill.

**How to make it.**

1. Print it with the ring's axis upright and supports under the block: a ring 26 across and 12 long, and a block 14 by 9.5 by 14 whose inner face follows the thumb.
2. Check the four 1.5 mm stitching holes through the block's flat face.

**How it fits the parts next to it.**

![Figure 22. Joint 10: thumb spacer on the glove](05-build-plan/joint-10.png)

*Figure 22. The block's flat face is stitched to the glove's thumb side at the web space; the ring slides over the thumb.*

**Check before moving on.** The thumb sits in the ring with no pressure marks after 10 minutes on a test hand.

### 3.12 Finger cuffs (make 8)

![Figure 23. Making sketch of the finger cuff](../cad/drawings/FXH-DWG-112.png)

*Figure 23. Finger cuff making sketch (FXH-DWG-112), drawn for the index anchor cuff.*

**What it is and what it is made from.** Padded bands on the fingers that the tendons pull on: a guide cuff on each first finger bone and an anchor cuff on each middle finger bone. TPU 95A, printed, with 2 mm foam liners.

**How to make it.**

1. Print each on end, no supports. Guide cuffs are 12 wide. Anchor cuffs are 16.4 (index), 18.6 (middle), 17.0 (ring) and 12.2 (little) wide. The bore is the finger's diameter: 18, 18, 17 and 15.
2. Each cuff is a padded saddle top and bottom, each covering 112° (2.5 mm of TPU outside a 2 mm liner), joined by 1 mm TPU side bands, with a slit in one side band.
3. Check the eyelets: a 2 mm hole on top of every cuff and under every guide cuff, and a tab with a 2 mm hole under every anchor cuff, where the flexor tendon ends.
4. Cut the liners from 2 mm foam and glue them into the saddles.
5. Glue a 6 mm hook-and-loop strip across each slit.

**How it fits the parts next to it.**

![Figure 24. Joint 9: cuffs and thimble on the index finger](05-build-plan/joint-09.png)

*Figure 24. The extensor tendon runs through the eyelets on top of both cuffs to the thimble's tab; the flexor runs through the guide cuff's lower eyelet and ends at the anchor cuff's tab.*

Each closes round its finger bone, 3 clear of each joint crease, slit on the side away from the next finger where possible. The glove holds the fingers slightly apart so neighbouring cuffs clear each other.

**Check before moving on.** On a test hand, every finger bends fully with all cuffs on, and no two cuffs touch.

### 3.13 Fingertip thimbles (make 4)

![Figure 25. Making sketch of the fingertip thimble](../cad/drawings/FXH-DWG-113.png)

*Figure 25. Fingertip thimble making sketch (FXH-DWG-113), drawn for the index finger.*

**What it is and what it is made from.** An open-tip band on each fingertip that shares the extensor pull with the anchor cuff. TPU 95A, printed, with 2 mm foam liners.

**How to make it.**

1. Print each on end, no supports: index 17.0, middle 19.0, ring 17.5 and little 13.2 wide, bore the fingertip's diameter.
2. Padded saddles top and bottom (2 mm of TPU outside a 2 mm liner) and 1 mm side bands, with no slit; a tab on top with a 2 mm hole for the end of the extensor tendon.
3. Glue in the liners.

**How it fits the parts next to it.** It slides onto the fingertip, from 3 beyond the last finger crease to the tip (Figure 24).

**Check before moving on.** It slides on and off; the nail and the tip stay uncovered.

### 3.14 Sheaths (make 8)

**What they are and what they are made from.** Eight lengths of 4 mm PTFE-lined bicycle shift housing, each with a ferrule on both ends. They carry the tendons from the anchor block to the hand plates (Figures 9, 19 and 1).

**How to make them.** Cut each length square with housing cutters, open the liner with a pin, and fit a ferrule on each end. The lengths include a fifth extra so the wrist can bend.

*Table 2. Sheath cut lengths.*

| Finger | Extensor sheath (over the back of the wrist) | Flexor sheath (down the side and under the wrist) |
| --- | --- | --- |
| Index | 77 | 145 |
| Middle | 82 | 164 |
| Ring | 82 | 164 |
| Little | 78 | 146 |

**How they fit the parts next to them.** The anchor end sits in a puck behind the cover (Figure 9); the hand end sits in its seat in a stop block (Figure 19). The index and little flexor sheaths go down the side of the wrist first and pass under it at the stop height; the middle and ring flexor sheaths go down nearer the hand and pass under them, deeper, so no two sheaths touch.

**Check before moving on.** Each tendon slides through its sheath freely by hand.

### 3.15 Sheath pucks (make 4)

![Figure 26. Making sketch of the sheath puck](../cad/drawings/FXH-DWG-114.png)

*Figure 26. Sheath puck making sketch (FXH-DWG-114).*

**What it is and what it is made from.** A small block that holds the anchor ends of two sheaths. PETG, printed, solid.

**How to make it.** Print four, 5 long by 14 wide by 6 tall, each with two 5.2 mm seats 3 deep in the front face, 8 apart, and 1.6 mm tendon holes on through to the back.

**How it fits the parts next to it.** It sits in a pocket in the cover, and its back presses on the release plate, which carries the sheaths' push. When the plate is pulled out, the puck and both sheaths slide back into the channel and both tendons go slack (Figure 9).

**Check before moving on.** The puck slides freely into a channel of the anchor block.

### 3.16 Release plate

![Figure 27. Making sketch of the release plate](../cad/drawings/FXH-DWG-115.png)

*Figure 27. Release plate making sketch (FXH-DWG-115).*

**What it is and what it is made from.** The plate that, pulled out by its loop, frees all eight sheaths at once. PETG, printed, 3 mm, solid, in red so it is easy to find.

**How to make it.**

1. Print it flat: 84 wide and 20 tall, with an 18 mm tab on the thumb side holding an 11 mm finger loop.
2. Check the two 1.6 mm slots, which run in from the little-finger edge to 36 past the centre, at the two tendon heights, so the plate slides off all eight tendons.

**How it fits the parts next to it.** It slides in the 3.4 gap between the anchor block's front face and the cover; the pucks press it against the block. To release, pull the loop toward the thumb side (Figure 9).

**Check before moving on.** With the cover screwed on and no tendons fitted, it slides out and back by hand.

### 3.17 Cover

![Figure 28. Making sketch of the cover](../cad/drawings/FXH-DWG-116.png)

*Figure 28. Cover making sketch (FXH-DWG-116).*

**What it is and what it is made from.** The front of the anchor block, holding the pucks and guiding the sheaths. PETG, printed, 40 % infill.

**How to make it.**

1. Print it front face down: 7.6 by 88 by 31.
2. Check the four pockets, 15 by 7 by 5.6, in the back face in front of each channel; the eight 4.5 mm sheath holes through the 2 mm front wall, 4 either side of each pocket's centre; and the four 5 mm spacer bosses, 3.4 long, with 3.4 mm screw holes, 30 to each side of centre at top and bottom.

**How it fits the parts next to it.** Its spacers sit on the anchor block's front face, held by four M3 x 16 cap screws into the block's front inserts; the release plate slides in the gap between them (Figure 9).

**Check before moving on.** The release plate slides through the gap without catching.

### 3.18 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Gearmotors (line 3).** Two 25 mm diameter, 71 mm long, 227:1 metal gearmotors rated 12 V with 48 counts-per-revolution encoders, 4 mm D-shaft, two M3 holes in the gearbox face.
- **Cells (line 5).** Two 18650 lithium-ion cells of 2,500 mAh from a maker that publishes a datasheet, and a 2S protection board rated 3 A or more.
- **Controller (line 6).** ESP32-S3 module of the small carrier type (about 18 by 21 mm).
- **Motor drivers (line 7).** Two single H-bridge carriers with a current-sense output (DRV8874 class).
- **Stop button (line 9).** 16 mm latching mushroom switch, normally closed, with bezel and panel nut, about 18 mm deep.
- **Sheath housing (line 11).** 2 m of 4 mm PTFE-lined shift housing and 16 ferrules.
- **Glove (line 12).** Fingerless, breathable, sizes S, M and L; it must leave the palm mostly open.
- **Tendon line (line 16).** 0.8 mm braided UHMWPE line.
- **Charger (line 18).** 2S lithium-ion charger module with USB-C input.
- **Idler and pulley bearings (lines 20 and 22).** Four 623 bearings (3 by 10 by 4) and four 693 bearings (3 by 8 by 4).
- **Fixing kit (line 24).** 18 brass M3 heat-set inserts 5 mm long; six M3 x 8 button-head, four M3 x 6 countersunk, four M3 x 8 pan-head, four M3 x 8 cap and four M3 x 16 cap screws; four M2.2 x 8 self-tapping screws; eight 3 mm steel pins (four 8 long, four 6.5 long); cable ties.
- **5 V regulator (line 25).** Step-down module, 6 to 9 V in, 5 V 1 A out.
- **Straps and consumables (lines 1 and 19).** Two 38 mm hook-and-loop straps, 6 mm hook-and-loop strip, foam tape, a 1 mm foam pad, a 100 µF capacitor, wire, heat shrink, crimp sleeves for the stop beads, strong polyester thread.

## 4. Putting it together

In each picture the parts already fitted are grey and the parts being fitted are in colour, with an arrow showing the way they go in.

### Step 1: inserts into the pack base and anchor block

![Step 1](05-build-plan/step-01.png)

Ten inserts in the base and eight in the block, pressed in square with the iron (sections 3.1 and 3.2).

### Step 2: anchor block onto the pack

![Step 2](05-build-plan/step-02.png)

Four M3 x 8 cap screws from inside the pack into the block's back inserts, snug. Check the exit holes line up with the channels.

### Step 3: pack onto the cuff shell

![Step 3](05-build-plan/step-03.png)

Six M3 x 8 button-head screws up through the shell into the rib inserts, snug only: the shell must not crack.

### Step 4: liner and straps

![Step 4](05-build-plan/step-04.png)

Stick the liner in over the screw heads and punch its holes (section 3.4). Thread each strap through the gap under the pack between two ribs.

### Step 5: gearmotors

![Step 5](05-build-plan/step-05.png)

Each gearbox face flat on the back of the bulkhead, two M3 x 6 countersunk screws from the front. The screws must not be longer than 6 mm, or they can reach the gears. A cable tie through the cradle slots round each motor.

### Step 6: spools

![Step 6](05-build-plan/step-06.png)

Each spool onto its shaft, hub 0.5 from the bulkhead, set screw tight on the flat.

### Step 7: idlers

![Step 7](05-build-plan/step-07.png)

Lower idlers on pins pressed into the floor posts; upper idlers held under the shelves by pins pushed down through them. A thin washer above and below each.

### Step 8: lines, springs, pulleys and couplings

![Step 8](05-build-plan/step-08.png)

For each of the four spool lines: tie the line through its groove's hole, wind about one turn, run it round its idler and out through its exit hole into the channel. Tie its slack spring and its balance pulley's pin to it. Run a line round the pulley and tie a coupling socket to each end, so the two sockets sit just in front of the pulley. Slide the set in from the front of the channel. Extensor lines go in the upper channels and flexor lines in the lower ones; the thumb-side channels serve the index and middle fingers.

### Step 9: cells and regulator

![Step 9](05-build-plan/step-09.png)

Cells into their saddles with the battery board leads free; the regulator on foam tape beside the stop button well. **Hold point:** safety stop S1.

### Step 10: tray, modules and wiring

![Step 10](05-build-plan/step-10.png)

Foam pad on the cells, tray onto its posts with four screws, then finish the wiring as Figure 16, with the cell leads still unconnected. **Hold point:** safety stop S2.

### Step 11: lid and stop button

![Step 11](05-build-plan/step-11.png)

Stop button through the lid, nut below; lid on with four M3 x 8 pan-head screws.

### Step 12: plates and thumb spacer onto the glove

![Step 12](05-build-plan/step-12.png)

With the glove on a hand form, stitch each plate and the thumb spacer through its holes with strong polyester thread.

### Step 13: cuffs, thimbles and tendons

![Step 13](05-build-plan/step-13.png)

Cut eight tendons about 400 long. Thread each extensor from the dorsal stop block through the eyelets on top of its two cuffs and tie it off at its thimble's tab. Thread each flexor from the palmar stop block through its guide cuff's lower eyelet and tie it off at its anchor cuff's tab. Slide a crimp sleeve onto each tendon between the stop block and the first cuff, and leave it loose.

### Step 14: sheaths

![Step 14](05-build-plan/step-14.png)

Slide each sheath over its tendon, hand end into its stop block seat. Extensors go over the back of the wrist, flexors down the side and under the wrist as section 3.14 describes.

### Step 15: pucks, release plate and cover

![Step 15](05-build-plan/step-15.png)

Pass each pair of tendons through a puck, seat the sheath ends in the puck, and tie each tendon to its coupling plug; click the plugs into the sockets. Slide the release plate into place, drop the pucks into the cover's pockets, and fit the cover with four M3 x 16 cap screws. With the motors at mid-stroke and the hand form's fingers half bent, take up the slack at each coupling plug, then set each stop bead at the end of its finger's range and crimp it. **Hold point:** safety stop S4.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of FXH-REQ-001. All are bench checks on a hand form or finger model, not on a person.

*Table 3. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Tendon stroke | R1 | Run each motor end to end with no load; measure the tendon travel at the hand plate | At least 29.8 mm on every tendon |
| Release | R9 | With 40 N on each finger of the finger model, pull the release plate | All eight tendons slack within 10 s, by hand, with no tools; pull force recorded |
| Stop button | R9 | Press it during a stroke | Both motors stop at once; the controller logs the stop |
| Breakaway | R3 | Pull each coupling apart on a spring balance | About 60 N, the value recorded for each |
| Force limit | R3 | Block one finger of the model; raise the load on the other | The motor stops at the set current; neither finger passes 40 N |
| Stop beads | R3 | Block one finger; run a full stroke | The other finger stops at the end of its own range |
| Stroke time and dose | R4, R5 | Time 20 cycles at design load on the model | Stroke adjustable from 4 to 15 s; 300 or more cycles an hour |
| Extension force | R2 | Spring-loaded finger model at design load | 30 N reached at full extension; motor temperature recorded |
| Sessions per charge | R6 | Run cycles on the model from a full charge | 3 or more hours of cycling |
| Mass | R7 | Weigh the forearm unit and the hand parts | Hand parts 120 g or less (117 g estimated); forearm unit recorded (723 g estimated) |
| Fit | R10 | Fit the glove and cuffs to hand forms of 170, 183 and 205 mm | Every cuff 3 mm clear of each crease; no two cuffs touch |
| Cuff pressure | R11 | Pressure film under each cuff and thimble at design load on the model | Mean 50 kPa or less |
| Session log | R13 | Run a session; read the log | Time, cycles and peak current recorded; limits cannot be changed from the user controls |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the cells come into the workshop.** Each cell reads 3.0 to 4.1 V, with no dents, swelling or leaks, and has a datasheet from its maker. A charging spot is ready on a non-combustible surface with a fire extinguisher for electrical fires in reach.
- **S2. Before the cells are connected to the battery board.** With the cells out, the pack, motor and 5 V rails read open to each other; the battery board's cell order is checked with a meter, not by wire colour; the stop button opens the motor supply when pressed.
- **S3. Before first power.** The lid is on; the anchor block's channels have no lines in them; a current-limited bench supply at 7.4 V and 1 A stands in for the cells; the stop button cuts the motors at once.
- **S4. Before any tendon is loaded.** The release plate slides out freely; every coupling's force has been set; the force limit is set in firmware at its lowest value; the stop beads are crimped; a person who knows the release is within reach.
- **S5. Charging.** Only with the pack off any arm or form, on the charging spot, attended; stop if a cell passes 45 °C or the pack swells.
- **S6. Before anything is worn by a person (outside this plan).** Not part of this build. Wearing needs the TRL 4 bench results, a supervising therapist, informed consent and, in a research setting, ethics review.

## 7. Tools, skills and workspace

**Tools.** FDM 3D printer with a bed of at least 180 by 100 mm that prints PETG and TPU 95A; soldering iron with a heat-set insert tip; drills 1 to 3.4 mm in a hand drill and pin vice; M3 tap; countersink; craft knife and steel rule; 12 mm and 6.5 mm hole punches; housing cutters; crimping pliers; hex keys 1.5 to 2.5 mm; small screwdrivers; needle and strong polyester thread; spring balance to 100 N; digital calipers; multimeter; bench power supply with a current limit (0 to 15 V, 0 to 3 A); hand form or finger model.

**Skills.** No certified trade is needed. 3D printing in PETG and TPU, pressing in heat-set inserts, simple soldering and crimping, hand sewing, tying line, safe use of a bench supply and care with lithium cells. All circuits are extra-low voltage: 8.4 V at most; no mains wiring is part of this build.

**Workspace.** A bench about 1.2 by 0.6 m; a ventilated place for the printer and soldering; the charging spot of S1.

**Personal protective equipment.** Safety glasses when cutting housing and crimping; no loose sleeves or long hair near the spools while the motors run.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 203 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/FXH-DWG-101` to `FXH-DWG-116`.
- General arrangement: `cad/drawings/FXH-DWG-001.pdf`, Rev P3.
- Calculations: `docs/04-calcs/01-sizing.md` (FXH-CAL-001 v0.3) and `docs/04-calcs/sizing.py`; stroke [A2], force and torque [C2], speed and dose [D2], [D3], force limit and pulley travel [E1] to [E4], energy [F2], [F3], mass [G2], [G4], pressure [H2], [H3], cost [J1].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (FXH-DDR-003), with FXH-DDR-001 and FXH-DDR-002.
- Requirements: `docs/03-requirements.md` (FXH-REQ-001 v0.5).
