"""Shared filesystem locations for the tusopen pipeline (plan §3, §6.1)."""
from pathlib import Path


def repo_root() -> Path:
    """Project root (src/tusopen/paths.py -> src/tusopen -> src -> repo)."""
    return Path(__file__).resolve().parents[2]


def default_cache() -> Path:
    """Local cache for fetched PDFs and parsed text; never committed (plan §6.1)."""
    return Path.home() / ".tusopen" / "cache"
