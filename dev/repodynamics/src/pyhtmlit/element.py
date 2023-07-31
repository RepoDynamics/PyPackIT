"""Dynamically create HTML syntax."""


# Standard libraries
import re
from typing import Literal, Optional, Sequence, Union

# Non-standard libraries
from pylinks.url import URL


_VOID_ELEMENTS = (
    "area",
    "base",
    "br",
    "col",
    "command",
    "embed",
    "hr",
    "img",
    "input",
    "keygen",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
)


class ElementCollection:
    def __init__(self, elements: list = None, seperator: dict | list | str = "\n"):
        self.elements = (
            (list(elements) if isinstance(elements, (list, tuple)) else [elements])
            if elements
            else list()
        )
        self.seperator = seperator
        return

    def __str__(self):
        if not self.elements:
            return ""
        string = ""
        for idx, element in enumerate(self.elements):
            string += str(element)
            if idx == len(self.elements) - 1:
                break
            if isinstance(self.seperator, dict):
                sep = self.seperator.get(idx)
                if not sep:
                    sep = self.seperator.get("default")
                    if not sep:
                        sep = ""
            elif isinstance(self.seperator, (list, tuple)):
                sep = self.seperator[idx % len(self.seperator)]
            else:
                sep = self.seperator
            string += str(sep)
        return string

    def display(self):
        # Non-standard libraries
        from IPython.display import HTML, display

        display(HTML(str(self)))
        return


class Element:
    def __init__(
        self,
        tag: str,
        attrs: Optional[dict] = None,
        content: Optional[list | ElementCollection] = None,
        tag_seperator: Optional[str] = "\n",
        content_indent: Optional[str] = "\t",
    ):
        self._tag = tag.lower()
        self.attrs = attrs or dict()
        self.content = (
            content if isinstance(content, ElementCollection) else ElementCollection(content)
        )
        self.tag_seperator = tag_seperator
        self.content_indent = content_indent
        return

    @property
    def tag(self):
        return f"<{self._tag}>"

    @property
    def is_void(self):
        return self._tag in _VOID_ELEMENTS

    def __str__(self):
        """
        The element in HTML syntax, e.g. for an IMG element:
        '<img alt="My Image" src="https://example.com/image">'.
        """
        attrs = []
        for key, val in self.attrs.items():
            if val is None:
                continue
            if isinstance(val, bool):
                if val:
                    attrs.append(f"{key}")
            else:
                attrs.append(f'{key}="{val}"')
        attrs_str = "" if not attrs else f" {' '.join(attrs)}"
        start_tag = f"<{self._tag}{attrs_str}>"
        if self.is_void:
            return start_tag
        end_tag = f"</{self._tag}>"
        if not self.content:
            return f"{start_tag}{end_tag}"
        content = "\n".join(
            [f"{self.content_indent}{line}" for line in str(self.content).split("\n")]
        )
        return f"{start_tag}{self.tag_seperator}{content}{self.tag_seperator}{end_tag}"

    def display(self):
        # Non-standard libraries
        from IPython.display import HTML, display

        display(HTML(str(self)))
        return


