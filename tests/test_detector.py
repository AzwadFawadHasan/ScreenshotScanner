"""Unit tests for ScreenshotScanner."""

import unittest
import os
from screenshot_scanner import ScreenshotScanner


class TestScreenshotScanner(unittest.TestCase):
    """Test cases for ScreenshotScanner class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scanner = ScreenshotScanner()
    
    def test_initialization(self):
        """Test scanner initialization."""
        self.assertEqual(self.scanner.threshold, 5)
        
        custom_scanner = ScreenshotScanner(threshold=7)
        self.assertEqual(custom_scanner.threshold, 7)
    
    def test_process_returns_dict(self):
        """Test that process returns a dictionary with required keys."""
        # This test requires a sample image in test_data folder
        test_image = os.path.join("..", "test_data", "sample_image.jpg")
        
        if os.path.exists(test_image):
            result = self.scanner.process(test_image)
            
            self.assertIsInstance(result, dict)
            self.assertIn('is_screenshot', result)
            self.assertIn('score', result)
            self.assertIn('confidence', result)
            self.assertIn('reasons', result)
            
            self.assertIsInstance(result['is_screenshot'], bool)
            self.assertIsInstance(result['score'], int)
            self.assertIsInstance(result['confidence'], float)
            self.assertIsInstance(result['reasons'], list)
    
    def test_verbose_mode(self):
        """Test verbose mode returns metrics."""
        test_image = os.path.join("..", "test_data", "sample_image.jpg")
        
        if os.path.exists(test_image):
            result = self.scanner.is_screenshot(test_image, verbose=True)
            
            self.assertIn('metrics', result)
            self.assertIsInstance(result['metrics'], dict)
            
            # Check for expected metrics
            expected_metrics = [
                'alpha', 'aspect_ratio', 'border_vars', 'ela_std',
                'exif_level', 'horiz_edge_ratio', 'moire_score',
                'noise_median_var', 'sharpness', 'solid_color_ratio',
                'status_bar', 'text_conf', 'vert_symmetry'
            ]
            
            for metric in expected_metrics:
                self.assertIn(metric, result['metrics'])
    
    def test_file_not_found(self):
        """Test handling of non-existent file."""
        with self.assertRaises(FileNotFoundError):
            self.scanner.process("nonexistent_file.jpg")
    
    def test_score_range(self):
        """Test that score is within valid range."""
        test_image = os.path.join("..", "test_data", "sample_image.jpg")
        
        if os.path.exists(test_image):
            result = self.scanner.process(test_image)
            
            self.assertGreaterEqual(result['score'], 0)
            self.assertLessEqual(result['score'], 15)  # Max possible score
    
    def test_confidence_range(self):
        """Test that confidence is within valid range."""
        test_image = os.path.join("..", "test_data", "sample_image.jpg")
        
        if os.path.exists(test_image):
            result = self.scanner.process(test_image)
            
            self.assertGreaterEqual(result['confidence'], 0)
            self.assertLessEqual(result['confidence'], 100)


if __name__ == '__main__':
    unittest.main()
