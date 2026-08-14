from pathlib import Path
import json
from datetime import datetime


DATA = Path("data/contributions.json")
OUTPUT = Path("snake.svg")

CELL = 12
GAP = 4

LEFT = 42
TOP = 58

WIDTH = 860
HEIGHT = 245


PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]


def main():

    if not DATA.exists():
        raise SystemExit(
            "data/contributions.json not found"
        )

    data = json.loads(
        DATA.read_text(
            encoding="utf-8"
        )
    )

    days = data["days"]

    for day in days:
        day["date_obj"] = datetime.strptime(
            day["date"],
            "%Y-%m-%d"
        ).date()

    first = days[0]["date_obj"]

    start_offset = (
        first.weekday() + 1
    ) % 7

    padded = (
        [None] * start_offset
        + days
    )

    svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<defs>

<style>

.bg {{
    fill: #0d1117;
}}

.border {{
    fill: none;
    stroke: #30363d;
    stroke-width: 1;
}}

.cell {{
    opacity: 0.9;
}}

.snake {{
    fill: none;
    stroke: #58a6ff;
    stroke-width: 5;
    stroke-linecap: round;
    stroke-linejoin: round;

    stroke-dasharray: 12 12;

    animation:
        moveSnake
        2.8s
        linear
        infinite;
}}

.snake-head {{
    fill: #ffffff;

    animation:
        headMove
        2.8s
        linear
        infinite;
}}

.title {{
    fill: #c9d1d9;

    font-family:
        "Courier New",
        monospace;

    font-size: 17px;
    font-weight: 700;
}}

.subtitle {{
    fill: #8b949e;

    font-family:
        "Courier New",
        monospace;

    font-size: 12px;
}}

@keyframes moveSnake {{

    from {{
        stroke-dashoffset: 0;
    }}

    to {{
        stroke-dashoffset: -120;
    }}

}}

@keyframes headMove {{

    0% {{
        opacity: 1;
    }}

    50% {{
        opacity: 0.35;
    }}

    100% {{
        opacity: 1;
    }}

}}

</style>

</defs>

<rect
class="bg"
x="0"
y="0"
width="{WIDTH}"
height="{HEIGHT}"
rx="14"/>

<rect
class="border"
x="1"
y="1"
width="{WIDTH - 2}"
height="{HEIGHT - 2}"
rx="14"/>

<text
x="22"
y="27"
class="title">

github@kunalvish08

</text>

<text
x="22"
y="45"
class="subtitle">

$ ./snake --contributions

</text>

'''

    # -------------------------------------------------
    # Contribution cells
    # -------------------------------------------------

    active_points = []

    for index, item in enumerate(padded):

        if item is None:
            continue

        week = index // 7
        day = index % 7

        x = (
            LEFT
            + week * (CELL + GAP)
        )

        y = (
            TOP
            + day * (CELL + GAP)
        )

        level = max(
            0,
            min(
                4,
                int(
                    item.get(
                        "level",
                        0
                    )
                )
            )
        )

        svg += f'''
<rect
class="cell"
x="{x}"
y="{y}"
width="{CELL}"
height="{CELL}"
rx="3"
fill="{PALETTE[level]}"/>
'''

        if level > 0:
            active_points.append(
                (
                    x + CELL / 2,
                    y + CELL / 2
                )
            )

    # -------------------------------------------------
    # Build snake path from contribution points
    # -------------------------------------------------

    if len(active_points) > 8:

        # Use a recent section so the snake
        # remains visually clean.

        points = active_points[-45:]

        path = (
            f"M {points[0][0]} {points[0][1]}"
        )

        for x, y in points[1:]:
            path += (
                f" L {x} {y}"
            )

        svg += f'''

<path
class="snake"
d="{path}"/>

<circle
class="snake-head"
cx="{points[-1][0]}"
cy="{points[-1][1]}"
r="4"/>

'''

    # -------------------------------------------------
    # Footer
    # -------------------------------------------------

    stats = data["stats"]

    svg += f'''

<text
x="22"
y="205"
class="subtitle">

{stats["active_days"]} active days
 •
current streak: {stats["current_streak"]}
 •
longest: {stats["longest_streak"]}

</text>

<text
x="22"
y="225"
class="subtitle">

activity trail generated from GitHub contribution data

</text>

</svg>
'''

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )

    print()
    print("========================================")
    print("SNAKE GRAPH CREATED")
    print("========================================")
    print(
        f"Created: {OUTPUT.absolute()}"
    )
    print()


if __name__ == "__main__":
    main()