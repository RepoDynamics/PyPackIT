# Standard libraries
from typing import Optional, Sequence, Literal
import itertools
# Non-standard libraries
import pycolorit as pcit
import pybadgeit as bdg
import pyhtmlit as html
import pylinks as plinks
# Self
import pypackit as pkit


def logo(
        src: dict[Literal['dark', 'light'], str],
        link: Optional = "",
        width: Optional[str] = '80%',
        height: Optional[str] = None,
        align: Optional[Literal['left', 'right']] = None,
        alt: Optional[str] = None,
        title: Optional[str] = None,
        default_theme: Literal['dark', 'light'] = 'light',
) -> html.Element:
    """
    Create an HTML <picture> element for the logo, and optionally wrap it inside an anchor.

    Parameters
    ----------
    src_dark : has_str
        Path to the dark-themed logo. This can be a URL or a local path.
        Any object that implements a __str__ method is accepted.
    src_light : has_str
        Path to the light-themed logo. This can be a URL or a local path.
        Any object that implements a __str__ method is accepted.
    link : has_str
    width
    alt
    title

    Returns
    -------

    """
    picture_tag = html.element.PICTURE(
        img=html.element.IMG(
            src=src[default_theme],
            alt=alt,
            title=title,
            width=width,
            height=height,
            align=align
        ),
        sources=[
            html.element.SOURCE(media='(prefers-color-scheme: dark)', srcset=src['dark']),
            html.element.SOURCE(media='(prefers-color-scheme: light)', srcset=src['light']),
        ]
    )
    return html.element.A(href=link, content=[picture_tag]) if link else picture_tag


def paragraph(
        text: str,
        align: Optional[str] = 'justify',
        word_styles: dict[str, dict[str, str | bool]] = None,
) -> html.element.P:
    """
    Project description paragraph.

    Parameters
    ----------
    text : str
        Project description.
    align : str, default: 'justify'
        Text alignment of the description paragraph.
    word_styles : dict, optional
        A dictionary of words and corresponding styles.
        Each key in the dictionary must be a word as appears in text, and the corresponding value
        must be a dictionary with any of the following key-value pairs:

        bold : bool, default: False
            Make the word bold.
        italic : bool, default: False
            Make the word italic.
        link : str
            Link the word to a path.

    Returns
    -------
    project_description : pyhtmlit.element.P
    """
    return html.element.P(align=align, content=[text]).style(word_styles)


def pypackit_badge():
    return bdg.shields.static(
        text={'left': 'Template', "right": f'PyPackIT {pkit.__version__}'},
        style='for-the-badge',
        color={'right': 'rgb(0, 100, 0)'},
        logo=(
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsPAAALDwGS"
            "+QOlAAADxklEQVRYhb1XbWxTZRR+3vvR3rt+OsJ2M5CWrKIxZJsm/gITk0XBjYQ4IJshAcJHjIq4HyyKgjJBPiLqwg"
            "8Tk6L80qATgwkLGpUE94OYSBgSIZnTFoK93VxhpV1v73s/TGu6rOu69nZlz6/zvue85zw55z73vZeYpgkraDr85IX7"
            "NLEGFHDrrtDQ8d+WW0owA4yV4LVH2juHyV9rQuYthPQwrqnX/U/3PHNswQhEmbFNCpS8vZgWW71gBFJECRQkIMyK+R"
            "DgZtvsOtV2Om5OBmomPZv795wLz/RLpB5gTMiIImEkF8+HQEEHXvr0xdXjzsjWO67QqiSX6J3uSyPdLEDAI2jc9Tj7"
            "2AGBCPOpnUVBB1Re6UrZkvDEa5HkkgXzlcw6XOr9OZixl/esOATDmopKEtBZKi2JBX7VVTIa4aLr5pW9DBSMQGPVAA"
            "Fu1FDXTw+6eAazqsCpeK+WOti6/zmfYiqlwkpiVhWUAzuxvyDrUfixbM7oXR+s7055wttEkcDBi1yN/lD7kc3np5RV"
            "MYHZsHbP853/mndes4mGkxe1gCDCwTvTgGMMuosBXATC3eaMsrbljlt6ETFgksV8ra8/6/t94npwOHVzVZgON8tmyD"
            "HO3kKCG82L073y1oNft/sqIsCD/7OYTzXUlyNKxFkqh+4eAwjeya2rNoIJbaKl3FhTTKx/v7+jlVXcgqUOzAXVoFK5"
            "sWTS2ff2xrN+tvbuxgICJjGn2iiL/2DDhx3d5SQ1YJRsfwbcmC96cNP5wxm7p+3cYHYE+z7f0UkpWpL2+EqGZRqDr3"
            "7Rt+VkV1mFc6AGbcyYdTYp4bM1fGMngKAxUKm8wcRolhyj2cHG607nEXo3+IqZXirjnn0c96kKQZa+t1J4Jlyse+TH"
            "45enZLbjRFuQ3Fv2BhB7SkiJV492/vBmHoHenZ+QfZ/t7PZwHkmkWEx14z0rBUNqGG171xXt1qm9A4MABov5syM4uj"
            "3YZ6VoNVE1FVSKigkY0CO5D5IbqZsfy+lo1nawjpIX2XRUTODCoYEzEluftUNKGIpR2c1Y9RGwhEssGAE7sQ1NXwus"
            "ADfr+WXBCHgZb568logN0e9ODJypKoEYH5u6ZDRoEg9+JLe+fGxwd5OwMuQXfPCLPjQIDfutFM+g5G14W7jd0XTyiR"
            "ZCWc8I+3f9ozQgT/cPfXTlwfwbUkb9tja9CHFuwjVsH2m+ZvvDn9m3gZeLnakqgS93nw07NFf+Q2YK8Jre/moSmHME"
            "Ts351lL94a+SuupQqY46bdHFSwf+/ympCgD8BxQORGJUan2aAAAAAElFTkSuQmCC"
        ),
        alt='Template by PyPackIT',
        title=f'Project template created by PyPackIT version {pkit.__version__}.',
        link='https://pypackit.readthedocs.io'
    )
