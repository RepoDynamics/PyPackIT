# Standard libraries
import copy
import datetime
import itertools
import re
from pathlib import Path
from typing import Literal, Optional, Sequence

# Non-standard libraries
import pybadgeit as bdg
import pycolorit as pcit
import markitup as html
import pylinks
import pypackit


class ReadMe:
    def __init__(self, metadata: dict):
        self._metadata = metadata
        # self._github_repo_link_gen = pylinks.github.user(self.github["user"]).repo(
        #     self.github["repo"]
        # )
        # self._github_badges = bdg.shields.GitHub(
        #     user=self.github["user"],
        #     repo=self.github["repo"],
        #     branch=self.github["branch"],
        # )
        return

    def generate(self) -> html.element.ElementCollection:
        file_content = html.element.ElementCollection(
            elements=[
                html.element.Comment(f"{self._metadata['project']['name']} ReadMe File"),
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
        return file_content

    def header(self):
        top_menu, bottom_menu = self.menu()
        return html.element.DIV(
            align="center",
            content=[
                marker(start="Logo"),
                self.logo(),
                marker(end="Logo"),
                marker(start="Top Panel"),
                top_menu,
                marker(end="Top Panel"),
                marker(start="Description"),
                *self.header_body(),
                marker(end="Description"),
                marker(start="Bottom Panel"),
                bottom_menu,
                marker(end="Bottom Panel"),
            ],
        )

    def body(self):
        data = self._metadata["body"]
        return html.element.DIV(
            content=[getattr(self, f'{section["id"]}')(section) for section in data]
        )

    def footer(self):
        """ """
        project_badge = self.project_badge()
        project_badge.align = "left"
        copyright_badge = self.copyright_badge()
        copyright_badge.align = "left"
        license_badge = self.license_badge()
        license_badge.align = "right"
        pypackit_badge_ = pypackit_badge()
        pypackit_badge_.align = "right"
        elements = html.element.DIV(
            content=[
                html.element.HR(),
                marker(start="Left Side"),
                project_badge,
                copyright_badge,
                marker(end="Left Side"),
                marker(start="Right Side"),
                pypackit_badge,
                license_badge,
                marker(end="Right Side"),
            ]
        )
        return elements

    def logo(self) -> html.element.A:
        style = self._metadata["readme"]["header"]["style"]
        url = f"{self._metadata['url']['website']['base']}" + "/_static/logo/full_{}.svg"
        picture_tag = html.element.PICTURE(
            img=html.element.IMG(
                src=url.format("light"),
                alt=f"{self._metadata['project']['name']}: {self._metadata['project']['tagline']}",
                title=f"Welcome to {self._metadata['project']['name']}! Click to visit our website and learn more.",
                width="80%" if style == "vertical" else "auto",
                height="300px" if style == "horizontal" else "auto",
                align="center" if style == "vertical" else "left",
            ),
            sources=[
                html.element.SOURCE(
                    media=f"(prefers-color-scheme: {theme})", srcset=url.format(theme)
                )
                for theme in ("dark", "light")
            ],
        )
        logo = html.element.A(href=self._metadata["url"]["website"]["home"], content=[picture_tag])
        if self._metadata["readme"]["header"]["style"] == "horizontal":
            logo.content.elements.append(self.spacer(width="10px", height="300px", align="left"))
        return logo

    def header_body(self):
        description = html.element.P(
            align="justify", content=[self._metadata["project"]["description"]]
        ).style(
            {
                self._metadata["project"]["name"]: {
                    "bold": True,
                    "italic": True,
                    "link": self._metadata["url"]["website"]["home"],
                }
            }
        )
        content = [description]
        for key_point in self._metadata["project"]["key_points"]:
            content.extend(
                [
                    # self.spacer(width="10%", align="left"),
                    # self.spacer(width="10%", align="right"),
                    self.button(text=key_point["title"], color="primary"),
                    html.element.P(align="justify", content=[key_point["description"]]),
                ]
            )
        return content

    def menu(self):
        def get_top_data():
            with open(path_docs / "index.md") as f:
                text = f.read()
            toctree = re.findall(r":::{toctree}\s((.|\s)*?)\s:::", text, re.DOTALL)[0][0]
            top_section_filenames = [
                entry for entry in toctree.splitlines() if not entry.startswith(":")
            ]
            top_section_names = []
            for filename in top_section_filenames:
                with open((path_docs / filename).with_suffix(".md")) as f:
                    text = f.read()
                top_section_names.append(re.findall(r"^# (.*)", text, re.MULTILINE)[0])
            return [
                {"text": text, "link": str(Path(link).with_suffix(""))}
                for text, link in zip(top_section_names, top_section_filenames)
            ]

        def get_bottom_data():
            return [
                {"text": item["title"], "link": item["path"]}
                for group in self._metadata["website"]["quicklinks"]
                for item in group
                if item.get("include_in_readme")
            ]

        path_docs = Path(self._metadata["path"]["abs"]["docs"]["website"]["source"])
        top_data = get_top_data()
        bottom_data = get_bottom_data()
        colors = [
            pcit.gradient.interpolate_rgb(
                color_start=pcit.color.hexa(self._metadata["theme"]["color"]["primary"][theme]),
                color_end=pcit.color.hexa(self._metadata["theme"]["color"]["secondary"][theme]),
                count=len(top_data) + len(bottom_data),
            ).hex()
            for theme in ("light", "dark")
        ]
        buttons = [
            self.button(
                text=data["text"],
                color=(color_light, color_dark),
                link=f"{self._metadata['url']['website']['home']}/{data['link']}",
            )
            for data, color_light, color_dark in zip(top_data + bottom_data, colors[0], colors[1])
        ]
        menu_top, menu_bottom = [
            html.element.DIV(
                align="center",
                content=[
                    ("&nbsp;" * 2).join(
                        [
                            str(badge.as_html_picture(tag_seperator="", content_indent=""))
                            for badge in badges
                        ]
                    )
                ],
            )
            for badges in (buttons[: len(top_data)], buttons[len(top_data) :])
        ]
        menu_bottom.content.elements.insert(0, html.element.HR(width="100%"))
        menu_bottom.content.elements.append(html.element.HR(width="80%"))
        if self._metadata["readme"]["header"]["style"] == "vertical":
            menu_top.content.elements.insert(0, html.element.HR(width="80%"))
            menu_top.content.elements.append(html.element.HR(width="100%"))
        else:
            menu_top.content.elements.append("<br><br>")
        return menu_top, menu_bottom

    def continuous_integration(self, data):
        def github(filename, **kwargs):
            badge = self._github_badges.workflow_status(filename=filename, **kwargs)
            return badge

        def readthedocs(rtd_name, rtd_version=None, **kwargs):
            badge = bdg.shields.build_read_the_docs(project=rtd_name, version=rtd_version, **kwargs)
            return badge

        def codecov(**kwargs):
            badge = bdg.shields.coverage_codecov(
                user=self.github["user"],
                repo=self.github["repo"],
                branch=self.github["branch"],
                **kwargs,
            )
            return badge

        func_map = {"github": github, "readthedocs": readthedocs, "codecov": codecov}

        badges = []
        for test in copy.deepcopy(data["args"]["tests"]):
            func = test.pop("type")
            if "style" in test:
                style = test.pop("style")
                test = style | test
            badges.append(func_map[func](**test))

        div = html.element.DIV(
            align=data.get("align") or "center",
            content=[
                marker(start="Continuous Integration"),
                self.heading(data=data["heading"]),
                *badges,
                marker(end="Continuous Integration"),
            ],
        )
        return div

    def activity(self, data):
        pr_button = bdg.shields.static(text="Pull Requests", style="for-the-badge", color="444")

        prs = []
        issues = []
        for label in (None, "bug", "enhancement", "documentation"):
            prs.append(self._github_badges.pr_issue(label=label, raw=True, logo=None))
            issues.append(self._github_badges.pr_issue(label=label, raw=True, pr=False, logo=None))

        prs_div = html.element.DIV(
            align="right", content=html.element.ElementCollection(prs, "\n<br>\n")
        )
        iss_div = html.element.DIV(
            align="right", content=html.element.ElementCollection(issues, "\n<br>\n")
        )

        table = html.element.TABLE(
            content=[
                html.element.TR(
                    content=[
                        html.element.TD(
                            content=html.element.ElementCollection(
                                [pr_button, *prs], seperator="<br>"
                            ),
                            align="center",
                            valign="top",
                        ),
                        html.element.TD(
                            content=html.element.ElementCollection(
                                [
                                    bdg.shields.static(
                                        text="Milestones",
                                        style="for-the-badge",
                                        color="444",
                                    ),
                                    self._github_badges.milestones(
                                        state="both",
                                        style="flat-square",
                                        logo=None,
                                        text="Total",
                                    ),
                                    "<br>",
                                    bdg.shields.static(
                                        text="Commits",
                                        style="for-the-badge",
                                        color="444",
                                    ),
                                    self._github_badges.last_commit(logo=None),
                                    self._github_badges.commits_since(logo=None),
                                    self._github_badges.commit_activity(),
                                ],
                                seperator="<br>",
                            ),
                            align="center",
                            valign="top",
                        ),
                        html.element.TD(
                            content=html.element.ElementCollection(
                                [
                                    bdg.shields.static(
                                        text="Issues",
                                        style="for-the-badge",
                                        logo="github",
                                        color="444",
                                    ),
                                    *issues,
                                ],
                                seperator="<br>",
                            ),
                            align="center",
                            valign="top",
                        ),
                    ]
                )
            ]
        )

        div = html.element.DIV(
            align=data.get("align") or "center",
            content=[
                marker(start="Activity"),
                self.heading(data=data["heading"]),
                table,
                marker(end="Activity"),
            ],
        )
        return div

    def project_badge(self):
        data = self._metadata["footer"]["package_badge"]
        badge = self._github_badges.release_version(
            display_name="release",
            include_pre_release=True,
            text=self._metadata["project"]["name"],
            style="for-the-badge",
            link=data["link"],
            logo=data["logo"],
        )

        badge.right_color = data["color"]
        return badge

    def copyright_badge(self):
        data = self._metadata["footer"]["copyright_badge"]
        right_text = (
            f"{data['first_release_year']}–{datetime.date.today().year} "
            if data["first_release_year"] != datetime.date.today().year
            else f"{data['first_release_year']} "
        ) + data["owner"]
        badge = bdg.shields.static(
            text={"left": "Copyright", "right": right_text},
            style="for-the-badge",
            color="AF1F10",
        )
        return badge

    def license_badge(self):
        data = self._metadata["footer"]["license_badge"]
        badge = self._github_badges.license(
            filename=data["license_path"],
            style="for-the-badge",
            color={"right": "AF1F10"},
        )
        return badge

    def button(
        self,
        text: str,
        color: Literal["primary", "secondary"] | tuple[str, str],
        link: Optional[str] = None,
        title: Optional[str] = None,
    ):
        return bdg.shields.static(
            text=text,
            style="for-the-badge",
            color={
                theme: (
                    self._metadata["theme"]["color"][color][theme]
                    if isinstance(color, str)
                    else color[idx]
                )
                for idx, theme in enumerate(("light", "dark"))
            },
            alt=text,
            title=title or text,
            height="35px",
            link=link,
        )

    @property
    def github(self):
        return self._metadata["globals"]["github"]

    def github_link_gen(self, branch: bool = False):
        if branch:
            return self._github_repo_link_gen.branch(self.github["branch"])
        return self._github_repo_link_gen

    def resolve_link(self, link: str, raw: bool = False):
        if link.startswith(("http://", "https://", "ftp://")):
            return link
        return self.github_link_gen(branch=True).file(link, raw=raw)

    def spacer(self, **args):
        spacer = html.element.IMG(
            src="docs/source/_static/img/spacer.svg",
            **args,
        )
        return spacer


def marker(start=None, end=None, main: bool = False):
    if start and end:
        raise ValueError("Only one of `start` or `end` must be provided, not both.")
    if not (start or end):
        raise ValueError("At least one of `start` or `end` must be provided.")
    tag = "START" if start else "END"
    section = start if start else end
    delim = "-" * (40 if main else 25)
    return html.element.Comment(f"{delim} {tag} : {section} {delim}")


"""Components for creating a GitHub README file in HTML."""


def connect(
    data: Sequence[
        tuple[
            Literal[
                "website",
                "email",
                "linkedin",
                "twitter",
                "researchgate",
                "gscholar",
                "orcid",
            ],
            str,
            str,
        ]
    ]
):
    config = {
        "website": {"label": "Website", "color": "21759B", "logo": "wordpress"},
        "email": {"label": "Email", "color": "8B89CC", "logo": "maildotru"},
        "linkedin": {"label": "LinkedIn", "color": "0A66C2", "logo": "linkedin"},
        "twitter": {"label": "Twitter", "color": "1DA1F2", "logo": "twitter"},
        "researchgate": {"label": "ResearchGate", "color": "00CCBB", "logo": "researchgate"},
        "gscholar": {"label": "Google Scholar", "color": "4285F4", "logo": "googlescholar"},
        "orcid": {"label": "ORCID", "color": "A6CE39", "logo": "orcid"},
    }
    badges = []
    for id, display, url in data:
        conf = config.get(id)
        if conf is None:
            raise ValueError(f"Data item {id} not recognized.")
        badge = bdg.shields.static(text={"left": conf["label"], "right": display})
        badge.right_color = conf["color"]
        badge.logo = conf["logo"]
        badge.a_href = url
        badges.append(badge)
    return badges


def pypackit_badge():
    return bdg.shields.static(
        text={"left": "Template", "right": f"PyPackIT {pypackit.__version__}"},
        style="for-the-badge",
        color={"right": "rgb(0, 100, 0)"},
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
        alt="Template by PyPackIT",
        title=f"Project template created by PyPackIT version {pypackit.__version__}.",
        link="https://pypackit.readthedocs.io",
    )
