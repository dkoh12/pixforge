from pathlib import Path
from PIL import Image
import pytest
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from pixforge.converter import convert, get_format
from pixforge.transforms import resize, crop, rotate, flip, grayscale


SAMPLE_DIR = Path(__file__).parent / "sample_images"
SAMPLE_DIR.mkdir(exist_ok=True)


def make_test_image(path: Path, size=(100, 100), mode="RGB"):
    img = Image.new(mode, size, color=(255, 100, 50))
    img.save(path)
    return path


def test_get_format():
    assert get_format(Path("test.png")) == "PNG"
    assert get_format(Path("test.jpg")) == "JPEG"
    assert get_format(Path("test.webp")) == "WEBP"


def test_convert_png_to_jpeg(tmp_path):
    src = make_test_image(tmp_path / "test.png")
    dst = tmp_path / "out.jpg"
    convert(src, dst)
    assert dst.exists()
    img = Image.open(dst)
    assert img.format == "JPEG"


def test_convert_with_quality(tmp_path):
    src = make_test_image(tmp_path / "test.png")
    dst_high = tmp_path / "high.jpg"
    dst_low = tmp_path / "low.jpg"
    convert(src, dst_high, quality=95)
    convert(src, dst_low, quality=10)
    assert dst_high.stat().st_size > dst_low.stat().st_size


def test_convert_rgba_to_jpeg(tmp_path):
    src = tmp_path / "rgba.png"
    img = Image.new("RGBA", (100, 100), (255, 0, 0, 128))
    img.save(src)
    dst = tmp_path / "out.jpg"
    convert(src, dst)
    assert dst.exists()


def test_convert_with_dpi(tmp_path):
    src = make_test_image(tmp_path / "test.png")
    dst = tmp_path / "out.png"
    convert(src, dst, dpi=300)
    assert dst.exists()
