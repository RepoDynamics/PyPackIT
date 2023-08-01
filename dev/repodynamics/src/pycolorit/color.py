# Standard libraries
from typing import Literal, Sequence

# Non-standard libraries
import jax
import jax.numpy as jnp
import numpy as np


class Color:
    def __init__(self, values: np.ndarray):
        self._values = values
        return

    def rgb(
        self,
        unit: Literal["int", "percent", "fraction"] = "int",
        as_str: bool = False,
        with_comma: bool = True,
    ) -> np.ndarray:
        rgb_colors = self._values
        sep = ", " if with_comma else " "
        if unit == "int":
            if not as_str:
                return rgb_colors
            return np.array([f"rgb({sep.join(color)})" for color in rgb_colors.astype(str)])
        rgb_colors_norm = rgb_colors / 255
        if unit == "percent":
            rgb_colors_norm *= 100
        if not as_str:
            return rgb_colors_norm
        return np.array(
            [
                f"rgb({sep.join(color)})"
                for color in np.char.mod("%.1f%%" if unit == "percent" else "%.1f", rgb_colors_norm)
            ]
        )

    def hex(
        self,
        with_hash: bool = False,
    ):
        sep = "#" if with_hash else ""
        return np.array([f"{sep}{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}" for rgb in self._values])

    @property
    def hsl(self):
        return _rgb_to_hsl(rgb=self._values)


def rgb(values: tuple[int, int, int] | Sequence[tuple[int, int, int]]):
    colors = np.asarray(values)
    if not np.issubdtype(colors.dtype, np.integer):
        raise ValueError(
            f"`values` must be a sequence of integers, but found elements with type {colors.dtype}"
        )
    if np.any(np.logical_or(colors < 0, colors > 255)):
        raise ValueError("`values` must be in the range [0, 255].")
    colors = colors.astype(np.ubyte)
    if colors.ndim > 2 or colors.shape[-1] != 3:
        raise ValueError(
            f"`values` must either have a shape of (3, ) or (n, 3). The input shape was {colors.shape}"
        )
    colors = colors[np.newaxis] if colors.ndim == 1 else colors
    return Color(values=colors)


def hexa(values: str | Sequence[str]) -> Color:
    def process_single_hex(val: str) -> tuple[int, int, int]:
        if len(val) == 3:
            val = "".join([d * 2 for d in val])
        elif len(val) != 6:
            raise ValueError(f"Hex color '{val}' not recognized.")
        return tuple(int(val[i : i + 2], 16) for i in range(0, 5, 2))

    colors = np.asarray(values)
    if not np.issubdtype(colors.dtype, np.str_):
        raise ValueError(
            f"`values` must be a sequence of strings, but found elements with type {colors.dtype}"
        )
    if colors.ndim == 0:
        colors = colors[np.newaxis]
    elif colors.ndim > 1:
        raise ValueError(
            f"`values` must either be a string, or a 1-dimensional sequence. The input dimension was {colors.ndim}"
        )
    colors = np.char.lstrip(colors, "#")
    colors_rgb = np.empty(shape=(colors.size, 3), dtype=np.ubyte)
    for i, color in enumerate(colors):
        colors_rgb[i] = process_single_hex(color)
    return Color(values=colors_rgb)


@jax.jit
def _rgb_to_hsl(rgb: jax.Array):
    """
    Calculate HSL values from RGB values.

    Parameters
    ----------
    rgb : jax.Array, shape: (3, ) or (n, 3)
        Array of RGB values, for either one color, or a series of colors.

    Returns
    -------
    hsl_colors : jax.Array
        Array of HSL values with the same shape as `colors`.
    """
    norm = rgb / 255
    rs, gs, bs = norm[..., 0], norm[..., 1], norm[..., 2]
    max_val = jnp.max(norm, axis=-1)  # max(r, g, b) for each color
    min_val = jnp.min(norm, axis=-1)  # min(r, g, b) for each color
    minmax_sum = max_val + min_val
    minmax_dist = max_val - min_val
    # Calculate all 'L' values.
    hsl_l = minmax_sum / 2
    # For cases where max and min values are not the same,
    #   'H' and 'S' values are non-zero and must be calculated.
    # Calculate all 'S' values.
    # Here conditioning on `minmax_dist == 0` is not necessary, since the numerator is `minmax_dist`
    hsl_s = jnp.where(hsl_l > 0.5, minmax_dist / (2 - minmax_sum), minmax_dist / minmax_sum)
    # Calculate all 'H' values.
    hsl_h = (
        jnp.where(
            minmax_dist == 0,
            0,
            jnp.where(
                max_val == rs,
                jnp.where(gs < bs, 6, 0) + (gs - bs) / minmax_dist,
                jnp.where(max_val == gs, (bs - rs) / minmax_dist + 2, (rs - gs) / minmax_dist + 4),
            ),
        )
        / 6
    )
    return jnp.stack([hsl_h, hsl_s, hsl_l], axis=-1) * 100
