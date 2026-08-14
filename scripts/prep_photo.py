from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image


def main():

    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py source-photo.jpg")
        sys.exit(1)

    source = Path(sys.argv[1])

    if not source.exists():
        print(f"ERROR: File not found: {source}")
        sys.exit(1)

    output = Path("source-prepped.png")

    print("[1/5] Loading original photo...")

    image = cv2.imread(str(source))

    if image is None:
        print("ERROR: Could not read image.")
        sys.exit(1)

    height, width = image.shape[:2]

    print(f"Image size: {width} x {height}")

    # ---------------------------------------------------------
    # Convert to LAB color space.
    # The background of the original photo is mostly neutral
    # gray, so LAB makes separation more stable.
    # ---------------------------------------------------------

    print("[2/5] Detecting connected background...")

    lab = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2LAB
    )

    # Estimate background color from the image borders.
    border = max(8, int(width * 0.05))

    border_pixels = np.concatenate([
        lab[:border, :, :].reshape(-1, 3),
        lab[-border:, :, :].reshape(-1, 3),
        lab[:, :border, :].reshape(-1, 3),
        lab[:, -border:, :].reshape(-1, 3)
    ])

    background_color = np.median(
        border_pixels,
        axis=0
    )

    print(
        "Estimated background:",
        background_color.astype(int)
    )

    # Distance from estimated background.
    diff = lab.astype(np.float32) - background_color

    distance = np.sqrt(
        np.sum(diff ** 2, axis=2)
    )

    # Initial background candidate.
    # Larger value = more different from background.
    background_candidate = (
        distance < 32
    ).astype(np.uint8) * 255

    # ---------------------------------------------------------
    # Only remove regions connected to the outside.
    # This is the key difference from the previous GrabCut
    # approach.
    # ---------------------------------------------------------

    print("[3/5] Removing edge-connected background...")

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        background_candidate,
        connectivity=8
    )

    background_mask = np.zeros(
        (height, width),
        dtype=np.uint8
    )

    for label in range(1, num_labels):

        x = stats[label, cv2.CC_STAT_LEFT]
        y = stats[label, cv2.CC_STAT_TOP]
        w = stats[label, cv2.CC_STAT_WIDTH]
        h = stats[label, cv2.CC_STAT_HEIGHT]

        touches_edge = (
            x <= 1
            or y <= 1
            or x + w >= width - 1
            or y + h >= height - 1
        )

        if touches_edge:
            background_mask[
                labels == label
            ] = 255

    # Expand background slightly to clean the boundary.
    kernel = np.ones(
        (7, 7),
        np.uint8
    )

    background_mask = cv2.morphologyEx(
        background_mask,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    background_mask = cv2.dilate(
        background_mask,
        kernel,
        iterations=1
    )

    # ---------------------------------------------------------
    # Create foreground mask.
    # ---------------------------------------------------------

    foreground_mask = (
        255 - background_mask
    )

    # Smooth edge.
    foreground_mask = cv2.GaussianBlur(
        foreground_mask,
        (5, 5),
        0
    )

    # ---------------------------------------------------------
    # Grayscale + contrast.
    # ---------------------------------------------------------

    print("[4/5] Preparing high-contrast portrait...")

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    gray = clahe.apply(gray)

    # Gentle sharpening.
    sharpen_kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    gray = cv2.filter2D(
        gray,
        -1,
        sharpen_kernel
    )

    # ---------------------------------------------------------
    # Composite subject on pure white.
    # ---------------------------------------------------------

    alpha = (
        foreground_mask.astype(np.float32)
        / 255.0
    )

    result = (
        gray.astype(np.float32) * alpha
        +
        255.0 * (1.0 - alpha)
    )

    result = np.clip(
        result,
        0,
        255
    ).astype(np.uint8)

    print("[5/5] Saving final image...")

    Image.fromarray(
        result
    ).save(output)

    print()
    print("SUCCESS!")
    print(
        f"Created: {output.absolute()}"
    )


if __name__ == "__main__":
    main()