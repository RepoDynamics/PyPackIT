
# Standard libraries
from typing import Optional, Literal
import datetime
from pathlib import Path
import copy
# Non-standard libraries
import pyhtmlit as html
import pylinks
import pybadgeit as bdg
import pycolorit as pcit
# Self
import pypackit
from pypackit.docs.readme import component, element
from pypackit.jsons import _JSONLoader


class ReadMe:

    def __init__(
            self,
            data: dict
    ):
        self.data = data
        self._github_repo_link_gen = pylinks.github.user(self.github['user']).repo(self.github['repo'])
        self._github_badges = bdg.shields.GitHub(
            user=self.github['user'], repo=self.github['repo'], branch=self.github['branch']
        )
        return

    def generate(self, output: Literal['str'] = 'str'):
        file_content = self.assemble_file()
        if output == 'str':
            return str(file_content)
        return file_content

    def assemble_file(self):
        return html.element.ElementCollection(
            elements=[
                html.element.Comment(f"{self.project_name} ReadMe File"),
                html.element.Comment(
                    f"Document automatically generated on "
                    f"{datetime.datetime.utcnow().strftime('%Y.%m.%d at %H:%M:%S UTC')} "
                    f"by PyPackIT {pypackit.__version__}"
                ),
                "\n",
                marker(start="Header", main=True),
                self.header(),
                "\n",
                marker(end="Header", main=True),
                "\n",
                marker(start="Body", main=True),
                "\n",
                self.body(),
                "\n",
                marker(end="Body", main=True),
                "\n",
                marker(start="Footer", main=True),
                "\n",
                self.footer(),
                "\n",
                marker(end="Footer", main=True),
                "\n",
            ]
        )

    def header(self):
        top_menu, bottom_menu = self.menu()
        return html.element.DIV(
            align="center",
            content=[
                marker(start='Logo'),
                self.logo(),
                marker(end='Logo'),
                marker(start='Top Panel'),
                top_menu,
                marker(end='Top Panel'),
                marker(start='Description'),
                element.paragraph(**self.data['header']['paragraph']),
                marker(end='Description'),
                marker(start='Bottom Panel'),
                bottom_menu,
                marker(end='Bottom Panel')
            ]
        )

    def body(self):
        data = self.data['body']
        return html.element.DIV(
            content=[getattr(self, f'{section["id"]}')(section) for section in data]
        )

    def footer(self):
        """
        """
        project_badge = self.project_badge()
        project_badge.align = "left"
        copyright_badge = self.copyright_badge()
        copyright_badge.align = "left"
        license_badge = self.license_badge()
        license_badge.align = "right"
        pypackit_badge = element.pypackit_badge()
        pypackit_badge.align = "right"
        elements = html.element.DIV(
            content=[
                html.element.HR(),
                marker(start='Left Side'),
                project_badge,
                copyright_badge,
                marker(end='Left Side'),
                marker(start='Right Side'),
                pypackit_badge,
                license_badge,
                marker(end='Right Side')
            ]
        )
        return elements

    def logo(self):
        data = copy.deepcopy(self.data['header']['logo'])
        data['src']['dark'] = self.resolve_link(link=data['src']['dark'], raw=True)
        data['src']['light'] = self.resolve_link(link=data['src']['light'], raw=True)
        data['link'] = self.resolve_link(link=data['link'], raw=False)
        data['align'] = 'center' if self.data['header']['style'] == 'wide_logo' else 'left'
        logo = element.logo(**data)
        if self.data['header']['style'] == 'tall_logo':
            logo.content.elements.append(self.spacer(width="10px", height=data['height'], align="left"))
        return logo

    def menu(self):
        top = copy.deepcopy(self.data['header']['top_menu'])
        bottom = copy.deepcopy(self.data['header']['bottom_menu'])
        if 'gradient_colors' in top and 'gradient_colors' in bottom:
            for theme in ('dark', 'light'):
                if (
                        theme in top['gradient_colors'] and top['gradient_colors'][theme][1] is None and
                        theme in bottom['gradient_colors'] and bottom['gradient_colors'][theme][0] is None
                ):
                    grad_colors = pcit.gradient.interpolate_rgb(
                        color_start=pcit.color.hexa(top['gradient_colors'][theme][0]),
                        color_end=pcit.color.hexa(bottom['gradient_colors'][theme][1]),
                        count=len(top['buttons']) + len(bottom['buttons'])
                    ).hex()
                    top['gradient_colors'][theme][1] = grad_colors[len(top['buttons']) - 1]
                    bottom['gradient_colors'][theme][0] = grad_colors[len(top['buttons'])]
        if self.data['header']['style'] == 'tall_logo':
            top.pop("width", None)
        top_menu = component.menu(**top)
        if self.data['header']['style'] == 'tall_logo':
            top_menu.content.elements.append("<br><br>")
        bottom_menu = component.menu(**bottom)
        return top_menu, bottom_menu

    def continuous_integration(self, data):

        def github(filename, **kwargs):
            badge = self._github_badges.workflow_status(
                filename=filename,
                **kwargs
            )
            return badge

        def readthedocs(rtd_name, rtd_version=None, **kwargs):
            badge = bdg.shields.build_read_the_docs(
                project=rtd_name,
                version=rtd_version,
                **kwargs
            )
            return badge

        def codecov(**kwargs):
            badge = bdg.shields.coverage_codecov(
                user=self.github['user'],
                repo=self.github['repo'],
                branch=self.github['branch'],
                **kwargs
            )
            return badge

        func_map = {'github': github, 'readthedocs': readthedocs, 'codecov': codecov}

        badges = []
        for test in copy.deepcopy(data['args']['tests']):
            func = test.pop('type')
            if 'style' in test:
                style = test.pop('style')
                test = style | test
            badges.append(func_map[func](**test))

        div = html.element.DIV(
            align=data.get('align') or 'center',
            content=[
                marker(start="Continuous Integration"),
                self.heading(data=data['heading']),
                *badges,
                marker(end="Continuous Integration")
            ]
        )
        return div

    def activity(self, data):

        pr_button = bdg.shields.static(text="Pull Requests", style="for-the-badge", color='444')

        prs = []
        issues = []
        for label in (None, "bug", "enhancement", "documentation"):
            prs.append(self._github_badges.pr_issue(label=label, raw=True, logo=None))
            issues.append(self._github_badges.pr_issue(label=label, raw=True, pr=False, logo=None))

        prs_div = html.element.DIV(
            align="right",
            content=html.element.ElementCollection(prs, "\n<br>\n")
        )
        iss_div = html.element.DIV(
            align="right",
            content=html.element.ElementCollection(issues, "\n<br>\n")
        )


        table = html.element.TABLE(
            content=[
                html.element.TR(
                    content=[
                        html.element.TD(
                            content=html.element.ElementCollection(
                                [
                                    pr_button,
                                    *prs
                                ],
                                seperator="<br>"
                            ),
                            align="center",
                            valign="top",
                        ),
                        html.element.TD(
                            content=html.element.ElementCollection(
                                [
                                    bdg.shields.static(text="Milestones", style='for-the-badge', color='444'),
                                    self._github_badges.milestones(state='both', style="flat-square", logo=None, text="Total"),
                                    "<br>",
                                    bdg.shields.static(text="Commits", style='for-the-badge',
                                                       color='444'),
                                    self._github_badges.last_commit(logo=None),
                                    self._github_badges.commits_since(logo=None),
                                    self._github_badges.commit_activity()
                                ],
                                seperator="<br>"
                            ),
                            align="center",
                            valign="top",
                        ),
                        html.element.TD(
                            content=html.element.ElementCollection(
                                [
                                    bdg.shields.static(text="Issues", style='for-the-badge', logo='github',
                                                       color='444'),
                                    *issues
                                ],
                                seperator="<br>"
                            ),
                            align="center",
                            valign="top",
                        ),
                    ]
                )
            ]
        )

        div = html.element.DIV(
            align=data.get('align') or 'center',
            content=[
                marker(start="Activity"),
                self.heading(data=data['heading']),
                table,
                marker(end="Activity")
            ]
        )
        return div



    def project_badge(self):

        data = self.data['footer']['package_badge']
        badge = self._github_badges.release_version(
            display_name='release',
            include_pre_release=True,
            text=self.project_name,
            style='for-the-badge',
            link=data['link'],
            logo=data['logo'],
        )

        badge.right_color = data['color']
        return badge

    def copyright_badge(self):
        data = self.data['footer']['copyright_badge']
        right_text = (
            f"{data['first_release_year']}–{datetime.date.today().year} "
            if data['first_release_year'] != datetime.date.today().year else
            f"{data['first_release_year']} "
        ) + data['owner']
        badge = bdg.shields.static(
            text={"left": 'Copyright', "right": right_text},
            style='for-the-badge',
            color="AF1F10"
        )
        return badge

    def license_badge(self):
        data = self.data['footer']['license_badge']
        badge = self._github_badges.license(
            filename=data['license_path'],
            style="for-the-badge",
            color={'right': "AF1F10"}
        )
        return badge

    def heading(self, data):
        data = copy.deepcopy(data)
        if 'button' in data:
            if 'style' in data['button']:
                style = data['button'].pop('style')
                args = style | data['button']
            heading = bdg.shields.static(**args)
            return html.element.H(1, content=[heading])
        return

    @property
    def project_name(self):
        return self.data['globals']['project_name']

    @property
    def github(self):
        return self.data['globals']['github']

    def github_link_gen(self, branch: bool = False):
        if branch:
            return self._github_repo_link_gen.branch(self.github['branch'])
        return self._github_repo_link_gen


    def resolve_link(self, link: str, raw: bool = False):
        if link.startswith(('http://', 'https://', 'ftp://')):
            return link
        return self.github_link_gen(branch=True).file(link, raw=raw)


    def spacer(self, **args):
        spacer = html.element.IMG(
            src='docs/source/_static/img/spacer.svg',
            **args,
        )
        return spacer



def marker(start=None, end=None, main: bool = False):
    if start and end:
        raise ValueError("Only one of `start` or `end` must be provided, not both.")
    if not (start or end):
        raise ValueError("At least one of `start` or `end` must be provided.")
    tag = 'START' if start else 'END'
    section = start if start else end
    delim = '-' * (40 if main else 25)
    return html.element.Comment(f"{delim} {tag} : {section} {delim}")


def from_file(filepath):
    data = _JSONLoader(filepath=filepath).fill()
    return ReadMe(data)