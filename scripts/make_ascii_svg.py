from pathlib import Path
from PIL import Image, ImageEnhance
import numpy as np
import html


SOURCE = Path("source-photo.jpg")
OUTPUT = Path("avi-ascii.svg")

WIDTH = 78

# Light → dark
RAMP = " .:-=+*#%@"

CHAR_W = 7
CHAR_H = 11


def main():

    if not SOURCE.exists():
        raise SystemExit(
            "ERROR: source-photo.jpg not found."
        )

    print("Loading original photo...")

    original = Image.open(
        SOURCE
    ).convert("RGB")

    rgb = np.array(
        original
    ).astype(np.float32)

    h, w = rgb.shape[:2]

    # ---------------------------------------------------------
    # Estimate the studio background from the outer edges.
    # ---------------------------------------------------------

    border = max(
        8,
        int(min(w, h) * 0.08)
    )

    border_pixels = np.concatenate([
        rgb[:border, :, :].reshape(-1, 3),
        rgb[-border:, :, :].reshape(-1, 3),
        rgb[:, :border, :].reshape(-1, 3),
        rgb[:, -border:, :].reshape(-1, 3),
    ])

    bg_color = np.median(
        border_pixels,
        axis=0
    )

    print(
        "Detected background:",
        bg_color.astype(int)
    )

    # ---------------------------------------------------------
    # Crop
    # ---------------------------------------------------------

    left = int(w * 0.04)
    right = int(w * 0.96)
    top = int(h * 0.025)
    bottom = int(h * 0.99)

    rgb = rgb[
        top:bottom,
        left:right
    ]

    # ---------------------------------------------------------
    # Convert RGB to grayscale for ASCII brightness.
    # ---------------------------------------------------------

    gray = (
        0.299 * rgb[:, :, 0]
        + 0.587 * rgb[:, :, 1]
        + 0.114 * rgb[:, :, 2]
    )

    # ---------------------------------------------------------
    # Calculate how different each pixel is from the
    # studio background.
    #
    # IMPORTANT:
    # We do NOT delete pixels.
    # We simply turn pixels that look like the background
    # into white/empty space.
    # ---------------------------------------------------------

    bg = bg_color.reshape(1, 1, 3)

    color_distance = np.sqrt(
        np.sum(
            (rgb - bg) ** 2,
            axis=2
        )
    )

    # ---------------------------------------------------------
    # Dark objects are ALWAYS preserved.
    #
    # This protects:
    # hair
    # eyebrows
    # eyes
    # beard
    # tie
    # suit
    # ---------------------------------------------------------

    dark_object = gray < 105

    # Background is usually a mid-gray.
    similar_background = (
        color_distance < 42
    )

    # Only suppress pixels that:
    # 1. look like background
    # 2. are not dark subject pixels
    suppress = (
        similar_background
        & ~dark_object
    )

    # Softly push background toward white.
    gray[suppress] = 245

    # ---------------------------------------------------------
    # Increase contrast.
    # ---------------------------------------------------------

    gray_image = Image.fromarray(
        np.clip(gray, 0, 255).astype(np.uint8)
    )

    gray_image = ImageEnhance.Contrast(
        gray_image
    ).enhance(1.45)

    gray_image = ImageEnhance.Sharpness(
        gray_image
    ).enhance(1.2)

    # ---------------------------------------------------------
    # Resize for ASCII.
    # ---------------------------------------------------------

    aspect = (
        gray_image.height
        / gray_image.width
    )

    ascii_height = max(
        1,
        int(
            WIDTH
            * aspect
            * 0.50
        )
    )

    gray_image = gray_image.resize(
        (
            WIDTH,
            ascii_height
        ),
        Image.Resampling.LANCZOS
    )

    pixels = np.array(
        gray_image
    )

    print(
        f"ASCII size: {WIDTH} x {ascii_height}"
    )

    # ---------------------------------------------------------
    # Generate ASCII rows.
    # ---------------------------------------------------------

    lines = []

    for y in range(ascii_height):

        row = []

        for x in range(WIDTH):

            brightness = int(
                pixels[y, x]
            )

            darkness = (
                255 - brightness
            )

            index = int(
                darkness
                / 255
                * (len(RAMP) - 1)
            )

            index = max(
                0,
                min(
                    len(RAMP) - 1,
                    index
                )
            )

            row.append(
                RAMP[index]
            )

        line = "".join(row)

        # Remove trailing background.
        line = line.rstrip()

        lines.append(line)

    # ---------------------------------------------------------
    # Find useful bounds.
    # ---------------------------------------------------------

    non_empty = [
        i
        for i, line in enumerate(lines)
        if line.strip()
    ]

    if non_empty:

        first = max(
            0,
            min(non_empty) - 1
        )

        last = min(
            len(lines),
            max(non_empty) + 2
        )

        lines = lines[first:last]

    # ---------------------------------------------------------
    # SVG dimensions
    # ---------------------------------------------------------

    svg_width = (
        WIDTH * CHAR_W + 40
    )

    svg_height = (
        len(lines) * CHAR_H + 45
    )

    svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{svg_width}"
height="{svg_height}"
viewBox="0 0 {svg_width} {svg_height}">

<defs>

<style>

.terminal {{
    fill: #0d1117;
}}

.frame {{
    fill: none;
    stroke: #30363d;
    stroke-width: 1;
}}

.ascii {{
    font-family:
        "Courier New",
        "Liberation Mono",
        monospace;

    font-size: 9px;

    font-weight: 700;

    fill: #58a6ff;

    opacity: 0;

    animation:
        typeLine
        0.5s
        ease-out
        forwards;
}}

@keyframes typeLine {{

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

</style>

</defs>

<rect
    class="terminal"
    x="0"
    y="0"
    width="100%"
    height="100%"
    rx="14"
/>

<rect
    class="frame"
    x="1"
    y="1"
    width="{svg_width - 2}"
    height="{svg_height - 2}"
    rx="14"
/>

'''

    # ---------------------------------------------------------
    # Add text rows.
    # ---------------------------------------------------------

    visible = 0

    for i, line in enumerate(lines):

        if not line.strip():
            continue

        y = (
            25
            + i * CHAR_H
        )

        delay = (
            visible * 0.045
        )

        svg += f'''
<text
class="ascii"
x="20"
y="{y}"
xml:space="preserve"
style="animation-delay:{delay:.3f}s"
>{html.escape(line)}</text>
'''

        visible += 1

    svg += """

</svg>
"""

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )

    print()
    print("================================")
    print("SUCCESS!")
    print("================================")
    print(
        f"Created: {OUTPUT.absolute()}"
    )


if __name__ == "__main__":
    main()