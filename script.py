import colorsys
import csv
from pathlib import Path
import sys
from typing import NamedTuple

from rich.console import Console
from rich.table import Table

from data import download_data, colors_csv_file

console = Console()
error_console = Console(stderr=True, style="bold red")

FULL_COLOR_HEX_LEN = 7


class Hls(NamedTuple):
    H: float
    L: float
    S: float


class Color(NamedTuple):
    hex_: str
    name: str
    hls: Hls


def get_hex_colors(search_term):
    if not Path(colors_csv_file).exists():
        download_data()

    with open(colors_csv_file) as f:
        rows = csv.DictReader(f)
        for row in rows:
            hex_, name = row["hex"], row["name"]
            if len(hex_) != FULL_COLOR_HEX_LEN:
                continue
            if search_term.lower() not in name.lower():
                continue
            hls = Hls(*colorsys.rgb_to_hls(
                int(row["r"]), int(row["g"]), int(row["b"])
            ))
            yield Color(hex_, name, hls)


def show_colors(seach_term, colors, num_column_pairs=3, order_by_hls=True):
    if order_by_hls:
        colors.sort(key=lambda x: x.hls.L)

    table = Table(title=f"Matching colors for {search_term}")

    for _ in range(num_column_pairs):
        table.add_column("Hex")
        table.add_column("Name")

    def _color(hex_, string):
        return f"[{hex_}]{string}"

    row = []
    for i, color in enumerate(colors, start=1):
        row.extend([
            _color(color.hex_, color.hex_),
            _color(color.hex_, color.name)
        ])
        is_last_row = i == len(colors)  # in case < num_column_pairs results
        if i % num_column_pairs == 0 or is_last_row:
            table.add_row(*row)
            row = []

    console.print(table)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} search_term")
        sys.exit(1)

    search_term = sys.argv[1]
    colors = list(get_hex_colors(search_term))
    if colors:
        show_colors(search_term, colors)
    else:
        error_console.print(f"No matches for {search_term}")