class DIV(Element):
    """A <div> element."""

    def __init__(
        self,
        content: Optional[list | ElementCollection] = None,
        tag_seperator: Optional[str] = "\n",
        content_indent: Optional[str] = "\t",
        **attrs,
    ):
        super().__init__(
            tag="div",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


class HR(Element):
    """An <hr> element."""

    def __init__(self, **attrs):
        super().__init__(tag="hr", attrs=attrs)
        return


class P(Element):
    """A <p> element."""

    def __init__(
        self,
        content: Optional[Sequence] = None,
        tag_seperator: Optional[str] = "\n",
        content_indent: Optional[str] = "\t",
        **attrs,
    ):
        super().__init__(
            tag="p",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return

    def style(self, words: dict[str, dict[str, str | bool]], ignore_case=False):
        """
        Given a string and a replacement map, it returns the replaced string.
        :param str string: string to execute replacements on
        :param dict words: replacement dictionary {value to find: value to replace}
        :param bool ignore_case: whether the match should be case insensitive
        :rtype: str

        Reference : https://stackoverflow.com/a/6117124/14923024
        """
        if not words:
            return self
        # If case insensitive, we need to normalize the old string so that later a replacement
        # can be found. For instance with {"HEY": "lol"} we should match and find a replacement for "hey",
        # "HEY", "hEy", etc.
        if ignore_case:

            def normalize_old(s):
                return s.lower()

            re_mode = re.IGNORECASE
        else:

            def normalize_old(s):
                return s

            re_mode = 0

        subs = dict()
        for word, config in words.items():
            mod_word = word
            if config.get("italic"):
                mod_word = f"<em>{mod_word}</em>"
            if config.get("bold"):
                mod_word = f"<strong>{mod_word}</strong>"
            if config.get("link"):
                mod_word = str(
                    A(
                        href=config.get("link"),
                        content=[mod_word],
                        tag_seperator="",
                        content_indent="",
                    )
                )
            subs[normalize_old(word)] = mod_word
        # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
        # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
        # 'hey ABC' and not 'hey ABc'
        rep_sorted = sorted(subs, key=len, reverse=True)
        rep_escaped = map(re.escape, rep_sorted)
        # Create a big OR regex that matches any of the substrings to replace
        pattern = re.compile("|".join(rep_escaped), re_mode)
        # For each match, look up the new string in the replacements, being the key the normalized old string
        string = self.content.elements[0]
        replaced_text = pattern.sub(
            lambda match: subs[normalize_old(match.group(0))], string, count=1
        )
        return P(
            content=[replaced_text],
            tag_seperator=self.tag_seperator,
            content_indent=self.content_indent,
            **self.attrs,
        )


class IMG(Element):
    """An <img> element."""

    def __init__(self, src: str | URL, **attrs):
        attrs["src"] = src
        super().__init__(tag="img", attrs=attrs)
        return


class A(Element):
    """An <a> element."""

    def __init__(
        self,
        href: str | URL,
        content: Optional[Sequence] = None,
        tag_seperator: Optional[str] = "\n",
        content_indent: Optional[str] = "\t",
        **attrs,
    ):
        """
        Parameters
        ----------
        href : str or pypackit.docs.html.URL
            Anchor reference.
        content : any
            Content of the anchor.
        """
        attrs["href"] = href
        super().__init__(
            tag="a",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


class SOURCE(Element):
    """A <source> element."""

    def __init__(self, **attrs):
        super().__init__(tag="source", attrs=attrs)
        return


class PICTURE(Element):
    """A <picture> element."""

    def __init__(
        self,
        img: IMG,
        sources: Sequence[SOURCE],
        tag_seperator: Optional[str] = "\n",
        content_indent: Optional[str] = "\t",
        **attrs,
    ):
        super().__init__(
            tag="picture",
            attrs=attrs,
            content=ElementCollection([*sources, img], seperator=tag_seperator),
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


class H(Element):
    """A heading element from <h1> to <h6>."""

    def __init__(
        self,
        level: Literal[1, 2, 3, 4, 5, 6],
        content: Optional[Sequence] = None,
        tag_seperator: Optional[str] = "\n",
        content_indent: Optional[str] = "\t",
        **attrs,
    ):
        super().__init__(
            tag=f"h{level}",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


class TABLE(Element):
    """A <table> element."""

    def __init__(
        self,
        content: Optional[Sequence] = None,
        tag_seperator: Optional[str] = "\n",
        content_indent: Optional[str] = "\t",
        **attrs,
    ):
        super().__init__(
            tag=f"table",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


class TR(Element):
    """A table-row <tr> element."""

    def __init__(
        self,
        content: Optional[Sequence] = None,
        tag_seperator: Optional[str] = "\n",
        content_indent: Optional[str] = "\t",
        **attrs,
    ):
        super().__init__(
            tag=f"tr",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


class TD(Element):
    """A table-data <td> element."""

    def __init__(
        self,
        content: Optional[Sequence] = None,
        tag_seperator: Optional[str] = "\n",
        content_indent: Optional[str] = "\t",
        **attrs,
    ):
        super().__init__(
            tag=f"td",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


class Comment:
    def __init__(self, comment: str):
        self.comment = comment
        return

    def __str__(self):
        return f"<!-- {self.comment} -->"
