# Review note: FlexHand

## Session 2026-09-25: /populate to a strong TRL 2 (overnight batch run)

### What was done

- `docs/01-problem.md` (FXH-PRB-001 v0.2): problem with cited evidence on hand impairment and therapy dose, prior devices (clinical gloves, NEOFECT, Columbia tendon orthosis, Exo-Glove Poly II), users and context, constraints, safety note, out of scope, open questions. There was no co-design checklist to keep.
- `docs/03-requirements.md` (FXH-REQ-001 v0.2): 13 measurable requirements (R1 to R13) with targets, planned verification, concept status and stated assumptions.
- `docs/02-concept.md` (FXH-PRC-001 v0.2): how it works, 17 numbered components, first-order numbers, key design choices with options, safety section, open questions.
- `cad/src/concept_media.py`: massing model of the forearm cuff, motor pack (two 25 mm gearmotors, spools, 2S cells, controller, drivers, lid, stop button), sheath anchor block, Bowden sheaths, glove, plates, finger cuffs, tendons and thumb spacer, on a grey forearm and hand for scale (no 1.75 m figure, as for TremorTrace). Modeled as a right hand and mirrored to a left hand so the thumb side faces the standard camera.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` (callouts 1 to 17), `cutaway.png` (motor pack only), `flow.png` (energy per session, all values estimates), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 19 lines with indicative prices, lines 1 to 17 matching the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line before "## Problem"; concept paragraph, key components and a safety note brought in line with the concept.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml` is unchanged; the pitch and problem still match the numbers found.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Extensor tendon force, design load | 30 N per finger (assumed), 0.41 N·m at the spool | R2 met, thin margin |
| Repetitions | about 6.4 cycles per min, about 385 per hour | R4 met |
| Sessions per charge (18 Wh 2S pack) | about 3.1 at 4.7 Wh per session | R6 met, no margin |
| Mass on the hand | about 90 g | R7 hand part met |
| Mass of forearm pack | about 510 g | **R7 not met** (450 g) |
| Cuff contact pressure | about 100 kPa with 12 mm cuffs | **R11 not met** (50 kPa) |
| Parts cost | about $280 | R12 met (budget $500 unchanged) |

Requirements not met or at risk:

- **R7 (pack mass) not met:** about 510 g against 450 g, driven by the two 25 mm gearmotors (about 190 g).
- **R11 (cuff pressure) not met:** about 100 kPa against a proposed 50 kPa. Wider (20 mm) cuffs would give about 43 kPa but may block PIP flexion.
- **R2 marginal:** peak spool torque is about 5 % above the gearbox maker's recommended continuous load, though within its intermittent limit.
- **R8 (donning time) at risk:** fitting cuffs on flexed, spastic fingers is unverified.
- **R6 no margin** at the design load.

### Proposed, awaiting Amish

1. **Motor route (drives R2 and R7).** (a) 25 mm 227:1 gearmotors on the forearm, about 510 g pack; (b) micro (N20) gearmotors with the force target cut to 20 N per finger, lighter but weaker than moderate tone may need; (c) a bench-top motor unit with longer sheaths, very light on the arm but departs from the wrist-mounted pitch. Recommendation: (a) for the first build and revisit the 450 g target with a therapist, since the forearm rests on a support during sessions.
2. **Motor count.** One motor for four fingers, two motors (one per finger pair) or four motors. Recommendation: two.
3. **Passive only or plan for active assist (pitch-level).** Evidence for passive motion alone improving function is weak; an active-assist mode triggered by the user's effort would strengthen the case but adds sensing and scope. Recommendation: keep the pitch as passive motion for TRL 3 and record active assist as a later option.
4. **Cuff pressure fix.** Wider padded cuffs, a distal anchor, or a lower force limit. Recommendation: 20 mm cuffs with a soft liner, checked for PIP clearance at TRL 3.
5. **Design load.** 30 N per finger for mild to moderate flexor tone. Recommendation: keep, and check against published stiffness data.
6. **Thumb passive** with an abduction spacer. Recommendation: keep for TRL 3.
7. **Tendons through Bowden sheaths** rather than a pneumatic glove. Recommendation: tendons.
8. **First clinical co-design partner** (stroke unit OT team, community rehabilitation service or university lab).
9. **Pack voltage** 2S (7.4 V) with 12 V rated motors, trading speed for a smaller pack. Recommendation: keep.

### Safety concerns

- Not a medical device; every document says so and must keep saying so.
- Forcing spastic or contracted fingers: layered force limits (firmware current limit, 60 N breakaway, hardware stop) are designed but unverified.
- Non-back-drivable gearboxes can hold the hand closed on power loss; the tool-free quick-release and a care partner within reach are essential.
- Users may not feel pressure; R11 is not met, so nothing should be worn until cuff pressure is reduced.
- 2S lithium-ion pack worn on the arm: protected pack, no charging while worn.

### Problems and notes

- PMC pages were blocked by a bot check during research, so the passive-mobilization study is cited by title and link without detailed results.
- The 30 N design load is an engineering estimate, not a measured value; it drives most of the numbers.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).
- The cutaway shows only the motor pack; the hand-side parts have nothing inside worth sectioning.

### Recommended next step

Review this note and the media, then decide items 1 and 3. If approved, run `/advance-trl3` to check the design load, torque, speed, power, mass and cuff pressure by calculation and produce the parametric model and drawing sheet.
