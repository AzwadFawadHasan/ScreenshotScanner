"""
ScreenshotScanner - A heuristic-based tool to detect whether an image is a screenshot.

This package provides functionality to detect if an image (particularly of documents like
passports, IDs, or driver's licenses) is a screenshot rather than a photo of a physical document.
"""

__version__ = "0.1.0"
__author__ = "AzwadFawadHasan"

from .detector import ScreenshotDetector

__all__ = ["ScreenshotDetector"]
