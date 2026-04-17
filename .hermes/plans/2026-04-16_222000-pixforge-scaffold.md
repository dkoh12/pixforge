# pixforge — Project Plan

## Goal
Build a powerful CLI image conversion and transformation toolkit supporting multiple formats and operations.

## Supported Formats
- Input/Output: PNG, JPEG, WebP, AVIF, GIF, TIFF, BMP

## Features
- **Format conversion** — convert between any supported formats
- **Resize** — scale by percentage or exact width/height
- **Resolution** — set DPI for print-ready output
- **Quality** — control compression quality (1-100)
- **Crop** — crop to specific dimensions
- **Rotate** — rotate by degrees
- **Flip** — horizontal/vertical
- **Grayscale** — convert to grayscale
- **Batch processing** — process entire directories at once

## Tech Stack
- **Language**: Python 3
- **Core library**: [Pillow](https://pillow.readthedocs.io/) — battle-tested image processing
- **CLI framework**: [Click](https://click.palletsprojects.com/) — clean, composable CLI
- **Packaging**: `pyproject.toml` with `pip install -e .` support

## Proposed File Structure
```
pixforge/
├── README.md
├── pyproject.toml
├── requirements.txt
├── pixforge/
│   ├── __init__.py
│   ├── cli.py          # Click CLI entrypoint
│   ├── converter.py    # Format conversion logic
│   ├── transforms.py   # Resize, crop, rotate, flip, grayscale
│   └── utils.py        # Helpers (file detection, validation)
└── tests/
    ├── test_converter.py
    ├── test_transforms.py
    └── sample_images/  # small test images
```

## CLI Design
```bash
# Convert format
pixforge convert input.png output.jpg

# Convert with quality
pixforge convert input.png output.jpg --quality 85

# Resize by percentage
pixforge convert input.png output.png --scale 50

# Resize to exact dimensions
pixforge convert input.png output.png --width 800 --height 600

# Set DPI
pixforge convert input.png output.png --dpi 300

# Rotate
pixforge convert input.png output.png --rotate 90

# Grayscale
pixforge convert input.png output.png --grayscale

# Batch convert entire folder
pixforge batch ./images/ ./output/ --format webp --quality 80
```

## Step-by-Step Plan

1. **Initialize repo** — `pyproject.toml`, `requirements.txt`, `.gitignore`
2. **Core module** — `converter.py` with format conversion using Pillow
3. **Transforms module** — resize, crop, rotate, flip, grayscale
4. **CLI** — Click-based `cli.py` wiring everything together
5. **Batch command** — directory-level processing
6. **Tests** — unit tests for converter and transforms
7. **README** — usage examples, install instructions
8. **PR** — open PR via GitHub App

## Files to Create
- `README.md`
- `pyproject.toml`
- `requirements.txt`
- `.gitignore`
- `pixforge/__init__.py`
- `pixforge/cli.py`
- `pixforge/converter.py`
- `pixforge/transforms.py`
- `pixforge/utils.py`
- `tests/test_converter.py`
- `tests/test_transforms.py`

## Risks / Open Questions
- AVIF support requires `pillow-avif-plugin` or Pillow 9.1+ with libaom — may need to make it optional
- GIF animation handling — out of scope for v1, static GIF only
- Should `--width` without `--height` maintain aspect ratio? → Yes, default behavior
