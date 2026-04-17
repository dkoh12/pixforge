from PIL import Image
from pathlib import Path

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


def get_format(path: Path) -> str:
    ext = path.suffix.lower()
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format: {ext}. Supported: {', '.join(SUPPORTED_FORMATS)}")
    return SUPPORTED_FORMATS[ext]


def convert(
    input_path: Path,
    output_path: Path,
    quality: int = 85,
    dpi: int | None = None,
) -> None:
    """Convert an image to a different format with optional quality and DPI settings."""
    img = Image.open(input_path)

    # Convert RGBA -> RGB if saving to JPEG (no alpha support)
    out_format = get_format(output_path)
    if out_format == "JPEG" and img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    save_kwargs = {}
    if out_format in ("JPEG", "WEBP"):
        save_kwargs["quality"] = quality
    if dpi:
        save_kwargs["dpi"] = (dpi, dpi)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, format=out_format, **save_kwargs)
