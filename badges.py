from typing import Literal, Tuple, Sequence
import urllib
import numpy as np


def static_badge(
        left_text: str = "",
        left_color: str = None,
        right_text: str = " ",
        right_color: str = None,
        style: Literal['plastic', 'flat', 'flat-square', 'for-the-badge', 'social'] = None,
        logo: str = None,
        logo_color: str = None,
        logo_width: float = None,
        cache_time: int = None,
        output_html: bool = True,
        link: str = None,
        title: str = None,
):
    """

    Parameters
    ----------
    left_text : str
        The left text. Pass an empty string (default) to omit the left side.
    left_color : str
    logo : str
    right_text : str
        The right text. Can't be empty.
    right_color : str
        The right color. Supports the eight named colors above,
        as well as hex, rgb, rgba, hsl, hsla and css named colors.
    logo_color
    style
    cache_time
    logo_width

    Returns
    -------

    """
    base_url = (
        f"https://img.shields.io/static/v1?"
        f"label={urllib.parse.quote(left_text, safe='')}"
        f"&message={urllib.parse.quote(right_text, safe='')}"
    )
    if right_color:
        base_url += f"&color={right_color.replace(' ', '')}"
    if left_color:
        base_url += f"&labelColor={right_color.replace(' ', '')}"
    if style:
        base_url += f"&style={style}"
    if logo:
        base_url += f"&logo={logo}"
    if logo_color:
        base_url += f"&logoColor={logo_color.replace(' ', '')}"
    if logo_width:
        base_url += f"&logoWidth={logo_width}"
    if cache_time:
        base_url += f"&cacheSeconds={cache_time}"
    alt_text = left_text if left_text else right_text
    if output_html:
        img_tag = (
            f'<img alt="{alt_text}" '
            f'title="{title if title else alt_text.capitalize()}" '
            f'src="{base_url}">'
        )
        if not link:
            return img_tag
        return f'<a href="{link}">{img_tag}</a>'
    img_tag = f'![{alt_text}]({base_url})'
    if not link:
        return img_tag
    return f'[{img_tag}]({link})'


def create_rgb_color_gradient(
        color_start: Tuple[int, int, int],
        color_end: Tuple[int, int, int],
        count: int = 3
):
    if not isinstance(count, int) or count <= 0:
        raise ValueError("count must be positive integer")
    if count == 1:
        return color_start
    if count == 2:
        return color_start, color_end
    c1 = np.asarray(color_start, dtype=np.uint8)
    c2 = np.asarray(color_end, dtype=np.uint8)
    step = (c2 - c1) / (count - 1)
    colors = ((np.arange(count)[...,np.newaxis] * step) + c1[np.newaxis, ...]).astype(np.uint8)
    colors[-1] = c2
    return colors


def create_main_buttons(
        data: Sequence[Tuple[str, str]] = (
            ("HOME", None, "Homepage"),
            ("INTRO", None)
        ),
        color_start: Tuple[int, int, int] = (100, 100, 100),
        color_end: Tuple[int, int, int] = None,
        num_spaces: int = 1,
        output_html: bool = True,
):
    if color_end:
        colors = create_rgb_color_gradient(color_start=color_start, color_end=color_end, count=len(data))
    buttons = [
        static_badge(
            right_text=button_name,
            right_color=str(tuple(colors[i])) if color_end else str(tuple(color_start)),
            style='for-the-badge',
            output_html=output_html,
            link=button_link,
        ) for i, (button_name, button_link) in enumerate(data)
    ]
    return ('&nbsp;' * num_spaces).join(buttons)

