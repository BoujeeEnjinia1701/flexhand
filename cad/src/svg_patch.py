"""Work-around for a build123d SVG export failure (reported as a kit problem, FXH-DDR-003 session).

build123d's ExportSVG raises AssertionError when a projected elliptical arc is so short that its
start and end points coincide (it happens on the swept sheaths and tendons). Such an arc is
invisible at drawing scale, so it is skipped, exactly as build123d already does for arcs shorter
than 1e-6. Imported by cad/src/sheets.py, concept_media.py and build_plan_media.py.
"""
import build123d.exporters as _ex

_orig = _ex.ExportSVG._ellipse_segments


def _safe_ellipse_segments(self, edge, reverse):
    try:
        return _orig(self, edge, reverse)
    except AssertionError:
        return []


_ex.ExportSVG._ellipse_segments = _safe_ellipse_segments
