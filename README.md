# FlexHand

**Area:** BioMedical · **Status:** Concept · **Prototype budget:** about $500 USD · **Difficulty:** 4 of 5

Soft-actuated finger exoskeleton for continuous passive motion, driven by tendons from a wrist-mounted motor pack.

## Problem

Post-stroke hand rehab needs many repetitions, but therapist time is limited.

## Concept

Soft-actuated finger exoskeleton for continuous passive motion, driven by tendons from a wrist-mounted motor pack.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Micro servos or N20 gear motors (2)
- Bowden cable
- TPU finger cuffs
- Current sensing
- Controller

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> This is a research and educational prototype. It is not a medical device, has not been cleared or approved by any regulator, and must not be used to diagnose, treat or monitor any person.

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
