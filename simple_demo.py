"""
Simplest possible usage example!
"""

from screenshot_scanner import ScreenshotScanner
# from screenshot_scanner.scanner import ScreenshotScanner

# That's it! Just 3 lines!
scanner = ScreenshotScanner()
result = scanner.process(f"test_data/False/20260115_153409.jpg")
print(result)
