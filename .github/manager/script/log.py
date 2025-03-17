#!/usr/bin/env python3

import sys


LEN_CONSOLE_LINE = 88
HEADING_COLORS = [
    (255, 200, 255),
    (235, 160, 255),
    (215, 120, 255),
    (195, 80, 255),
    (175, 40, 255),
    (155, 0, 255),
]
LINE_COLORS = [
    (250, 250, 230),
    (220, 220, 200),
    (190, 190, 170),
    (160, 160, 140),
    (130, 130, 110),
    (100, 100, 80),
]


def heading(content: str):
    number, title = content.split(" ", 1)
    level = min(len(number.removesuffix(".").split(".")), len(HEADING_COLORS))
    len_heading = len(content)
    len_margin = 2
    num_dashes = LEN_CONSOLE_LINE - len_heading - len_margin
    num_dashes_left = num_dashes // 2
    num_dashes_right = num_dashes - num_dashes_left
    line_char = "–"
    heading_text = _apply_style(content.strip(), HEADING_COLORS[level - 1], bold=True)
    line_left = _apply_style(line_char * num_dashes_left, LINE_COLORS[level - 1], bold=True)
    line_right = _apply_style(line_char * num_dashes_right, LINE_COLORS[level - 1], bold=True)
    return f"{line_left} {heading_text} {line_right}"


def _apply_style(text: str, color: tuple[int, int, int], bold: bool = False):
    return f"\033[{'1;' if bold else ''}38;2;{color[0]};{color[1]};{color[2]}m{text}\033[0m"


if __name__ == "__main__":
    # Check if the necessary arguments are provided
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} 'X.Y.Z Title'")
        sys.exit(1)
    print(heading(sys.argv[1]))
