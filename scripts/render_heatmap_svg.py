from pathlib import Path
import json
from datetime import datetime


DATA = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")

CELL = 12
GAP = 4

LEFT = 42
TOP = 55

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
            "ERROR: data/contributions.json not found."
        )

    data = json.loads(
        DATA.read_text(
            encoding="utf-8"
        )
    )

    days = data["days"]
    stats = data["stats"]

    # ---------------------------------------------------------
    # GitHub calendar
    # ---------------------------------------------------------

    # Convert dates
    for day in days:
        day["date_obj"] = datetime.strptime(
            day["date"],
            "%Y-%m-%d"
        ).date()

    # GitHub calendar starts Sunday.
    first = days[0]["date_obj"]

    start_offset = (
        first.weekday() + 1
    ) % 7

    # Pad beginning
    padded = (
        [None] * start_offset
        + days
    )

    weeks = (
        len(padded) + 6
    ) // 7

    # ---------------------------------------------------------
    # SVG
    # ---------------------------------------------------------

    svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<defs>

<style>

.background {{
    fill: #0d1117;
}}

.border {{
    fill: none;
    stroke: #30363d;
    stroke-width: 1;
}}

.cell {{
    opacity: 0;
    transform-origin: center;
    animation:
        reveal
        0.45s
        ease-out
        forwards;
}}

@keyframes reveal {{

    0% {{
        opacity: 0;
        transform:
            scale(0.35)
            translateY(10px);
    }}

    70% {{
        opacity: 1;
        transform:
            scale(1.08)
            translateY(-1px);
    }}

    100% {{
        opacity: 1;
        transform:
            scale(1)
            translateY(0);
    }}

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

.stats {{
    fill: #58a6ff;

    font-family:
        "Courier New",
        monospace;

    font-size: 12px;

    font-weight: 700;
}}

.legend {{
    fill: #8b949e;

    font-family:
        "Courier New",
        monospace;

    font-size: 10px;
}}

</style>

</defs>


<!-- Background -->

<rect
class="background"
x="0"
y="0"
width="{WIDTH}"
height="{HEIGHT}"
rx="14"/>


<!-- Border -->

<rect
class="border"
x="1"
y="1"
width="{WIDTH - 2}"
height="{HEIGHT - 2}"
rx="14"/>


<!-- Header -->

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

$ ./contributions.sh

</text>


'''

    # ---------------------------------------------------------
    # Contribution cells
    # ---------------------------------------------------------

    visible = 0

    for index, item in enumerate(padded):

        if item is None:
            continue

        position = index

        week = position // 7
        day = position % 7

        x = (
            LEFT
            + week
            * (CELL + GAP)
        )

        y = (
            TOP
            + day
            * (CELL + GAP)
        )

        level = int(
            item.get(
                "level",
                0
            )
        )

        level = max(
            0,
            min(
                4,
                level
            )
        )

        delay = (
            visible * 0.008
        )

        svg += f'''
<rect
class="cell"
x="{x}"
y="{y}"
width="{CELL}"
height="{CELL}"
rx="3"
fill="{PALETTE[level]}"
style="animation-delay:{delay:.3f}s"
/>
'''

        visible += 1

    # ---------------------------------------------------------
    # Footer
    # ---------------------------------------------------------

    total = stats[
        "total_activity"
    ]

    active = stats[
        "active_days"
    ]

    current = stats[
        "current_streak"
    ]

    longest = stats[
        "longest_streak"
    ]

    svg += f'''

<!-- Footer -->

<text
x="22"
y="180"
class="stats">

{active} active days
</text>


<text
x="170"
y="180"
class="stats">

current streak: {current}
</text>


<text
x="350"
y="180"
class="stats">

longest streak: {longest}
</text>


<text
x="620"
y="180"
class="stats">

activity: {total}
</text>


<!-- Legend -->

<text
x="22"
y="214"
class="legend">

Less
</text>
'''

    legend_x = 62

    for i, color in enumerate(
        PALETTE
    ):

        x = (
            legend_x
            + i * 22
        )

        svg += f'''
<rect
x="{x}"
y="205"
width="12"
height="12"
rx="3"
fill="{color}"/>
'''

    svg += '''

<text
x="180"
y="214"
class="legend">

More
</text>


</svg>
'''

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )

    print()
    print("========================================")
    print("CONTRIBUTION HEATMAP CREATED")
    print("========================================")
    print(
        f"Created: {OUTPUT.absolute()}"
    )
    print(
        f"Cells rendered: {visible}"
    )
    print()


if __name__ == "__main__":
    main()