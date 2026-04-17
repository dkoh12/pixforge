"""Image transformation functions for pixforge."""

from PIL import Image

_LANCZOS = Image.Resampling.LANCZOS


def resize(
    img: Image.Image,
    width: int | None,
    height: int | None,
    scale: float | None,
) -> Image.Image:
    """Resize image.


    Scale takes priority. Width/height maintain aspect ratio if only one is given.
    """
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

    return img.resize((new_w, new_h), _LANCZOS)


def crop(img: Image.Image, x: int, y: int, width: int, height: int) -> Image.Image:
    """Crop image to a box starting at (x, y) with given width and height."""
    return img.crop((x, y, x + width, y + height))


def rotate(img: Image.Image, degrees: int) -> Image.Image:
    """Rotate image by degrees (counter-clockwise), expanding canvas to fit."""
    return img.rotate(degrees, expand=True)


def flip(img: Image.Image, direction: str) -> Image.Image:
    """Flip image horizontally or vertically."""
    if direction == "horizontal":
        return img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if direction == "vertical":
        return img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    raise ValueError(f"Invalid flip direction: {direction!r}. Use 'horizontal' or 'vertical'.")


def grayscale(img: Image.Image) -> Image.Image:
    """Convert image to grayscale."""
    return img.convert("L")


def apply_transforms(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    img: Image.Image,
    scale=None,
    width=None,
    height=None,
    crop_box=None,
    rotation=None,
    flip_dir=None,
    to_grayscale=False,
) -> Image.Image:
    """Apply all requested transforms to an image in a consistent order."""
    if scale or width or height:
        img = resize(img, width, height, scale)
    if crop_box:
        crop_x, crop_y, crop_w, crop_h = crop_box
        img = img.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
    if rotation:
        img = rotate(img, rotation)
    if flip_dir:
        img = flip(img, flip_dir)
    if to_grayscale:
        img = grayscale(img)
    return img
