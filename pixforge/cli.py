import click
from pathlib import Path
from PIL import Image

from .converter import convert, SUPPORTED_FORMATS
from .transforms import resize, crop, rotate, flip, grayscale
from .utils import validate_input, validate_output


@click.group()
@click.version_option()
def main():
    """🔨 pixforge — image conversion and transformation toolkit"""
    pass


@main.command()
@click.argument("input", type=click.Path(exists=True, path_type=Path))
@click.argument("output", type=click.Path(path_type=Path))
@click.option("--quality", "-q", default=85, show_default=True, help="Output quality (1-100, JPEG/WebP only)")
@click.option("--dpi", "-d", default=None, type=int, help="Set DPI (e.g. 300 for print)")
@click.option("--scale", "-s", default=None, type=float, help="Scale by percentage (e.g. 50 for 50%%)")
@click.option("--width", "-W", default=None, type=int, help="Resize to width (maintains aspect ratio if height omitted)")
@click.option("--height", "-H", default=None, type=int, help="Resize to height (maintains aspect ratio if width omitted)")
@click.option("--rotate", "-r", "rotation", default=None, type=int, help="Rotate by degrees (counter-clockwise)")
@click.option("--flip", "-f", "flip_dir", default=None, type=click.Choice(["horizontal", "vertical"]), help="Flip direction")
@click.option("--grayscale", "-g", "to_grayscale", is_flag=True, help="Convert to grayscale")
@click.option("--crop", "-c", nargs=4, type=int, metavar="X Y W H", default=None, help="Crop: x y width height")
def convert_cmd(input, output, quality, dpi, scale, width, height, rotation, flip_dir, to_grayscale, crop):
    """Convert and transform a single image."""
    validate_input(input)
    validate_output(output)

    img = Image.open(input)
    click.echo(f"📂 Input:  {input} ({img.size[0]}x{img.size[1]}, {img.mode})")

    # Apply transforms
    if scale or width or height:
        img = resize(img, width, height, scale)
        click.echo(f"📐 Resized to {img.size[0]}x{img.size[1]}")

    if crop:
        x, y, w, h = crop
        img = globals()["crop"](img, x, y, w, h) if False else __import__("pixforge.transforms", fromlist=["crop"]).crop(img, x, y, w, h)
        click.echo(f"✂️  Cropped to {img.size[0]}x{img.size[1]}")

    if rotation:
        img = rotate(img, rotation)
        click.echo(f"🔄 Rotated {rotation}°")

    if flip_dir:
        img = flip(img, flip_dir)
        click.echo(f"🔁 Flipped {flip_dir}")

    if to_grayscale:
        img = grayscale(img)
        click.echo("🎨 Converted to grayscale")

    # Save
    from .converter import get_format
    out_format = get_format(output)
    if out_format == "JPEG" and img.mode in ("RGBA", "P", "L"):
        img = img.convert("RGB")

    save_kwargs = {}
    if out_format in ("JPEG", "WEBP"):
        save_kwargs["quality"] = quality
    if dpi:
        save_kwargs["dpi"] = (dpi, dpi)

    output.parent.mkdir(parents=True, exist_ok=True)
    img.save(output, format=out_format, **save_kwargs)
    click.echo(f"✅ Output: {output} ({img.size[0]}x{img.size[1]})")


@main.command()
@click.argument("input_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.argument("output_dir", type=click.Path(path_type=Path))
@click.option("--format", "-F", "out_format", required=True, help="Output format (e.g. webp, jpg, png)")
@click.option("--quality", "-q", default=85, show_default=True, help="Output quality (1-100)")
@click.option("--scale", "-s", default=None, type=float, help="Scale by percentage")
@click.option("--width", "-W", default=None, type=int, help="Resize width")
@click.option("--height", "-H", default=None, type=int, help="Resize height")
@click.option("--grayscale", "-g", "to_grayscale", is_flag=True, help="Convert to grayscale")
def batch(input_dir, output_dir, out_format, quality, scale, width, height, to_grayscale):
    """Batch convert all images in a directory."""
    ext = f".{out_format.lstrip('.')}"
    if ext not in SUPPORTED_FORMATS:
        raise click.BadParameter(f"Unsupported format: {out_format}")

    output_dir.mkdir(parents=True, exist_ok=True)
    files = [f for f in input_dir.iterdir() if f.suffix.lower() in SUPPORTED_FORMATS]

    if not files:
        click.echo("⚠️  No supported images found in input directory.")
        return

    click.echo(f"🔨 Processing {len(files)} image(s)...")
    success, errors = 0, 0

    for f in files:
        try:
            out_path = output_dir / (f.stem + ext)
            img = Image.open(f)

            if scale or width or height:
                img = resize(img, width, height, scale)
            if to_grayscale:
                img = grayscale(img)

            out_f = SUPPORTED_FORMATS[ext]
            if out_f == "JPEG" and img.mode in ("RGBA", "P", "L"):
                img = img.convert("RGB")

            save_kwargs = {}
            if out_f in ("JPEG", "WEBP"):
                save_kwargs["quality"] = quality

            img.save(out_path, format=out_f, **save_kwargs)
            click.echo(f"  ✅ {f.name} → {out_path.name}")
            success += 1
        except Exception as e:
            click.echo(f"  ❌ {f.name}: {e}")
            errors += 1

    click.echo(f"\n🎉 Done! {success} succeeded, {errors} failed.")


@main.command()
@click.option("--port", "-p", default=5000, show_default=True, help="Port to run the GUI on")
@click.option("--debug", is_flag=True, help="Run in debug mode")
def gui(port, debug):
    """Launch the pixforge web GUI in your browser."""
    from pixforge.gui.app import run
    run(port=port, debug=debug)


# alias: `pixforge convert` maps to the convert_cmd
main.add_command(convert_cmd, name="convert")
