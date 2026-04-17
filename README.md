# pixforge 🔨

A powerful CLI tool for image conversion and transformation. Convert between formats, resize, crop, rotate, flip, and more.

## Supported Formats

PNG, JPEG, WebP, AVIF, GIF, TIFF, BMP

## Installation

```bash
pip install pixforge
```

Or install from source:
```bash
git clone https://github.com/dkoh12/pixforge.git
cd pixforge
pip install -e .
```

## Usage

### Convert a single image

```bash
# Basic format conversion
pixforge convert input.png output.jpg

# Control quality (JPEG/WebP)
pixforge convert input.png output.jpg --quality 85

# Set DPI for print-ready output
pixforge convert input.png output.png --dpi 300

# Scale by percentage
pixforge convert input.png output.png --scale 50

# Resize to exact width (maintains aspect ratio)
pixforge convert input.png output.png --width 800

# Resize to exact dimensions
pixforge convert input.png output.png --width 800 --height 600

# Rotate (counter-clockwise)
pixforge convert input.png output.png --rotate 90

# Flip
pixforge convert input.png output.png --flip horizontal
pixforge convert input.png output.png --flip vertical

# Grayscale
pixforge convert input.png output.png --grayscale

# Crop (x y width height)
pixforge convert input.png output.png --crop 10 10 200 200

# Chain multiple options
pixforge convert input.png output.webp --scale 50 --quality 80 --grayscale
```

### Batch convert a directory

```bash
# Convert all images in a folder to WebP
pixforge batch ./images/ ./output/ --format webp

# With quality and scale
pixforge batch ./images/ ./output/ --format jpg --quality 80 --scale 75
```

## Options Reference

| Option | Short | Description |
|--------|-------|-------------|
| `--quality` | `-q` | Output quality 1-100 (JPEG/WebP only, default: 85) |
| `--dpi` | `-d` | Set DPI for output image |
| `--scale` | `-s` | Scale by percentage (e.g. 50 for 50%) |
| `--width` | `-W` | Resize to width (maintains aspect ratio if height omitted) |
| `--height` | `-H` | Resize to height (maintains aspect ratio if width omitted) |
| `--rotate` | `-r` | Rotate degrees counter-clockwise |
| `--flip` | `-f` | Flip: `horizontal` or `vertical` |
| `--grayscale` | `-g` | Convert to grayscale |
| `--crop` | `-c` | Crop: x y width height |

## License

MIT
