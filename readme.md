# ScreenshotScanner

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/ScreenshotScanner.svg?logo=pypi&logoColor=959DA5&color=blue)](https://pypi.org/project/ScreenshotScanner/)
[![Downloads](https://static.pepy.tech/badge/ScreenshotScanner)](https://pypistats.org/packages/screenshotscanner)
[![CodeQL](https://github.com/AzwadFawadHasan/ScreenshotScanner/actions/workflows/codeql.yml/badge.svg)](https://github.com/AzwadFawadHasan/ScreenshotScanner/actions/workflows/codeql.yml)

A heuristic-based tool to detect whether an image is a screenshot or a photo of a physical document.



##  Features

- **13 Heuristic Checks** - Multiple detection methods for high accuracy
- **Simple API** - Easy to integrate into existing workflows
- **Detailed Metrics** - Optional verbose mode for debugging
- **No Training Required** - Rule-based system, no ML models needed
- **Fast Processing** - Analyze images in milliseconds

## Installation

### Basic Installation

```bash
pip install ScreenshotScanner
```


## Quick Start

```python
from screenshot_scanner import ScreenshotScanner

# Initialize scanner
scanner = ScreenshotScanner()

# Process an image (simple one-liner)
result = scanner.process("path/to/image.jpg")

print(result)
```

### Example Output

```python
{
    'is_screenshot': True,
    'score': 8,
    'confidence': 80.0,
    'reasons': ['Has alpha channel', 'Common aspect ratio: 1.78', 'Low ELA: 45.32', 'No EXIF data', 'High sharpness: 156.23']
}
```

**That's it!** Just 3 lines of code to detect screenshots.

<!-- 
## 📖 Advanced Usage

### Accessing Detailed Information

```python
result = scanner.process("image.jpg")

# Access individual fields
if result['is_screenshot']:
    print(f"Screenshot detected with {result['confidence']:.1f}% confidence")
    print(f"Detection score: {result['score']}/10")
    print("Reasons:")
    for reason in result['reasons']:
        print(f"  - {reason}")
```

### Verbose Mode (All Metrics)

For debugging or detailed analysis, use `is_screenshot()` with `verbose=True`:

```python
result = scanner.is_screenshot("image.jpg", verbose=True)

# Access detailed metrics
metrics = result['metrics']
print(f"Alpha channel: {metrics['alpha']}")
print(f"Aspect ratio: {metrics['aspect_ratio']}")
print(f"ELA std: {metrics['ela_std']}")
print(f"Sharpness: {metrics['sharpness']}")
# ... and 9 more metrics
```

### Custom Threshold

Adjust the detection sensitivity:

```python
# More strict (fewer false positives)
strict_scanner = ScreenshotScanner(threshold=7)

# More lenient (fewer false negatives)
lenient_scanner = ScreenshotScanner(threshold=3)

result = strict_scanner.process("image.jpg")
```

### Batch Processing

Process multiple images:

```python
import os
from screenshot_scanner import ScreenshotScanner

scanner = ScreenshotScanner()
image_folder = "path/to/images"

for filename in os.listdir(image_folder):
    if filename.endswith(('.jpg', '.png', '.jpeg')):
        image_path = os.path.join(image_folder, filename)
        result = scanner.process(image_path)
        print(f"{filename}: {result['is_screenshot']} (score: {result['score']})")
``` -->

## How It Works

ScreenshotScanner uses 13 different heuristic checks to determine if an image is a screenshot:

1. **Alpha Channel** - Screenshots often have transparency
2. **Aspect Ratio** - Common screen ratios (16:9, 4:3, etc.)
3. **Border Variance** - Uniform borders indicate screenshots
4. **ELA (Error Level Analysis)** - Lower compression artifacts in screenshots
5. **EXIF Data** - Screenshots typically lack camera metadata
6. **Horizontal Edges** - UI elements create horizontal patterns
7. **Moiré Patterns** - Photos of screens show moiré, screenshots don't
8. **Noise Analysis** - Screenshots have less sensor noise
9. **Sharpness** - Screenshots are typically sharper
10. **Solid Color Ratio** - UI elements have more solid colors
11. **Status Bar Detection** - Mobile screenshots often have status bars
12. **Text Confidence** - OCR works better on screenshot text
13. **Vertical Symmetry** - UI layouts are often symmetric

Each check contributes to a final score. A score ≥ 5 (default threshold) indicates a screenshot.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Motivation

- There is no good tool without ML to detect screenshots. So i decided to come up with this.

## Contact

- **Author**: AzwadFawadHasan
- **GitHub**: [@AzwadFawadHasan](https://github.com/AzwadFawadHasan)
- **Issues**: [GitHub Issues](https://github.com/AzwadFawadHasan/ScreenshotScanner/issues)

## Star

If you find this project useful, please consider giving it a star on GitHub!

---

Made with ❤️ for better document verification by AzwadFawadHasan
