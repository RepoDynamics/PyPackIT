"""Components for creating a GitHub README file in HTML."""
import copy

# Standard libraries
from typing import Optional, Sequence, Literal
import itertools
# Non-standard libraries
import pycolorit as pcit
import pybadgeit as bdg
import pyhtmlit as html
# Self
import pypackit as pkit
from pypackit.docs.readme import element


def menu(
        buttons: Sequence[dict[str, str]],
        align: str = 'center',
        width: Optional[dict[str, str]] = None,
        num_spaces: int = 1,
        button_defaults: Optional[dict] = None,
        gradient_colors: Optional[dict[Literal['dark', 'light'], tuple[str, str]]] = None,

) -> html.element.DIV:
    """
    Create a horizontal series of buttons, optionally sandwiched between two lines.

    Parameters
    ----------
    buttons
        A sequence of dictionaries, each describing one button, with the following keys:

        label : str
            The text on the button, which will also be used for its HTML element's 'alt' attribute.
        description : str
            A longer text to show when hovering on the button, i.e. the 'title' attribute of the HTML element.
        link : str
            Target path of the button, i.e. the 'href' attribute of its HTML <a> element.
    colors_dark
    colors_light
    height
    width
    num_spaces
    default_theme

    Returns
    -------

    """
    if not button_defaults:
        button_defaults = dict()
    grad_colors = {'dark': None, 'light': None}
    if gradient_colors:
        for theme, gradient in gradient_colors.items():
            if theme not in ('dark', 'light'):
                raise ValueError()
            if not isinstance(gradient, (list, tuple)) or len(gradient) != 2:
                raise ValueError()
            grad_colors[theme] = pcit.gradient.interpolate_rgb(
                pcit.hexa(gradient[0]),
                pcit.hexa(gradient[1]),
                count=len(buttons)
            ).rgb(as_str=True).tolist()

    badges = []
    for idx, button in enumerate(buttons):
        args = copy.deepcopy(button)
        if 'color' not in args:
            args['color'] = dict()
        if 'right' not in args['color']:
            args['color']['right'] = dict()
        if 'dark' not in args['color']['right']:
            if grad_colors['dark']:
                args['color']['right']['dark'] = grad_colors['dark'][idx]
        if 'light' not in args['color']['right']:
            if grad_colors['light']:
                args['color']['right']['light'] = grad_colors['light'][idx]
        badges.append(bdg.shields.static(**(button_defaults | args)))

    seperator = f"{'&nbsp;' * num_spaces}"
    menu_content = []
    if width and width.get('top'):
        menu_content.append(html.element.HR(width=width.get('top')))
    menu_content.append(
        seperator.join([str(badge.as_html_picture(tag_seperator='', content_indent='')) for badge in badges])
    )
    if width and width.get('bottom'):
        menu_content.append(html.element.HR(width=width.get('bottom')))
    return html.element.DIV(align=align, content=menu_content)



def connect(
        data: Sequence[
            tuple[
                Literal['website', 'email', 'linkedin', 'twitter', 'researchgate', 'gscholar', 'orcid'],
                str,
                str,
            ]
        ]
):
    config = {
        'website': {'label': 'Website', 'color': '21759B', 'logo': 'wordpress'},
        'email': {'label': 'Email', 'color': '8B89CC', 'logo': 'maildotru'},
        'linkedin': {'label': 'LinkedIn', 'color': '0A66C2', 'logo': 'linkedin'},
        'twitter': {'label': 'Twitter', 'color': '1DA1F2', 'logo': 'twitter'},
        'researchgate': {'label': 'ResearchGate', 'color': '00CCBB', 'logo': 'researchgate'},
        'gscholar': {'label': 'Google Scholar', 'color': '4285F4', 'logo': 'googlescholar'},
        'orcid': {'label': 'ORCID', 'color': 'A6CE39', 'logo': 'orcid'},
    }
    badges = []
    for id, display, url in data:
        conf = config.get(id)
        if conf is None:
            raise ValueError(f"Data item {id} not recognized.")
        badge = docs.badge.static(right_text=display)
        badge.left_text = conf['label']
        badge.right_color = conf['color']
        badge.logo = conf['logo']
        badge.a_href = url
        badges.append(badge)
    return badges
