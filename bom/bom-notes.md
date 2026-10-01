# BOM notes

- Line numbers match the callouts in `media/exploded.png` and the parts list on drawing FXH-DWG-001 (Rev P3). Line 19 (wiring and consumables) is not modeled.
- Every line is priced. Costs are indicative single-unit prices in USD for TRL 3 review. The gearmotor price (line 3, Pololu 4869, $53.95) was checked with the supplier on 2026-09-25; the other prices are indicative and suppliers are not yet selected.
- Value-engineering target: USD 500 (`budget_usd` in `project.yaml`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 303.90 (USD 196.10 under the target), computed by `docs/04-calcs/sizing.py` [J1].
- The gearmotor choice (line 3) was decided by Amish on 2026-09-25 (FXH-DDR-001, D1).
- Lines 1, 10, 21 and 22 changed after Amish accepted the TRL 3 recommendations on 2026-09-25 (FXH-DDR-002): the forearm cuff is perforated (N4), the anchor block is 44 mm long with ball-detent breakaways, balance pulley channels and tendon stop beads (N3, N4), and the fingertip thimbles (line 21, N2) and balance pulley bearings (line 22, N3) are new.
- Line 15: the anchor cuffs are as wide as each middle phalanx allows (12.2 to 18.6 mm). With the thimbles of line 21 sharing the load, contact pressure meets R11 on paper (FXH-CAL-001, section H).
- Line 20 (idler bearings) is new at TRL 3, from the layout with the motors along the forearm.
- This is a priced bill of materials for design review, not a purchasing list.
- FXH-DDR-003 (design for construction, 2026-10-01) changed lines 1, 2, 4, 5, 8 to 11, 13 to 15, 17, 19 and 20 and added line 23 (electronics tray), line 24 (fixing kit) and line 25 (5 V regulator). Line 19 no longer covers fasteners; they are in line 24.
