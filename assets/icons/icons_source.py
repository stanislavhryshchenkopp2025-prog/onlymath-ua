import itertools as it
from typing import Callable

from manim import *


def svg_coords(coords: np.ndarray) -> str:
    return f"{coords[0]:.3f} {-coords[1]:.3f}"


def vmobject_to_paths_str(mob: VMobject) -> str:
    if mob.submobjects:
        return "\n".join(vmobject_to_paths_str(sub) for sub in mob.submobjects)
    
    if mob.points.size == 0:
        return ""
    
    path_parts = [f"M {svg_coords(mob.points[0])}"]
    path_parts.extend(
        f"C " + ", ".join(svg_coords(p) for p in (p1, p2, p3))
        for _, p1, p2, p3 in it.batched(mob.points, 4)
    )
    path_str = " ".join(path_parts)
    
    style = mob.get_style(simple=True)
    fill_hex = style["fill_color"].to_hex()
    stroke_hex = style["stroke_color"].to_hex()
    stroke_w = style["stroke_width"] / 100
    
    return (
        f'  <path d="{path_str}"\n'
        f'        stroke="{stroke_hex}" stroke-width="{stroke_w}" stroke-opacity="{style["stroke_opacity"]}"\n'
        f'        fill="{fill_hex}"   fill-opacity="{style["fill_opacity"]}" />'
    )


def export_to_svg(mobject: VMobject, filename: str = "export.svg") -> None:
    raw_paths = vmobject_to_paths_str(mobject)
    
    svg_document = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-7.11 -4 14.22 8">\n'
        f"{raw_paths}\n"
        f"</svg>\n"
    )
    
    with open(filename, "w") as f:
        f.write(svg_document)