import io
from flask import Flask, request, send_file, render_template
from PIL import Image
from pixforge.converter import get_format, SUPPORTED_FORMATS
from pixforge.transforms import resize, crop, rotate, flip, grayscale

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", formats=list(SUPPORTED_FORMATS.keys()))


@app.route("/convert", methods=["POST"])
def convert():
    file = request.files.get("image")
    if not file:
        return {"error": "No image provided"}, 400

    out_format = request.form.get("format", ".jpg").lower()
    if not out_format.startswith("."):
        out_format = f".{out_format}"

    quality = int(request.form.get("quality", 85))
    dpi = request.form.get("dpi")
    dpi = int(dpi) if dpi else None
    scale = request.form.get("scale")
    scale = float(scale) if scale else None
    width = request.form.get("width")
    width = int(width) if width else None
    height = request.form.get("height")
    height = int(height) if height else None
    rotation = request.form.get("rotate")
    rotation = int(rotation) if rotation else None
    flip_dir = request.form.get("flip") or None
    to_grayscale = request.form.get("grayscale") == "true"

    img = Image.open(file.stream)

    # Apply transforms
    if scale or width or height:
        img = resize(img, width, height, scale)
    if rotation:
        img = rotate(img, rotation)
    if flip_dir:
        img = flip(img, flip_dir)
    if to_grayscale:
        img = grayscale(img)

    # Convert mode for JPEG
    pil_format = SUPPORTED_FORMATS.get(out_format, "JPEG")
    if pil_format == "JPEG" and img.mode in ("RGBA", "P", "L"):
        img = img.convert("RGB")

    # Save to buffer
    buf = io.BytesIO()
    save_kwargs = {}
    if pil_format in ("JPEG", "WEBP"):
        save_kwargs["quality"] = quality
    if dpi:
        save_kwargs["dpi"] = (dpi, dpi)
    img.save(buf, format=pil_format, **save_kwargs)
    buf.seek(0)

    # Build output filename
    original_name = file.filename.rsplit(".", 1)[0]
    out_filename = f"{original_name}_converted{out_format}"

    return send_file(
        buf,
        mimetype=f"image/{pil_format.lower()}",
        as_attachment=True,
        download_name=out_filename,
    )


def run(port=5000, debug=False):
    print(f"🔨 pixforge GUI running at http://localhost:{port}")
    app.run(port=port, debug=debug)
