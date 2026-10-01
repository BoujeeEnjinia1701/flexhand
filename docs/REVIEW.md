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

Status update: items 1 to 7 and 9 were decided by Amish on 2026-09-25 (go with recommendation, FXH-DDR-001, D1 to D8). Item 8 has no recommendation and stays proposed, awaiting Amish (O1).

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
- N1: reword R2 to mild flexor tone (MAS 1 to 1+) or raise the design load. Recommendation: reword. Decided by Amish, 2026-09-25: go with recommendation (FXH-DDR-002).
- N2: fingertip thimble sharing the extensor load (23 to 40 kPa). Recommendation: add it. Decided by Amish, 2026-09-25: go with recommendation (FXH-DDR-002).
- N3: balance pulley so the current limit acts per finger. Recommendation: add it. Decided by Amish, 2026-09-25: go with recommendation (FXH-DDR-002).
- N4: pack mass: lighter breakaways, perforated cuff, therapist-agreed target. Recommendation: the first two, then the target review. Decided by Amish, 2026-09-25: go with recommendation (FXH-DDR-002); the target review waits on O1.
- N5: relax the lower stroke-time limit to 4 s at design load. Recommendation: relax. Decided by Amish, 2026-09-25: go with recommendation (FXH-DDR-002).

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

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation (N1 to N5) is now decided as recommended and applied at TRL 3; the co-design partner (O1) has no recommendation and stays open.

### What was done

- `docs/decisions/0002-recommendations-accepted.md` (FXH-DDR-002 v0.1): N1 to N5 recorded as "Decided by Amish, 2026-09-25: go with recommendation", with what changed; O1 left open.
- `docs/decisions/0001-trl2-review-decisions.md` to v0.2: N1 to N5 marked decided.
- `cad/src/model.py`: fingertip thimbles (`thimbles`, BOM 21), four floating balance pulleys (`balance_pulleys`, BOM 22) in channels in an anchor block lengthened from 12 to 44 mm, perforated forearm cuff shell and liner (12 mm holes, 33 % open), flexor sheath route adjusted to the longer block. STEP and STL re-exported, including `flexhand-thimbles.step` and `.stl`.
- `cad/src/sheets.py` and `cad/drawings/FXH-DWG-001.*`: Rev P1 to P2 (balance pulleys, anchor block length, perforation, thimble widths, parts list item 22).
- `docs/04-calcs/sizing.py` and `docs/04-calcs/01-sizing.md` (FXH-CAL-001 v0.1 to v0.2): balance pulley loss and per-finger limit, stop beads, thimble load sharing, new masses, R2 and R5 restated; all tables recomputed.
- `bom/bom.csv`: lines 1 and 10 updated, lines 21 and 22 added; `bom/bom-notes.md` updated.
- `docs/01-problem.md` (v0.4), `docs/02-concept.md` (v0.4), `docs/03-requirements.md` (v0.4) updated; `project.yaml` trl_evidence lists DDR-002; budget, pitch and problem lines unchanged.
- `README.md`: concept paragraph and key components updated; new sections "Concept rationale", "Burning platform", "Where it could be used" and "What sparked the idea" (continuous passive motion, Salter, Toronto, 1978).
- All media regenerated from the model (`cad/src/concept_media.py`), checked by eye; all PDFs re-rendered with the designmolecule.com footer.

### Decisions applied (before and after)

| Item | Change | Before | After |
| --- | --- | --- | --- |
| N1 | R2 wording | "moderate flexor tone" | "mild flexor tone (MAS 1 to 1+)"; 30 N covers the 18 N needed |
| N2 | Fingertip thimbles | Cuff pressure 46 to 84 kPa (96 kPa small hand) | 23 to 40 kPa (46 kPa small hand); hand side 103 to 115 g |
| N3 | Balance pulleys | One finger up to 80 N at the pair trip | 40 N per finger; efficiency 0.694 to 0.659; peak torque 0.467 to 0.492 N·m |
| N4 | Ball-detent couplings, perforated cuff | Pack 675 g | Pack 639 g (40 g and 25 g saved, about 32 g added by the longer block and pulleys) |
| N5 | R5 lower limit | 3 to 15 s | 4 to 15 s at design load; fastest 3.3 s (3.9 s pessimistic) |
| Budget | No change recommended | $500; parts $281.90 | $500; parts $289.90 |

### Requirement status (FXH-CAL-001 v0.2), not met first

| ID | Status | Value against target |
| --- | --- | --- |
| R7 | **Not met** | Pack 639 g against 450 g; hand 115 g against 120 g (met) |
| R2 | At risk | 0.492 N·m peak, 125 % of the gearbox's continuous rating (RMS 68 %) |
| R3 | At risk | 40 N per finger with balance pulleys; friction spread 27 to 47 N at a 40 N setting |
| R1, R4, R5, R6, R10, R11, R12 | Met | 29.8 mm stroke; 445 cycles per hour (360 at 4 s strokes); 3.3 s fastest stroke; 3.8 sessions; three sizes; 40 kPa worst (on paper); $289.90 |
| R8, R9, R13 | Not verifiable at TRL 3 | Donning time; release time; limit lock |

