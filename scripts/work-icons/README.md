# Work icon generator

Reproducible source and outputs for the five spinning Experience badges.

## Contents

- `source/`: supplied raster logos.
- `vectors/`: Potrace SVGs consumed by Blender.
- `exports/`: final posters, CSS sprite sheets, and animated previews.
- `build/`: generated masks, PNG frames, and stills; ignored by Git.

Each final sprite is 96 frames at 168×168 pixels, packed horizontally into a
16,128×168 WebP. The matching preview WebP loops those frames in four seconds.

## Requirements

- Python with Pillow and NumPy
- Potrace
- Blender with the SVG importer

## Regenerate vectors after changing a source logo

```sh
python3 prepare_logos.py
potrace build/ellipsis.pbm -s -o vectors/ellipsis.svg --turdsize 2 --alphamax 1 --opttolerance 0.2
potrace build/selini.pbm -s -o vectors/selini.svg --turdsize 2 --alphamax 1 --opttolerance 0.2
potrace build/mgnr.pbm -s -o vectors/mgnr.svg --turdsize 2 --alphamax 1 --opttolerance 0.2
potrace build/mschf.pbm -s -o vectors/mschf.svg --turdsize 2 --alphamax 1 --opttolerance 0.2
potrace build/vatic-dark.pbm -s -o vectors/vatic-dark.svg --turdsize 2 --alphamax 1 --opttolerance 0.2
potrace build/vatic-light.pbm -s -o vectors/vatic-light.svg --turdsize 2 --alphamax 1 --opttolerance 0.2
python3 ungroup_svgs.py
```

## Render and package

Run Blender in normal windowed mode; the installed Blender 5.2 build crashed on
this Mac when started with `--background`.

```sh
blender --python render_previews.py
blender --python render_animations.py
python3 package_animations.py
```

Append a logo name to rebuild only that animation or package, for example:

```sh
blender --python render_animations.py -- mschf
python3 package_animations.py mschf
```
