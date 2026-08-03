from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source"
OUTPUT = ROOT / "build"
OUTPUT.mkdir(parents=True, exist_ok=True)


def save_mask(name, mask):
    pixels = np.where(mask, 0, 255).astype(np.uint8)
    Image.fromarray(pixels, mode="L").convert("1").save(OUTPUT / f"{name}.pbm")


for name in ("ellipsis", "selini", "mgnr", "mschf", "vatic"):
    image = np.asarray(Image.open(SOURCE / f"{name}.png").convert("RGBA"))
    rgb, alpha = image[..., :3], image[..., 3]

    if name in ("ellipsis", "selini"):
        save_mask(name, (rgb.mean(axis=2) > 150) & (alpha > 128))
    elif name == "mgnr":
        save_mask(name, (rgb.mean(axis=2) < 100) & (alpha > 128))
    elif name == "mschf":
        save_mask(name, (rgb[..., 0] > 180) & (rgb[..., 1] < 100) & (alpha > 128))
    else:
        # The supplied Vatic image contains a wordmark below the symbol.
        symbol = rgb[:225]
        symbol_alpha = alpha[:225]
        save_mask("vatic-dark", (symbol[..., 0] < 100) & (symbol[..., 2] > 50) & (symbol_alpha > 128))
        save_mask("vatic-light", (symbol[..., 0] > 100) & (symbol[..., 2] > 150) & (symbol_alpha > 128))
