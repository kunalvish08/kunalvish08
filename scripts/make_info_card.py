from pathlib import Path
import html


OUTPUT = Path("info-card.svg")

WIDTH = 520
HEIGHT = 430


def main():

    svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<defs>

    <linearGradient
        id="cardBorder"
        x1="0"
        y1="0"
        x2="1"
        y2="1">

        <stop
            offset="0%"
            stop-color="#58a6ff"/>

        <stop
            offset="100%"
            stop-color="#30363d"/>

    </linearGradient>

    <style>

        .terminal {{
            fill: #0d1117;
        }}

        .border {{
            fill: none;
            stroke: url(#cardBorder);
            stroke-width: 1;
        }}

        .title {{
            font-family:
                "Courier New",
                "Liberation Mono",
                monospace;

            font-size: 17px;
            font-weight: 700;
            fill: #58a6ff;
        }}

        .prompt {{
            font-family:
                "Courier New",
                "Liberation Mono",
                monospace;

            font-size: 13px;
            fill: #8b949e;
        }}

        .key {{
            font-family:
                "Courier New",
                "Liberation Mono",
                monospace;

            font-size: 14px;
            font-weight: 700;
            fill: #58a6ff;
        }}

        .value {{
            font-family:
                "Courier New",
                "Liberation Mono",
                monospace;

            font-size: 14px;
            fill: #c9d1d9;
        }}

        .accent {{
            fill: #3fb950;
        }}

        .yellow {{
            fill: #d29922;
        }}

        .line {{
            stroke: #30363d;
            stroke-width: 1;
        }}

        .row {{
            opacity: 0;

            animation:
                appear
                0.45s
                ease-out
                forwards;
        }}

        @keyframes appear {{

            0% {{
                opacity: 0;
                transform:
                    translateX(-12px);
            }}

            100% {{
                opacity: 1;
                transform:
                    translateX(0);
            }}

        }}

        .cursor {{
            animation:
                blink
                1s
                step-end
                infinite;
        }}

        @keyframes blink {{

            0%, 45% {{
                opacity: 1;
            }}

            46%, 100% {{
                opacity: 0;
            }}

        }}

    </style>

</defs>


<!-- Terminal background -->

<rect
    class="terminal"
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


<!-- Terminal header -->

<circle
    cx="24"
    cy="24"
    r="5"
    fill="#ff7b72"/>

<circle
    cx="42"
    cy="24"
    r="5"
    fill="#d29922"/>

<circle
    cx="60"
    cy="24"
    r="5"
    fill="#3fb950"/>


<text
    x="82"
    y="29"
    class="prompt">
    ~/kunalvish08
</text>


<line
    x1="20"
    y1="48"
    x2="500"
    y2="48"
    class="line"/>


<!-- Command -->

<text
    x="24"
    y="78"
    class="prompt">
    $ whoami
</text>


<text
    x="24"
    y="108"
    class="title">
    kunal@github
</text>


<text
    x="190"
    y="108"
    class="prompt">
    — profile.sh
</text>


<!-- ROW 1 -->

<g
    class="row"
    style="animation-delay:0.20s">

    <text
        x="28"
        y="145"
        class="key">
        ROLE
    </text>

    <text
        x="150"
        y="145"
        class="value">
        CSE • AI Student
    </text>

</g>


<!-- ROW 2 -->

<g
    class="row"
    style="animation-delay:0.35s">

    <text
        x="28"
        y="177"
        class="key">
        FOCUS
    </text>

    <text
        x="150"
        y="177"
        class="value">
        SDE • AI • GenAI
    </text>

</g>


<!-- ROW 3 -->

<g
    class="row"
    style="animation-delay:0.50s">

    <text
        x="28"
        y="209"
        class="key">
        BUILDING
    </text>

    <text
        x="150"
        y="209"
        class="value">
        NexAlgoTrix
    </text>

</g>


<!-- ROW 4 -->

<g
    class="row"
    style="animation-delay:0.65s">

    <text
        x="28"
        y="241"
        class="key">
        COMMUNITY
    </text>

    <text
        x="150"
        y="241"
        class="value">
        10K+ followers
    </text>

</g>


<!-- ROW 5 -->

<g
    class="row"
    style="animation-delay:0.80s">

    <text
        x="28"
        y="273"
        class="key">
        REACH
    </text>

    <text
        x="150"
        y="273"
        class="value">
        500K+ views
    </text>

</g>


<!-- Divider -->

<line
    x1="24"
    y1="295"
    x2="496"
    y2="295"
    class="line"/>


<!-- STACK -->

<g
    class="row"
    style="animation-delay:0.95s">

    <text
        x="28"
        y="322"
        class="key">
        STACK
    </text>

    <text
        x="150"
        y="322"
        class="value">
        C++ • Python • JS
    </text>

</g>


<g
    class="row"
    style="animation-delay:1.10s">

    <text
        x="150"
        y="348"
        class="value">
        React • Node • Next
    </text>

</g>


<g
    class="row"
    style="animation-delay:1.25s">

    <text
        x="150"
        y="374"
        class="value">
        MongoDB • SQL • Git
    </text>

</g>


<g
    class="row"
    style="animation-delay:1.40s">

    <text
        x="150"
        y="400"
        class="value">
        OpenAI • Gemini
    </text>

</g>


<!-- Status -->

<text
    x="390"
    y="428"
    class="prompt">

    status:
</text>

<text
    x="447"
    y="428"
    class="accent">

    online
</text>

<text
    x="490"
    y="428"
    class="cursor accent">
    _
</text>


</svg>
'''

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )

    print()
    print("================================")
    print("INFO CARD CREATED")
    print("================================")
    print(
        f"Created: {OUTPUT.absolute()}"
    )


if __name__ == "__main__":
    main()