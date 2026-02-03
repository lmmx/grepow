"""
grepow: sparse-checkout repos from grep.app search results.

Usage:
    grepow "some_function" ./repos
    grepow "impl.*Trait" ./repos --full
"""

from .cli import main

__all__ = ["main"]
