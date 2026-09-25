# BOM notes

- Line numbers match the callouts in `media/exploded.png` and the parts list on drawing FXH-DWG-001. Line 19 (wiring and consumables) is not modeled.
- Every line is priced. Costs are indicative single-unit prices in USD for TRL 3 review. The gearmotor price (line 3, Pololu 4869, $53.95) was checked with the supplier on 2026-09-25; the other prices are indicative and suppliers are not yet selected.
- Parts total: $281.90 against the $500 budget in `project.yaml` (56 %), computed by `docs/04-calcs/sizing.py` [J1].
- The gearmotor choice (line 3) was decided by Amish on 2026-09-25 (FXH-DDR-001, D1).
- Line 15: the anchor cuffs are as wide as each middle phalanx allows (12.2 to 18.6 mm) and still do not meet the contact pressure requirement (R11). A fingertip thimble is proposed (FXH-DDR-001, N2) and is not in this BOM.
- Line 10: the eight magnetic breakaway couplings add about 56 g to the pack; ball-detent couplings are proposed as a lighter option (N4).
- Line 20 (idler bearings) is new at TRL 3, from the layout with the motors along the forearm.
- This is a priced bill of materials for design review, not a purchasing list.
