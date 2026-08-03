from pathlib import Path
import sys

from PIL import Image


ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
ASSETS = ROOT.parents[1] / "assets"
PREVIEWS = ROOT / "previews"
FRAME_COUNT = 96
FRAME_SIZE = 168
ASSETS.mkdir(parents=True, exist_ok=True)
PREVIEWS.mkdir(parents=True, exist_ok=True)

requested = set(sys.argv[1:])
for logo_dir in sorted((BUILD / "frames").iterdir()):
    if requested and logo_dir.name not in requested:
        continue
    frames = [Image.open(path).convert("RGBA") for path in sorted(logo_dir.glob("*.png"))]
    if len(frames) != FRAME_COUNT:
        raise RuntimeError(f"{logo_dir.name}: expected {FRAME_COUNT} frames, found {len(frames)}")

    sprite = Image.new("RGBA", (FRAME_SIZE * FRAME_COUNT, FRAME_SIZE))
    for index, frame in enumerate(frames):
        if frame.size != (FRAME_SIZE, FRAME_SIZE):
            raise RuntimeError(f"{logo_dir.name}: expected {FRAME_SIZE}px frames, found {frame.size}")
        sprite.paste(frame, (index * FRAME_SIZE, 0))
    sprite.save(ASSETS / f"{logo_dir.name}-sprite.webp", "WEBP", quality=90, method=6)

    frames[5].save(ASSETS / f"{logo_dir.name}-poster.webp", "WEBP", quality=92, method=6)
    frames[0].save(
        PREVIEWS / f"{logo_dir.name}-preview.webp",
        "WEBP",
        save_all=True,
        append_images=frames[1:],
        duration=42,
        loop=0,
        quality=88,
        method=6,
    )

(BUILD / "packaged.done").write_text("ok")
