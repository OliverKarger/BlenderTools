from typing import Sequence, Tuple


def to_rgba(color: Sequence[float]) -> Tuple[float, float, float, float]:
    """
    Normalize input to an RGBA tuple with 4 floats.
    Accepts RGB or RGBA, trims extra channels, pads missing alpha with 1.0.
    """
    r, g, b = color[:3]
    a = color[3] if len(color) > 3 else 1.0
    return (r, g, b, a)
