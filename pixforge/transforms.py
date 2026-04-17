from PIL import Image


def resize(img: Image.Image, width: int | None, height: int | None, scale: float | None) -> Image.Image:
    """Resize image. Scale takes priority. Width/height maintain aspect ratio if only one is given."""
    orig_w, orig_h = img.size

    if scale is not None:
        new_w = int(orig_w * scale / 100)
        new_h = int(orig_h * scale / 100)
    elif width and height:
        new_w, new_h = width, height
    elif width:
        new_w = width
        new_h = int(orig_h * (width / orig_w))
    elif height:
        new_h = height
        new_w = int(orig_w * (height / orig_h))
    else:
        return img  # no resize requested

    return img.resize((new_w, new_h), Image.LANCZOS)


def crop(img: Image.Image, x: int, y: int, width: int, height: int) -> Image.Image:
    """Crop image to a box starting at (x, y) with given width and height."""
    return img.crop((x, y, x + width, y + height))


def rotate(img: Image.Image, degrees: int) -> Image.Image:
    """Rotate image by degrees (counter-clockwise), expanding canvas to fit."""
    return img.rotate(degrees, expand=True)


def flip(img: Image.Image, direction: str) -> Image.Image:
    """Flip image horizontally or vertically."""
    if direction == "horizontal":
        return img.transpose(Image.FLIP_LEFT_RIGHT)
    elif direction == "vertical":
        return img.transpose(Image.FLIP_TOP_BOTTOM)
    raise ValueError(f"Invalid flip direction: {direction}. Use 'horizontal' or 'vertical'.")


def grayscale(img: Image.Image) -> Image.Image:
    """Convert image to grayscale."""
    return img.convert("L")
