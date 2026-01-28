"""Main screenshot detection module."""

import os
import numpy as np
from PIL import Image
from scipy import signal
import pytesseract
from io import BytesIO
import cv2
from typing import Dict, Union, Tuple


class ScreenshotScanner:
    """
    A heuristic-based detector to identify if an image is a screenshot.
    
    This detector uses multiple heuristics including:
    - Alpha channel detection
    - Aspect ratio analysis
    - Border variance
    - ELA (Error Level Analysis)
    - EXIF data presence
    - Horizontal edge detection
    - Moiré pattern detection
    - Noise analysis
    - Sharpness measurement
    - Solid color ratio
    - Status bar detection
    - Text confidence from OCR
    - Vertical symmetry
    
    Attributes:
        threshold (int): Score threshold for screenshot detection (default: 5)
    """
    
    def __init__(self, threshold: int = 5):
        """
        Initialize the ScreenshotScanner.
        
        Args:
            threshold: Minimum score to classify as screenshot (default: 5)
        """
        self.threshold = threshold
    
    def process(self, image_path: str) -> Dict:
        """
        Process an image to detect if it's a screenshot (simple API).
        
        This is the recommended method for basic usage.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing:
                - is_screenshot (bool): Whether the image is detected as a screenshot
                - score (int): Detection score
                - confidence (float): Confidence percentage
                - reasons (list): List of reasons for detection
                
        Example:
            >>> from screenshot_scanner import ScreenshotScanner
            >>> scanner = ScreenshotScanner()
            >>> result = scanner.process("passport.jpg")
            >>> print(result)
        """
        return self.is_screenshot(image_path, verbose=False)
    
    def is_screenshot(self, image_path: str, verbose: bool = False) -> Dict:
        """
        Detect if an image is a screenshot (advanced API with verbose option).
        
        Args:
            image_path: Path to the image file
            verbose: If True, return detailed metrics
            
        Returns:
            Dictionary containing:
                - is_screenshot (bool): Whether the image is detected as a screenshot
                - score (int): Detection score
                - confidence (float): Confidence percentage
                - reasons (list): List of reasons for detection
                - metrics (dict): Detailed metrics if verbose=True
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Load image
        img = Image.open(image_path)
        
        # Calculate all metrics
        metrics = self._calculate_metrics(img, image_path)
        
        # Calculate score and reasons
        score, reasons = self._calculate_score(metrics)
        
        # Determine if screenshot
        is_screenshot = score >= self.threshold
        confidence = min(100, (score / 10) * 100)
        
        result = {
            "is_screenshot": is_screenshot,
            "score": score,
            "confidence": confidence,
            "reasons": reasons
        }
        
        if verbose:
            result["metrics"] = metrics
        
        return result

    
    def _calculate_metrics(self, img: Image.Image, image_path: str) -> Dict:
        """Calculate all detection metrics."""
        metrics = {}
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # 1. Alpha channel detection
        metrics["alpha"] = img.mode == "RGBA"
        
        # 2. Aspect ratio
        width, height = img.size
        metrics["aspect_ratio"] = round(width / height, 2)
        
        # 3. Border variance
        metrics["border_vars"] = self._calculate_border_variance(img_array)
        
        # 4. ELA (Error Level Analysis)
        metrics["ela_std"] = self._calculate_ela(img, image_path)
        
        # 5. EXIF data
        metrics["exif_level"] = self._check_exif(img)
        
        # 6. Horizontal edge ratio
        metrics["horiz_edge_ratio"] = self._calculate_horizontal_edges(img_array)
        
        # 7. Moiré pattern detection
        metrics["moire_score"] = self._detect_moire(img_array)
        
        # 8. Noise median variance
        metrics["noise_median_var"] = self._calculate_noise(img_array)
        
        # 9. Sharpness
        metrics["sharpness"] = self._calculate_sharpness(img_array)
        
        # 10. Solid color ratio
        metrics["solid_color_ratio"] = self._calculate_solid_color_ratio(img_array)
        
        # 11. Status bar detection
        metrics["status_bar"] = self._detect_status_bar(img_array)
        
        # 12. Text confidence (OCR)
        metrics["text_conf"] = self._calculate_text_confidence(img)
        
        # 13. Vertical symmetry
        metrics["vert_symmetry"] = self._calculate_vertical_symmetry(img_array)
        
        return metrics
    
    def _calculate_score(self, metrics: Dict) -> Tuple[int, list]:
        """Calculate detection score based on metrics."""
        score = 0
        reasons = []
        
        # Alpha channel
        if metrics["alpha"]:
            score += 2
            reasons.append("Has alpha channel")
        
        # Common screenshot aspect ratios
        common_ratios = [1.33, 1.5, 1.6, 1.78, 2.0, 2.16]
        if any(abs(metrics["aspect_ratio"] - r) < 0.05 for r in common_ratios):
            score += 1
            reasons.append(f"Common aspect ratio: {metrics['aspect_ratio']}")
        
        # Low border variance (uniform borders)
        if metrics["border_vars"][0] < 100 and metrics["border_vars"][1] < 100:
            score += 1
            reasons.append(f"Low border variance: {metrics['border_vars']}")
        
        # Low ELA (less compression artifacts)
        if metrics["ela_std"] < 50:
            score += 1
            reasons.append(f"Low ELA: {metrics['ela_std']:.2f}")
        
        # No EXIF data
        if metrics["exif_level"] is None or metrics["exif_level"] == 0:
            score += 1
            reasons.append("No EXIF data")
        
        # Horizontal edges (UI elements)
        if metrics["horiz_edge_ratio"] > 0.3:
            score += 1
            reasons.append(f"High horizontal edges: {metrics['horiz_edge_ratio']:.2f}")
        
        # Low moiré (no screen pattern)
        if metrics["moire_score"] < 50:
            score += 1
            reasons.append(f"Low moiré: {metrics['moire_score']:.2f}")
        
        # Low noise
        if metrics["noise_median_var"] < 10:
            score += 1
            reasons.append(f"Low noise: {metrics['noise_median_var']:.2f}")
        
        # High sharpness
        if metrics["sharpness"] > 100:
            score += 1
            reasons.append(f"High sharpness: {metrics['sharpness']:.2f}")
        
        # High solid color ratio
        if metrics["solid_color_ratio"] > 0.5:
            score += 1
            reasons.append(f"High solid color: {metrics['solid_color_ratio']:.2f}")
        
        # Status bar detected
        if metrics["status_bar"]:
            score += 2
            reasons.append("Status bar detected")
        
        # High text confidence
        if metrics["text_conf"] > 70:
            score += 1
            reasons.append(f"High text confidence: {metrics['text_conf']:.2f}")
        
        # High vertical symmetry
        if metrics["vert_symmetry"] > 0.8:
            score += 1
            reasons.append(f"High vertical symmetry: {metrics['vert_symmetry']:.2f}")
        
        return score, reasons
    
    def _calculate_border_variance(self, img_array: np.ndarray) -> Tuple[float, float]:
        """Calculate variance of top and side borders."""
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        height, width = gray.shape
        border_size = min(20, height // 20, width // 20)
        
        top_border = gray[:border_size, :]
        side_border = np.concatenate([gray[:, :border_size], gray[:, -border_size:]], axis=1)
        
        return (float(np.var(top_border)), float(np.var(side_border)))
    
    def _calculate_ela(self, img: Image.Image, image_path: str) -> float:
        """Calculate Error Level Analysis standard deviation."""
        try:
            # Save with quality 90
            temp_path = image_path + ".temp.jpg"
            img.convert("RGB").save(temp_path, "JPEG", quality=90)
            
            # Load both images
            original = np.array(img.convert("RGB"))
            compressed = np.array(Image.open(temp_path))
            
            # Calculate difference
            diff = np.abs(original.astype(float) - compressed.astype(float))
            ela_std = float(np.std(diff))
            
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return ela_std
        except Exception:
            return 0.0
    
    def _check_exif(self, img: Image.Image) -> Union[int, None]:
        """Check for EXIF data."""
        try:
            exif = img._getexif()
            return len(exif) if exif else None
        except Exception:
            return None
    
    def _calculate_horizontal_edges(self, img_array: np.ndarray) -> float:
        """Calculate ratio of horizontal edges."""
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Sobel edge detection
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # Calculate edge strength
        horiz_edges = np.sum(np.abs(sobely))
        total_edges = np.sum(np.abs(sobelx)) + np.sum(np.abs(sobely))
        
        return float(horiz_edges / total_edges) if total_edges > 0 else 0.0
    
    def _detect_moire(self, img_array: np.ndarray) -> float:
        """Detect moiré patterns (common in photos of screens)."""
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # FFT to detect periodic patterns
        f_transform = np.fft.fft2(gray)
        f_shift = np.fft.fftshift(f_transform)
        magnitude = np.abs(f_shift)
        
        # High frequency content indicates moiré
        center_y, center_x = magnitude.shape[0] // 2, magnitude.shape[1] // 2
        mask_size = min(center_y, center_x) // 4
        
        # Exclude center (DC component)
        magnitude[center_y-mask_size:center_y+mask_size, 
                  center_x-mask_size:center_x+mask_size] = 0
        
        return float(np.mean(magnitude))
    
    def _calculate_noise(self, img_array: np.ndarray) -> float:
        """Calculate noise level using median filter."""
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Apply median filter
        median = cv2.medianBlur(gray, 5)
        
        # Calculate difference
        noise = gray.astype(float) - median.astype(float)
        
        return float(np.var(noise))
    
    def _calculate_sharpness(self, img_array: np.ndarray) -> float:
        """Calculate image sharpness using Laplacian variance."""
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        
        return float(np.var(laplacian))
    
    def _calculate_solid_color_ratio(self, img_array: np.ndarray) -> float:
        """Calculate ratio of solid color regions."""
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Find regions with low variance
        kernel_size = 10
        local_var = signal.convolve2d(
            gray.astype(float), 
            np.ones((kernel_size, kernel_size)) / (kernel_size ** 2),
            mode='same'
        )
        
        solid_pixels = np.sum(local_var < 5)
        total_pixels = gray.size
        
        return float(solid_pixels / total_pixels)
    
    def _detect_status_bar(self, img_array: np.ndarray) -> bool:
        """Detect presence of status bar (common in mobile screenshots)."""
        height, width = img_array.shape[:2]
        status_bar_height = min(100, height // 10)
        
        # Check top region
        top_region = img_array[:status_bar_height, :]
        
        if len(top_region.shape) == 3:
            gray_top = cv2.cvtColor(top_region, cv2.COLOR_RGB2GRAY)
        else:
            gray_top = top_region
        
        # Status bars typically have low variance and specific height
        variance = np.var(gray_top)
        
        return variance < 500 and status_bar_height > 20
    
    def _calculate_text_confidence(self, img: Image.Image) -> float:
        """Calculate OCR confidence (screenshots usually have clear text)."""
        try:
            # Run OCR
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
            
            # Calculate average confidence
            confidences = [int(conf) for conf in data['conf'] if conf != '-1']
            
            return float(np.mean(confidences)) if confidences else 0.0
        except Exception:
            return 0.0
    
    def _calculate_vertical_symmetry(self, img_array: np.ndarray) -> float:
        """Calculate vertical symmetry (screenshots often have symmetric layouts)."""
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        height, width = gray.shape
        mid = width // 2
        
        left_half = gray[:, :mid]
        right_half = np.fliplr(gray[:, -mid:])
        
        # Resize to match if needed
        min_width = min(left_half.shape[1], right_half.shape[1])
        left_half = left_half[:, :min_width]
        right_half = right_half[:, :min_width]
        
        # Calculate correlation
        correlation = np.corrcoef(left_half.flatten(), right_half.flatten())[0, 1]
        
        return float(max(0, correlation))
