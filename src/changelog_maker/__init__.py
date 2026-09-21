"""changelog-maker: deterministic changelog generation from Git history."""
from .core import Commit, parse_commit, render

__version__ = "1.0.0"
__author__ = "Radwan Abdulhadi Ahmed (@rad03i2)"
__all__ = ["Commit", "parse_commit", "render"]
