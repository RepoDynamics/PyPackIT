"""Working with colors."""


# Non-standard libraries
import numpy as np
from pycolorit import rgb
from pycolorit.color import Color


def interpolate_rgb(
    color_start: tuple[int, int, int] | Color,
    color_end: tuple[int, int, int] | Color,
    count: int = 3,
) -> Color:
    """
    Create intermediate colors between two given RGB colors.

    Parameters
    ----------
    color_start : tuple[int, int, int]
        Initial RGB color.
    color_end : tuple[int, int, int], 0 <= int <= 255
        Final RGB color.
    count : int >= 0
        Total number of returned colors. The initial and final colors,
        which are always part of the gradient, are included, i.e.
        for example `count=1` returns `[color_start]`, `count=2` returns
        `[color_start, color_end]`, and `count=3` returns
        `[color_start, intermediate_color_1, color_end]`.

    Returns
    -------
    colors : numpy.ndarray, shape: (count, 3)
        RGB values starting with `color_start` and ending with `color_end`.
    """
    if not isinstance(count, int) or count <= 0:
        raise ValueError("count must be positive integer")
    c1 = (
        rgb(color_start).rgb()[0]
        if not isinstance(color_start, Color)
        else color_start.rgb()[0].astype(int)
    )
    c2 = (
        rgb(color_end).rgb()[0]
        if not isinstance(color_end, Color)
        else color_end.rgb()[0].astype(int)
    )
    if count == 1:
        return rgb(c1)
    if count == 2:
        return rgb([color_start, color_end])
    step = (c2 - c1) / (count - 1)
    colors = ((np.arange(count)[..., np.newaxis] * step) + c1[np.newaxis, ...]).astype(np.uint8)
    colors[-1] = c2
    return rgb(colors)
