"""Image format conversion utilities for pixforge."""

from pathlib import Path

from PIL import Image

SUPPORTED_FORMATS = {
    ".png": "PNG",
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".webp": "WEBP",
    ".avif": "AVIF",
    ".gif": "GIF",
    ".tiff": "TIFF",
    ".tif": "TIFF",
    ".bmp": "BMP",
}

# Formats that support lossy quality setting
QUALITY_FORMATS = {"JPEG", "WEBP"}

# Modes incompatible with JPEG (no alpha, no palette)
JPEG_INCOMPATIBLE_MODES = {"RGBA", "P", "LA", "PA"}


def get_format(path: Path) -> str:
    """Return the Pillow format string for a given file path."""
    ext = path.suffix.lower()
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format: {ext}. Supported: {', '.join(SUPPORTED_FORMATS)}")
    return SUPPORTED_FORMATS[ext]


def prepare_for_save(img: Image.Image, pil_format: str) -> Image.Image:
    """Ensure image mode is compatible with the target format."""
    if pil_format == "JPEG" and img.mode in JPEG_INCOMPATIBLE_MODES:
        return img.convert("RGB")
    return img


def build_save_kwargs(pil_format: str, quality: int, dpi: int | None) -> dict:
    """Build keyword arguments for Pillow's save() method."""
    kwargs = {}
    if pil_format in QUALITY_FORMATS:
        kwargs["quality"] = quality
    if dpi:
        kwargs["dpi"] = (dpi, dpi)
    return kwargs


def convert(
    input_path: Path,
    output_path: Path,
    quality: int = 85,
    dpi: int | None = None,
) -> None:
    """Convert an image to a different format with optional quality and DPI settings."""
    img = Image.open(input_path)
    out_format = get_format(output_path)
    img = prepare_for_save(img, out_format)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, format=out_format, **build_save_kwargs(out_format, quality, dpi))
