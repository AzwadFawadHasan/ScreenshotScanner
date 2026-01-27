# ScreenshotScanner

[![PyPI version](https://badge.fury.io/py/ScreenshotScanner.svg)](https://badge.fury.io/py/ScreenshotScanner)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A heuristic-based tool to detect whether an image is a screenshot or a photo of a physical document.

## 🎯 Use Cases

ScreenshotScanner is particularly effective at detecting if images of identity documents are screenshots rather than photos of physical documents:

- **Passport verification** - Detect screenshot submissions vs. real passport photos
- **ID card validation** - Verify driver's licenses and national ID cards
- **Document authentication** - Prevent fraudulent screenshot submissions
- **KYC/AML compliance** - Enhance identity verification processes

## ✨ Features

- **13 Heuristic Checks** - Multiple detection methods for high accuracy
- **Simple API** - Easy to integrate into existing workflows
- **Detailed Metrics** - Optional verbose mode for debugging
- **No Training Required** - Rule-based system, no ML models needed
- **Fast Processing** - Analyze images in milliseconds

## 📦 Installation

### Basic Installation

```bash
pip install ScreenshotScanner
```

### System Requirements

ScreenshotScanner requires **Tesseract-OCR** to be installed on your system for text confidence analysis.

**Windows:**
```bash
# Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
# Or use chocolatey:
choco install tesseract
```

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

## 🚀 Quick Start

```python
from screenshot_scanner import ScreenshotDetector

# Initialize detector
detector = ScreenshotDetector()

# Check if an image is a screenshot
result = detector.is_screenshot("path/to/image.jpg")

print(f"Is screenshot: {result['is_screenshot']}")
print(f"Confidence: {result['confidence']:.1f}%")
print(f"Score: {result['score']}/10")
print(f"Reasons: {', '.join(result['reasons'])}")
```

### Example Output

```python
Is screenshot: True
Confidence: 80.0%
Score: 8/10
Reasons: Has alpha channel, Common aspect ratio: 1.78, Low ELA: 45.32, No EXIF data, High sharpness: 156.23
```

## 📖 Advanced Usage

### Verbose Mode

Get detailed metrics for all heuristic checks:

```python
result = detector.is_screenshot("image.jpg", verbose=True)

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
strict_detector = ScreenshotDetector(threshold=7)

# More lenient (fewer false negatives)
lenient_detector = ScreenshotDetector(threshold=3)
```

### Batch Processing

Process multiple images:

```python
import os
from screenshot_scanner import ScreenshotDetector

detector = ScreenshotDetector()
image_folder = "path/to/images"

for filename in os.listdir(image_folder):
    if filename.endswith(('.jpg', '.png', '.jpeg')):
        image_path = os.path.join(image_folder, filename)
        result = detector.is_screenshot(image_path)
        print(f"{filename}: {result['is_screenshot']} (score: {result['score']})")
```

## 🔍 How It Works

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

### Development Setup

```bash
# Clone the repository
git clone https://github.com/AzwadFawadHasan/ScreenshotScanner.git
cd ScreenshotScanner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with OpenCV, NumPy, SciPy, Pillow, and pytesseract
- Inspired by the need for better document verification in KYC processes

## 📧 Contact

- **Author**: AzwadFawadHasan
- **GitHub**: [@AzwadFawadHasan](https://github.com/AzwadFawadHasan)
- **Issues**: [GitHub Issues](https://github.com/AzwadFawadHasan/ScreenshotScanner/issues)

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

Made with ❤️ for better document verification