Counts: 7 met, 2 at risk, 1 not met, 3 not verifiable at TRL 3 (was 5, 3, 2, 3).

### Still awaiting Amish

- O1: first clinical co-design partner (no recommendation). The therapist review of the 450 g pack target (D1, N4 (c)) and of the 50 kPa pressure limit waits on it.

### Cross-repo actions

- None. FlexHand does not share parts or interfaces with another repo.

### Safety concerns

- Not a medical device; every document still says so.
- R11 is met only on paper, under an assumed load split between cuff and thimble, and R3 is at risk. Nothing may be worn until pressure is mapped and the force limit is checked on a bench.
- New hazard from N3: with a balance pulley, a free finger can travel up to twice its range if its partner is held back. The stop bead on each finger tendon must be set to that finger's range before any use.
- The gearboxes hold position when unpowered: the tool-free release lever and a care partner within reach remain essential. Protected 2S lithium-ion pack: no charging while worn.

### TRL 4

TRL 4 remains on hold by Amish's instruction. No build, test, purchasing, PCB or firmware work was done. For reference only, TRL 4 would need a bench build of one finger-pair drive with its balance pulley, pressure mapping under cuff and thimble, breakaway, stop-bead and release tests, and a TST report.

### Recommended next step

Name a clinical co-design partner (O1) so that the pack-mass target and the pressure limit can be reviewed with a therapist. The design is otherwise complete at TRL 3.

## Session 2026-09-26: sources strengthened

Amish asked for the weaker sources to be fixed. README sections "Concept rationale" to "What sparked the idea" were checked link by link; every link now in those sections was fetched and supports its claim.

| Where | Old source | New source |
| --- | --- | --- |
| By country or region, India | None (income group and urban concentration of the workforce uncited) | Handa et al., *Current Physical Medicine and Rehabilitation Reports*, 2023 (WHO STARS review): stroke units clustered in metropolitan cities and tertiary centers, nearly absent at primary and secondary facilities |
| By country or region, Brazil | None (public system, ageing population and university groups uncited) | Silva et al., *Arquivos de Neuro-Psiquiatria*, 2024 (2019 National Health Survey): 24.6 % reported access to rehabilitation; 73.4 % of those with activity limitations had no physiotherapy |
| By country or region, Canada | Canadian Medical Hall of Fame (kept) | Same source; the uncited claim about rural distances was removed so the row states only what the source supports |
| Burning platform, therapy dose | Lang et al., 2009 (journal page, kept) | Added the open copy at Marquette University's repository, which was fetched and confirms 312 sessions and 32 repetitions; "hundreds" made specific as 400 to 600 repetitions per session in animal studies |
| Burning platform, dexterity at six months | Kwakkel et al., *Stroke*, 2003 | Removed from the README: the journal and PubMed pages refused automated access in this session, so the 38 % figure could not be re-verified. It remains in `docs/01-problem.md` (a peer-reviewed source, not a weak one) and can return to the README once checked. |
| What sparked the idea | Canadian Medical Hall of Fame plus Salter et al., JBJS 1980 (PubMed) | Canadian Medical Hall of Fame (the official laureate page, which confirms 1978, the Hospital for Sick Children and the immobilization reasoning). The PubMed link was dropped because the page could not be read in this session; the uncited line about bedside, single-joint machines was removed. `INSPIRATIONS.md` line updated to match. |

Kept and re-verified: IHME news release on the GBD 2021 stroke analysis in *The Lancet Neurology* (11.9 million new strokes, 93.8 million survivors, 70 % and 86 % rises, more than three-quarters in low- and middle-income countries); WHO rehabilitation fact sheet (fewer than 10 skilled practitioners per million in many low- and middle-income settings); CDC stroke facts (more than 795,000 strokes a year; a leading cause of serious long-term disability). No budget change; `docs/01-problem.md` cites no weak source for these claims and is unchanged.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session added an appearance model for photoreal renders; the render images themselves (`media/render-hero.png`, `media/render-exploded.png`) are produced separately from it.

### What was done

