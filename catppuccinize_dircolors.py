#!/usr/bin/env python3

"""
catppuccinize_dircolors.py -- modify existing .dircolors to appease Catppuccin.

For example:
curl -fSsL https://raw.githubusercontent.com/coreutils/coreutils/master/src/dircolors.hin | ./catppuccinize_dircolors.py

This will create 'themes/catppuccin-{flavour}' folders with a .dircolors file inside.

source: https://github.com/dracula/dircolors/blob/main/draculize_dircolors.py
Copyright (C) Ville Skyttä
SPDX-License-Identifier: MIT
"""

import os
import re
import sys
from typing import Match, Dict

# Define color palettes
PALETTES: Dict[str, Dict[str, str]] = {
    "catppuccin-latte": {
        "30": "#bcc0cc",  # surface1
        "31": "#d20f39",  # red
        "32": "#40a02b",  # green
        "33": "#df8e1d",  # yellow
        "34": "#1e66f5",  # blue
        "35": "#ea76cb",  # pink
        "36": "#179299",  # teal
        "37": "#4c4f69",  # text
        "90": "#7287fd",  # lavender
        "91": "#d20f39",  # red
        "92": "#40a02b",  # green
        "93": "#df8e1d",  # yellow
        "94": "#1e66f5",  # blue
        "95": "#ea76cb",  # pink
        "96": "#04a5e5",  # sky
        "97": "#6c6f85",  # subtext0
    },
    "catppuccin-frappe": {
        "30": "#51576d",  # surface1
        "31": "#e78284",  # red
        "32": "#a6d189",  # green
        "33": "#e5c890",  # yellow
        "34": "#8caaee",  # blue
        "35": "#f4b8e4",  # pink
        "36": "#81c8be",  # teal
        "37": "#c6d0f5",  # text
        "90": "#babbf1",  # lavender
        "91": "#e78284",  # red
        "92": "#a6d189",  # green
        "93": "#e5c890",  # yellow
        "94": "#8caaee",  # blue
        "95": "#f4b8e4",  # pink
        "96": "#99d1db",  # sky
        "97": "#a5adce",  # subtext0
    },
    "catppuccin-macchiato": {
        "30": "#494d64",  # surface1
        "31": "#ed8796",  # red
        "32": "#a6da95",  # green
        "33": "#eed49f",  # yellow
        "34": "#8aadf4",  # blue
        "35": "#f5bde6",  # pink
        "36": "#8bd5ca",  # teal
        "37": "#cad3f5",  # text
        "90": "#b7bdf8",  # lavender
        "91": "#ed8796",  # red
        "92": "#a6da95",  # green
        "93": "#eed49f",  # yellow
        "94": "#8aadf4",  # blue
        "95": "#f5bde6",  # pink
        "96": "#91d7e3",  # sky
        "97": "#a5adcb",  # subtext0
    },
    "catppuccin-mocha": {
        "30": "#45475a",  # surface1
        "31": "#f38ba8",  # red
        "32": "#a6e3a1",  # greed
        "33": "#f9e2af",  # yellow
        "34": "#89b4fa",  # blue
        "35": "#f5c2e7",  # pink
        "36": "#94e2d5",  # teal
        "37": "#cdd6f4",  # text
        "90": "#b4befe",  # lavender
        "91": "#f38ba8",  # red
        "92": "#a6e3a1",  # green
        "93": "#f9e2af",  # yellow
        "94": "#89b4fa",  # blue
        "95": "#f5c2e7",  # pink
        "96": "#89dceb",  # sky
        "97": "#a6adc8",  # subtext0
    },
}


def main() -> None:
    """Run the tool."""
    # Read the entire input from stdin first
    input_lines = sys.stdin.readlines()

    # Parent directory for all themes
    themes_base_dir = "themes"
    try:
        os.makedirs(themes_base_dir, exist_ok=True)
    except OSError as e:
        print(f"Error creating base directory {themes_base_dir}: {e}", file=sys.stderr)
        return

    # Iterate over each defined palette
    for name, palette in PALETTES.items():
        # Create 24-bit color maps from the palette
        # https://spec.draculatheme.com/#sec-ANSI
        # https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and-4-bit
        # https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit
        fg_map = {
            k: "38;2;%d;%d;%d"
            % tuple(int(v[i : i + 2], 16) for i in range(1, len(v), 2))
            for k, v in palette.items()
        }
        bg_map = {str(int(k) + 10): f"4{v[1:]}" for k, v in fg_map.items()}

        def map_color(match: Match[str]) -> str:
            """Map basic ANSI color to 24-bit Dracula for the current theme."""
            match_str = match.group(0)
            return fg_map.get(match_str, bg_map.get(match_str, match_str))

        # Create the specific directory for the theme inside the base directory
        theme_dir = os.path.join(themes_base_dir, name)
        try:
            os.makedirs(theme_dir, exist_ok=True)
        except OSError as e:
            print(f"Error creating directory {theme_dir}: {e}", file=sys.stderr)
            continue

        # Write the modified dircolors file inside the theme's directory
        output_path = os.path.join(theme_dir, ".dircolors")
        try:
            with open(output_path, "w") as f:
                for line in input_lines:
                    f.write(re.sub(r"\d+", map_color, line))
            print(f"Generated {output_path}")
        except IOError as e:
            print(f"Error writing to file {output_path}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
