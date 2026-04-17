from pathlib import Path
from PIL import Image
import pytest
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from pixforge.transforms import resize, crop, rotate, flip, grayscale


def make_img(size=(200, 100), mode="RGB"):
    return Image.new(mode, size, color=(100, 150, 200))


def test_resize_by_scale():
    img = make_img((200, 100))
    out = resize(img, None, None, scale=50)
    assert out.size == (100, 50)


def test_resize_by_width_maintains_aspect_ratio():
    img = make_img((200, 100))
    out = resize(img, width=100, height=None, scale=None)
    assert out.size == (100, 50)


def test_resize_by_height_maintains_aspect_ratio():
    img = make_img((200, 100))
    out = resize(img, width=None, height=50, scale=None)
    assert out.size == (100, 50)


def test_resize_exact():
    img = make_img((200, 100))
    out = resize(img, width=300, height=400, scale=None)
    assert out.size == (300, 400)


def test_resize_no_op():
    img = make_img((200, 100))
    out = resize(img, None, None, None)
    assert out.size == (200, 100)


def test_crop():
    img = make_img((200, 100))
    out = crop(img, 10, 10, 50, 50)
    assert out.size == (50, 50)


def test_rotate():
    img = make_img((200, 100))
    out = rotate(img, 90)
    assert out.size == (100, 200)


def test_flip_horizontal():
    img = make_img()
    out = flip(img, "horizontal")
    assert out.size == img.size


def test_flip_vertical():
    img = make_img()
    out = flip(img, "vertical")
    assert out.size == img.size


def test_grayscale():
    img = make_img()
    out = grayscale(img)
    assert out.mode == "L"