- `cad/src/product_model.py` (new): `product_parts()` returns 50 parts (49 device parts in the shell and internal groups plus the shared clay forearm and hand as context), with `TITLE` and three `RENDER_VIEWS` (hero, exploded and a thumb-side detail view). It imports `PARAMS`, `derived()` and `build_parts()` from `model.py`; `model.py`, the BOM and the other documents are unchanged. It adds:
  - a motor pack with filleted corners, a parting line between base and lid, four lid screws, side grip ribs, a USB-C port at the charger and a raised "FLEXHAND" marking with a teal accent line;
  - a clear window in the lid over the spools, so the spools, tendon windings and idlers show from outside;
  - an emergency stop with a yellow collar and knurled red mushroom cap, a teal start and pause button and a lit status LED;
  - a filleted anchor block with a seam, hinge lugs and a ribbed teal quick-release lever, with the balance pulleys inside;
  - gearmotors split into encoder cap, can and gearbox; two-flange spools with tendon windings; idler and balance bearings with shields; tendon runs from the spools around the idlers to the exit slots; cells with end caps; circuit boards on an electronics tray;
  - a perforated forearm cuff with a foam liner, hook-and-loop straps (fabric), buckles and teal pull tabs;
  - swept Bowden sheaths with metal ferrules at both ends and sheath stops on the plates;
  - a knit fingerless glove (fabric) with a wrist hem and knuckle binding, TPU dorsal and palmar plates, padded finger cuffs with liners and tendon eyelets, fingertip thimbles with tip tabs, a thumb spacer and the tendons along the fingers.
- `README.md`: hero image now points to `media/render-hero.png`; the links line starts with the exploded render.

Every part is a valid solid and tessellates at the render tolerance. Previews from the kit renderer (without the clear window) were checked for fit on the clay hand.

### Differences from model.py (Proposed, awaiting Amish)

1. **Forearm cuff section.** `model.py` models the forearm as a round cone (radius 29 to 38 mm), while the shared clay forearm is elliptical and flatter. In the appearance model the cuff shell, liner and straps follow the clay forearm with the `model.py` thicknesses (4 mm liner, 2 mm shell), axial extent, hole pattern and strap positions; the pack saddle ribs are trimmed to meet it. Recommendation: keep `model.py` as is for sizing (the round cone is a conservative envelope) and consider an elliptical forearm section when the cuff is fitted at a later TRL.
2. **Hand-side soft parts on the clay hand.** `model.py` puts the finger cuffs, thimbles and tendons on straight fingers along X and the glove and plates on a box palm. Here they sit on the clay hand's relaxed, slightly curled fingers and rounded palm. Cuff and thimble widths, wall and liner thicknesses, the plate plan sizes and the sheath end positions in plan are as `model.py`; the heights of the sheath ends follow the clay palm surface (within about 4 mm). Recommendation: accept for renders only; no change to `model.py`.
3. **Features that are not in the BOM.** The clear spool window, the start and pause button, the status LED light pipe and the "FLEXHAND" marking are appearance proposals. The precis mentions user buttons and the BOM mentions an LED window in the lid, but neither defines them. Recommendation: keep the LED window and one start and pause button; decide on the clear spool window with the enclosure design, since it shows tendon wear but adds a part.
4. **Strap routing.** In `model.py` the straps sit under the cuff liner; here they pass over the cuff shell on top and on the skin underneath, which is how a hook-and-loop strap would hold a half shell. Recommendation: adopt this routing in the concept description when the cuff is next revised.

### TRL

This is an appearance model only: no tolerances, fabrication detail, PCB layouts or build information. `trl` stays 3, and TRL 4 remains on hold by Amish's instruction.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: design for construction and prototype build plan (kit 1.7.0)

