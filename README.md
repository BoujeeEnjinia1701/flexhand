# FlexHand

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** BioMedical · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** about $500 USD · **Difficulty:** 4 of 5

Soft-actuated finger exoskeleton for continuous passive motion, driven by tendons from a wrist-mounted motor pack.

![FlexHand concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement (PDF)](cad/drawings/FXH-DWG-001.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Problem

Post-stroke hand rehab needs many repetitions, but therapist time is limited.

Problem statement: [docs/01-problem.md](docs/01-problem.md)

## Concept

Soft-actuated finger exoskeleton for continuous passive motion, driven by tendons from a wrist-mounted motor pack.

A fingerless glove carries TPU cuffs on the four fingers. Two gearmotors lying along the forearm in a strapped-on pack each turn a two-groove spool that pulls the flexor tendons of a finger pair while paying out the extensor tendons, through Bowden sheaths that cross the wrist. The TRL 3 calculations give about 448 finger cycles per hour at the design load, about 3.9 sessions of 60 min per charge and $281.90 in parts. Two requirements are not met (forearm pack mass, about 675 g against 450 g, and cuff contact pressure), and three are at risk; see the [sizing calculations](docs/04-calcs/01-sizing.md) and the [review note](docs/REVIEW.md).

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Two 25 mm 227:1 gearmotors with encoders, antagonistic spools and idlers
- Bowden sheaths and UHMWPE tendons, with breakaway couplings and a quick-release
- Fingerless glove, TPU finger cuffs, dorsal and palmar plates, thumb spacer
- Motor drivers with current sensing for force limiting
- ESP32-S3 controller, 2S Li-ion pack, emergency stop

The priced bill of materials is in [bom/bom.csv](bom/bom.csv). The parametric model is `cad/src/model.py` (STEP and STL in `cad/step` and `cad/stl`).

## Safety

> This is a research and educational prototype. It is not a medical device, has not been cleared or approved by any regulator, and must not be used to diagnose, treat or monitor any person.

> **Safety:** The device applies force to fingers that may be spastic or insensate, its gearboxes cannot be back-driven, and it carries a lithium-ion pack. See the safety section of the [design precis](docs/02-concept.md) before building or wearing anything.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (FXH-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `FXH-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
