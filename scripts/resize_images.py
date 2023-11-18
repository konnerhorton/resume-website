import os
from PIL import Image

"""Resizes the original image and saves to appropriate files"""

original_file = "assets\\images\\image_original.JPG"
conversions = {
    "sidebar_profile.jpg": (
        192,
        192,
    ),
    "android-chrome-192x192.png": (
        192,
        192,
    ),
    "android-chrome-256x256.png": (
        256,
        256,
    ),
    "apple-touch-icon.png": (
        180,
        180,
    ),
    "favicon.ico": (32, 32),
    "favicon-16x16.png": (
        16,
        16,
    ),
    "favicon-32x32.png": (
        32,
        32,
    ),
    "mstile-150x150.png": (
        150,
        150,
    ),
}

for k, v in conversions.items():
    original_image = Image.open(f"{os.path.dirname(os.getcwd())}\\{original_file}")
    if k in ["sidebar_profile.jpg"]:
        original_image.resize(v).save(
            f"{os.path.dirname(os.getcwd())}\\assets\\images\\{k}"
        )
    else:
        original_image.resize(v).save(
            f"{os.path.dirname(os.getcwd())}\\assets\\favicons\\{k}"
        )