Amish approved the build plan format on 2026-09-30 and asked for it to be extended to every repo, with outstanding decisions kept in a separate design decisions register. This session installed kit 1.7.0, made the FlexHand design constructable under his 2026-09-30 instruction ("If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations."), and wrote the illustrated build plan. Nothing was built or tested; TRL 4 stays on hold.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` matches `.kit/CLAUDE.md`.
- `cad/src/model.py` rewritten as a constructable model, part by part, with `python cad/src/model.py --check`: 203 constructability checks (no overlaps, nothing inside the forearm or hand, every joint touching, clearances, the release plate's path). All pass. STEP and STL re-exported.
- `docs/decisions/0003-design-for-construction.md` (FXH-DDR-003 v0.1, Draft): every change, with its reason; open for Amish's review.
- `cad/src/build_plan_media.py`: overview, 16 making sketches (`cad/drawings/FXH-DWG-101` to `116`), 10 joint close-ups, 15 assembly step pictures and a block-level wiring picture in `docs/05-build-plan/`.
- `docs/05-build-plan.md` (FXH-BLD-001 v0.1) and `docs/06-design-decisions.md` (FXH-DEC-001 v0.1), both new.
- `docs/04-calcs/sizing.py` and `01-sizing.md` (FXH-CAL-001 v0.3): masses recomputed from the new parts; cost reported against the value-engineering target. `docs/02-concept.md` (v0.5), `docs/03-requirements.md` (v0.5) and `docs/01-problem.md` (v0.5) updated to match.
- `bom/bom.csv`: lines 1, 2, 4, 5, 8 to 11, 13 to 15, 17, 19 and 20 updated; lines 23 (electronics tray), 24 (fixing kit) and 25 (5 V regulator) added. `bom/bom-notes.md` updated.
- `cad/src/sheets.py` and `cad/drawings/FXH-DWG-001`: Rev P3. Concept media regenerated with `cad/src/concept_media.py`.
- `project.yaml`: `design_state: constructable`; the build plan, the register and FXH-DDR-003 added to `trl_evidence`; `budget_usd` unchanged. `README.md`: links line and a "Building the prototype" section.

### Design changes made for construction (FXH-DDR-003)

1. Pack screwed to the cuff: floor raised 4 mm; three ribs on the solid strips between cuff holes, six M3 screws up through the shell into heat-set inserts; liner holes over the screw heads.
2. Straps over the shell and through the gap under the pack between its ribs (they were inside the liner).
3. Gearmotors held by a printed 3 mm bulkhead (two M3 screws into each gearbox face) and a cradle with cable ties; motor axes 13.5 mm from centre (was 15).
4. Spool flanges 14 mm (were 20, which the idlers cut into), a set-screw hub; idlers on 3 mm pins in a printed floor post and wall shelf.
5. Rear bay: cells in saddles, an electronics tray on four posts holding them down, boards laid out without overlap, a USB-C opening, a 6 mm cable gap behind the motors, and a 5 V regulator for the controller (a missing part).
6. Anchor block 53 mm long (was 44), 88 mm wide, full pack height, with four 15 by 7 mm channels in line with the tendon exits, holding each line's slack spring, balance pulley (30 mm travel) and two couplings; screwed to the pack front wall.
7. Tool-free release made real: sheath pucks press on a red pull-out release plate between the block and a cover; pulling it out slackens all eight tendons (the lever had no mechanism).
8. Pack 168 mm long, moved 16 to 24 mm toward the elbow; cuff moved 20 mm, same length; the block stops 7 mm short of the wrist.
9. Four slack springs (one per spool line) instead of eight; stop beads at the hand end, against the stop blocks.
10. Finger cuffs and thimbles as padded saddles with thin side bands, eyelets, end tabs and a hook-and-loop closure; fingers held slightly spread by the glove so neighbouring cuffs clear.
11. Sheath stop blocks on the dorsal and palmar plates; plates stitched to the glove; sheaths re-routed so none passes through the wrist, the glove or another sheath.
12. Thumb spacer block moved to the web space, shaped to the thumb and stitched to the glove; glove given a thumb opening.
13. Fixing kit listed (BOM line 24).
14. Breakaway coupling detent: two 2 mm balls and a spring-wire ring in a 6.8 mm body (a 4 mm ball and spring could not fit two couplings side by side).

### Key results (FXH-CAL-001 v0.3)

- Forearm pack about 723 g (was 639 g): **R7 still not met**, now further from 450 g. Hand side 117 g (met).
- Value-engineering target: USD 500. Estimated cost of the constructable design: USD 303.90 (USD 196.10 under the target).
- Forces, speeds, energy, pressures and requirement counts unchanged: 1 not met (R7), 2 at risk (R2, R3), 7 met, 3 not verifiable at TRL 3.

### Proposed, awaiting Amish

Listed in `docs/06-design-decisions.md`: accept the design-for-construction changes; confirm the pull-out release plate in place of the lever; confirm with a therapist that the glove may hold the fingers slightly spread; the pack-mass target (723 g against 450 g); the clinical co-design partner (O1). Eight items to confirm when parts are bought are listed there too.

### Safety

- The release changed form (pull-out plate instead of a lever); its pull force and 10 s release time are TRL 4 bench checks, and it is listed for Amish's confirmation.
- The build plan's safety stops keep everything on a bench and a hand form; nothing may be worn.
- Not a medical device; every document still says so.

### Stale media (made on Amish's Mac)

`media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png` and `media/social-preview.png` still show the concept's pack, anchor block, lever and full-ring cuffs; `cad/src/product_model.py` follows the concept too. They need regenerating on the Mac.

### Kit problems found

- build123d's SVG exporter, used by `.kit/drawing.py`, raises an AssertionError on a projected elliptical arc whose ends coincide (here on the swept sheaths). `.kit/` was not edited; `cad/src/svg_patch.py` skips such arcs, as build123d already does for arcs shorter than 1e-6, and is imported by `sheets.py`, `concept_media.py` and `build_plan_media.py`. The kit should carry the fix.
- The mirrored constructable pack base raised a Standard_DomainError in hidden-line projection, so the concept media and FXH-DWG-001 now show the right-hand device as modelled (the media were a mirrored left hand before), matching the build plan.

### Recommended next step

Review FXH-DDR-003 and the register (items 2 to 5). TRL 4 remains on hold.
