"""Basic usage example for ScreenshotScanner."""

from screenshot_scanner import ScreenshotDetector
import os

def main():
    # Initialize the detector
    detector = ScreenshotDetector()
    
    # Example 1: Check a single image
    print("=" * 60)
    print("Example 1: Single Image Detection")
    print("=" * 60)
    
    # Replace with your image path
    image_path = "../test_data/sample_image.jpg"
    
    if os.path.exists(image_path):
        result = detector.is_screenshot(image_path)
        
        print(f"\nImage: {image_path}")
        print(f"Is Screenshot: {result['is_screenshot']}")
        print(f"Confidence: {result['confidence']:.1f}%")
        print(f"Score: {result['score']}/10")
        print(f"\nReasons:")
        for reason in result['reasons']:
            print(f"  - {reason}")
    else:
        print(f"Image not found: {image_path}")
    
    # Example 2: Verbose mode with detailed metrics
    print("\n" + "=" * 60)
    print("Example 2: Verbose Mode (Detailed Metrics)")
    print("=" * 60)
    
    if os.path.exists(image_path):
        result = detector.is_screenshot(image_path, verbose=True)
        
        print(f"\nDetailed Metrics:")
        for metric, value in result['metrics'].items():
            print(f"  {metric}: {value}")
    
    # Example 3: Custom threshold
    print("\n" + "=" * 60)
    print("Example 3: Custom Threshold")
    print("=" * 60)
    
    strict_detector = ScreenshotDetector(threshold=7)
    lenient_detector = ScreenshotDetector(threshold=3)
    
    if os.path.exists(image_path):
        strict_result = strict_detector.is_screenshot(image_path)
        lenient_result = lenient_detector.is_screenshot(image_path)
        
        print(f"\nStrict detector (threshold=7): {strict_result['is_screenshot']}")
        print(f"Lenient detector (threshold=3): {lenient_result['is_screenshot']}")
    
    # Example 4: Batch processing
    print("\n" + "=" * 60)
    print("Example 4: Batch Processing")
    print("=" * 60)
    
    test_folder = "../test_data"
    if os.path.exists(test_folder):
        print(f"\nProcessing images in: {test_folder}\n")
        
        for filename in os.listdir(test_folder):
            if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
                filepath = os.path.join(test_folder, filename)
                result = detector.is_screenshot(filepath)
                
                status = "✓ Screenshot" if result['is_screenshot'] else "✗ Not Screenshot"
                print(f"{filename:30s} {status:20s} Score: {result['score']}/10")
    else:
        print(f"Test folder not found: {test_folder}")

if __name__ == "__main__":
    main()
