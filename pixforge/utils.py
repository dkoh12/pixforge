from pathlib import Path
from .converter import SUPPORTED_FORMATS


def validate_input(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    if path.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported input format: {path.suffix}")


def validate_output(path: Path) -> None:
    if path.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported output format: {path.suffix}")
