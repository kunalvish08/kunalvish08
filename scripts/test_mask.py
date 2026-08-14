from pathlib import Path
import cv2
import numpy as np

SOURCE = Path("source-photo.jpg")
OUTPUT = Path("masked-preview.png")

image = cv2.imread(str(SOURCE))

if image is None:
    raise SystemExit("source-photo.jpg not found")

h, w = image.shape[:2]

mask = np.zeros((h, w), dtype=np.uint8)

# Tighter silhouette around the actual person.
points = np.array([
    # Hair / head
    [112, 32],
    [145, 25],
    [195, 25],
    [235, 32],
    [260, 48],
    [268, 85],
    [268, 125],
    [263, 165],
    [250, 205],

    # Right side neck → shoulder
    [255, 225],
    [280, 245],
    [310, 265],
    [345, 285],
    [375, 305],
    [395, 325],

    # Right edge / bottom
    [399, 399],

    # Bottom / left edge
    [5, 399],
    [8, 325],

    # Left shoulder
    [28, 310],
    [55, 292],
    [82, 275],
    [105, 255],

    # Left neck
    [125, 225],
    [112, 205],

    # Left side face
    [105, 170],
    [103, 125],
    [105, 85],
    [108, 50],

], dtype=np.int32)

cv2.fillPoly(
    mask,
    [points],
    255
)

# Smooth only the edge.
mask = cv2.GaussianBlur(
    mask,
    (5, 5),
    0
)

gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)

# Preserve facial details.
gray = cv2.convertScaleAbs(
    gray,
    alpha=1.15,
    beta=-8
)

background = np.full_like(
    gray,
    255
)

alpha = mask.astype(np.float32) / 255.0

result = (
    gray.astype(np.float32) * alpha
    +
    background.astype(np.float32) * (1 - alpha)
)

result = np.clip(
    result,
    0,
    255
).astype(np.uint8)

cv2.imwrite(
    str(OUTPUT),
    result
)

print("SUCCESS!")
print(f"Created: {OUTPUT.absolute()}")