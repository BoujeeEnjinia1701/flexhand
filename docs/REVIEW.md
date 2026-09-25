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

## Session 2026-09-25: TRL 3

Amish reviewed the TRL 2 review points on 2026-09-25 and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." This session ran `/advance-trl3` on that authority and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (FXH-DDR-001 v0.1): the eight TRL 2 items with a recommendation recorded as "Decided by Amish, 2026-09-25: go with recommendation" (D1 to D8); the co-design partner left open (O1); five new items raised by the calculations (N1 to N5), proposed.
- `docs/04-calcs/01-sizing.md` (FXH-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: excursion, design load against published finger stiffness, transmission and torque, motor speed and cycle, force limit, energy, mass, cuff pressure and fit, stop time, cost and log storage, with a results table for R1 to R13. The script imports the model and the BOM and prints every quoted number with a tag.
- `cad/src/model.py`: parametric build123d model (forearm cuff, pack, motors, spools, idlers, cells, electronics, stop button, anchor block, sheaths, glove, plates, cuffs, tendons, thumb spacer) on a forearm and hand context. Exports `cad/step/flexhand-assembly.step`, `flexhand-on-forearm.step` and nine part files, with matching STL files in `cad/stl/`.
- `cad/src/sheets.py` and `cad/drawings/FXH-DWG-001.svg`, `.pdf`, `.png`: forearm unit general arrangement at Rev P1, 1:2, with main dimensions and parts list, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet keeps its number, FXH-DWG-010, so the general arrangement took FXH-DWG-001.
- `bom/bom.csv`: 20 lines, all priced, $281.90 against the $500 budget; line 20 (idler bearings) added; `bom/bom-notes.md` updated.
- `cad/src/concept_media.py` now builds the media from the model; all media in `media/` regenerated and checked by eye; temporary view folders removed.
- `docs/01-problem.md`, `docs/02-concept.md`, `docs/03-requirements.md` moved to v0.3 with the decisions and the TRL 3 numbers; `README.md` and `project.yaml` (trl: 3, trl_target: 3, trl_evidence) updated; PDFs rebuilt in `docs/pdf/`.
- Design change inside TRL 3 scope: the gearmotors now lie along the forearm with the spools at the front and idlers turning the tendons forward, because a 71 mm motor with its spool would not fit across a pack narrow enough for the forearm. The pack is 160 by 76 mm.

### Requirements (FXH-CAL-001), not met first

| ID | Status | Value against target |
| --- | --- | --- |
| R7 | **Not met** | Pack about 675 g against 450 g; hand 103 g against 120 g (met) |
| R11 | **Not met** | 46 to 84 kPa against 50 kPa; only the middle finger passes; 96 kPa on a small hand's little finger |
| R2 | At risk | 30 N delivered, but the 0.467 N·m peak is 119 % of the gearbox's continuous rating (RMS 65 %), and 30 N covers mild tone (MAS 1+) only; MAS 3 needs about 148 N |
| R3 | At risk | Current senses a finger pair: one finger can reach 80 N before a 40 N per finger limit trips (the 60 N breakaway acts first); friction spread -32 to +18 % |
| R5 | At risk | Fastest stroke at design load 3.3 s against 3 s |
| R1, R4, R6, R10, R12 | Met | 29.8 mm stroke; 448 cycles per hour; 3.9 sessions per charge; three sizes; $281.90 |
| R8, R9, R13 | Not verifiable at TRL 3 | Donning time; release time (stop time about 11 ms by calculation); limit lock |

Counts: 5 met, 3 at risk, 2 not met, 3 not verifiable at TRL 3. Numbers that changed from TRL 2: peak torque 0.41 to 0.467 N·m, cycles 385 to 448 per hour, sessions 3.1 to 3.9, pack mass 510 to 675 g, cuff pressure 100 kPa to 46 to 84 kPa.

### Decisions recorded (FXH-DDR-001)

Decided by Amish, 2026-09-25, going with the TRL 2 recommendations: D1 25 mm 227:1 gearmotors on the forearm, 450 g target to be revisited with a therapist; D2 two motors; D3 passive motion only, active assist a later option, pitch unchanged; D4 cuffs up to 20 mm with a soft liner, checked for PIP clearance (the check shows 20 mm does not fit; cuffs set to 12.2 to 18.6 mm); D5 30 N design load kept and checked against stiffness data; D6 thumb passive; D7 tendons in Bowden sheaths; D8 2S pack. The TRL 2 review recommended no change to the budget, pitch or problem line, so all three are unchanged. The SwapCell cross-cutting decisions do not apply (no SwapCell pack).

### Still awaiting Amish

- O1: first clinical co-design partner (no recommendation).
- N1: reword R2 to mild flexor tone (MAS 1 to 1+) or raise the design load. Recommendation: reword.
- N2: fingertip thimble sharing the extensor load (23 to 40 kPa). Recommendation: add it.
- N3: balance pulley so the current limit acts per finger. Recommendation: add it.
- N4: pack mass: lighter breakaways, perforated cuff, therapist-agreed target. Recommendation: the first two, then the target review.
- N5: relax the lower stroke-time limit to 4 s at design load. Recommendation: relax.

### Safety concerns

- Not a medical device; every document still says so.
- R11 is not met and R3 is at risk. Nothing may be worn until cuff pressure is reduced and the per-finger force limit is fixed; both are safety requirements.
- The design load suits mild tone only. Using it on fingers with moderate or severe tone would stall at the force limit, and raising the limit to compensate would overload the gearbox and the skin.
- The gearboxes hold position when unpowered: the tool-free release lever and a care partner within reach remain essential.
- Protected 2S lithium-ion pack worn on the arm: no charging while worn.

### Citations

- The passive-mobilization study, previously cited only by title because PMC showed a bot check, is now cited with authors, journal and year (Gobbo et al., *BioMed Research International*, 2017), confirmed by search. Its full text could not be fetched (PMC bot check, Wiley 403), so its detailed results are still not quoted.
- Motor data were checked on the Pololu 4869 specifications page (107 g, 24 kg·cm stall, 4 and 8 kg·cm recommended loads, $53.95).
- New citation: Heung et al., *Frontiers in Bioengineering and Biotechnology*, 2020, for finger joint stiffness after stroke (fetched and read).
- Phalanx length shares (47, 28 and 25 %) are stated as assumptions; the anthropometric source found (Buryanov and Kotiuk, 2010) could not be fetched, so it is not cited.

### Problems and notes

- No TRL 4 material exists in this repo (`electronics/`, `firmware/` and `build-log/` hold only the scaffold README), and none was created.
- The mean-pressure metric for R11 ignores skin shear and edge pressure; the cuff design needs a bench check at TRL 4 even if the numbers pass.
- The energy budget holds full torque with current during the extended dwell. If the gearbox holds without current, sessions per charge rise.

### Recommended next step

Decide N1 to N5 and name a co-design partner (O1). If Amish accepts N2 to N4, a further TRL 3 pass would add the fingertip thimble and balance pulley to the model and recalculate R3, R7 and R11. TRL 4 is on hold by Amish's instruction. For reference only, TRL 4 would need: a bench build of one finger-pair drive, a finger model with calibrated stiffness, measurements of tendon force against motor current, cuff pressure mapping, breakaway and release tests, and a TST report with `environment: lab`.
