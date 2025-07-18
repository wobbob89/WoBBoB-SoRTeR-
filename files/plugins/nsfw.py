"""
Production-ready NSFW detection plugin using NudeNet.
NudeNet is an open-source, MIT-licensed library for detecting NSFW content.
"""

import os
import logging
from typing import Optional, Dict, Any

try:
    from nudenet import NudeDetector
    NUDENET_AVAILABLE = True
except ImportError:
    NUDENET_AVAILABLE = False
    logging.warning("NudeNet not available. NSFW detection will be disabled.")

# Configure logging
logger = logging.getLogger(__name__)

class NSFWDetector:
    """Production-ready NSFW detector using NudeNet."""
    
    def __init__(self):
        self.detector = None
        self.initialized = False
        self._initialize()
    
    def _initialize(self):
        """Initialize the NudeNet detector."""
        if not NUDENET_AVAILABLE:
            logger.error("NudeNet is not available. Please install it with: pip install nudenet")
            return
        
        try:
            self.detector = NudeDetector()
            self.initialized = True
            logger.info("NudeNet NSFW detector initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize NudeNet detector: {e}")
            self.initialized = False
    
    def is_nsfw(self, image_path: str, threshold: float = 0.6) -> bool:
        """
        Detect if an image contains NSFW content.
        
        Args:
            image_path: Path to the image file
            threshold: Confidence threshold (0.0-1.0) for NSFW detection
            
        Returns:
            bool: True if NSFW content is detected, False otherwise
        """
        if not self.initialized:
            logger.warning("NSFW detector not initialized. Returning False.")
            return False
        
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return False
        
        try:
            # Detect NSFW content
            results = self.detector.detect(image_path)
            
            # Check if any detected objects exceed the threshold
            for result in results:
                if result.get('score', 0) > threshold:
                    class_name = result.get('class', '').lower()
                    # Consider these classes as NSFW
                    nsfw_classes = ['exposed_anus', 'exposed_armpits', 'exposed_belly', 
                                  'exposed_breast_f', 'exposed_breast_m', 'exposed_buttocks',
                                  'exposed_genitalia_f', 'exposed_genitalia_m', 'exposed_thighs_f',
                                  'exposed_thighs_m']
                    
                    if class_name in nsfw_classes:
                        logger.debug(f"NSFW content detected in {image_path}: {class_name} (score: {result.get('score', 0):.3f})")
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error detecting NSFW content in {image_path}: {e}")
            return False
    
    def get_detection_details(self, image_path: str) -> Dict[str, Any]:
        """
        Get detailed NSFW detection results for debugging/analysis.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dict containing detection results or error information
        """
        if not self.initialized:
            return {"error": "NSFW detector not initialized"}
        
        if not os.path.exists(image_path):
            return {"error": f"Image file not found: {image_path}"}
        
        try:
            results = self.detector.detect(image_path)
            return {
                "image_path": image_path,
                "detections": results,
                "is_nsfw": self.is_nsfw(image_path)
            }
        except Exception as e:
            return {"error": f"Error detecting NSFW content: {e}"}

# Global detector instance
_detector = NSFWDetector()

def is_nsfw(image_path: str, threshold: float = 0.6) -> bool:
    """
    Convenience function to detect NSFW content in an image.
    
    Args:
        image_path: Path to the image file
        threshold: Confidence threshold (0.0-1.0) for NSFW detection
        
    Returns:
        bool: True if NSFW content is detected, False otherwise
    """
    return _detector.is_nsfw(image_path, threshold)

def get_detection_details(image_path: str) -> Dict[str, Any]:
    """
    Get detailed NSFW detection results.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dict containing detection results or error information
    """
    return _detector.get_detection_details(image_path)