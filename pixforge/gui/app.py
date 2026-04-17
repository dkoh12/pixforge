"""Flask web GUI for pixforge image conversion."""

import io

from flask import Flask, request, send_file, render_template, jsonify
from PIL import Image

from pixforge.converter import build_save_kwargs, prepare_for_save, SUPPORTED_FORMATS
from pixforge.transforms import apply_transforms

app = Flask(__name__)

MAX_UPLOAD_BYTES = 50 * 1024 * 1024  # 50 MB


def _parse_int(value: str | None) -> int | None:
    """Parse a string to int, returning None if empty or invalid."""
    try:
        return int(value) if value else None
    except ValueError:
        return None


def _parse_float(value: str | None) -> float | None:
    """Parse a string to float, returning None if empty or invalid."""
    try:
        return float(value) if value else None
    except ValueError:
        return None


@app.route("/")
def index():
    """Render the main GUI page."""
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():  # pylint: disable=too-many-locals
    """Accept an uploaded image, apply transforms, and return the converted file."""
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No image provided"}), 400

    # Validate file size
    file.stream.seek(0, 2)
    size = file.stream.tell()
    file.stream.seek(0)
    if size > MAX_UPLOAD_BYTES:
        max_mb = MAX_UPLOAD_BYTES // 1024 // 1024
        return jsonify({"error": f"File too large (max {max_mb} MB)"}), 413

    # Validate output format
    out_ext = request.form.get("format", ".jpg").lower()
    if not out_ext.startswith("."):
        out_ext = f".{out_ext}"
    if out_ext not in SUPPORTED_FORMATS:
        return jsonify({"error": f"Unsupported format: {out_ext}"}), 400

    quality = _parse_int(request.form.get("quality")) or 85
    dpi = _parse_int(request.form.get("dpi"))
    scale = _parse_float(request.form.get("scale"))
    width = _parse_int(request.form.get("width"))
    height = _parse_int(request.form.get("height"))
    rotation = _parse_int(request.form.get("rotate"))
    flip_dir = request.form.get("flip") or None
    to_grayscale = request.form.get("grayscale") == "true"

    try:
        img = Image.open(file.stream)
    except (OSError, ValueError):
        return jsonify({"error": "Could not open image — file may be corrupt or unsupported"}), 400

    img = apply_transforms(img, scale, width, height, rotation=rotation,
                           flip_dir=flip_dir, to_grayscale=to_grayscale)

    pil_format = SUPPORTED_FORMATS[out_ext]
    img = prepare_for_save(img, pil_format)

    buf = io.BytesIO()
    img.save(buf, format=pil_format, **build_save_kwargs(pil_format, quality, dpi))
    buf.seek(0)

    original_name = file.filename.rsplit(".", 1)[0]
    out_filename = f"{original_name}_converted{out_ext}"

    return send_file(
        buf,
        mimetype=f"image/{pil_format.lower()}",
        as_attachment=True,
        download_name=out_filename,
    )


def run(port: int = 5000, debug: bool = False) -> None:
    """Start the Flask development server."""
    print(f"🔨 pixforge GUI running at http://localhost:{port}")
    app.run(port=port, debug=debug)
