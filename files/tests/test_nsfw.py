"""
Test suite for the NSFW detection plugin.
"""

import os
import tempfile
import pytest
from unittest.mock import Mock, patch
from plugins.nsfw import is_nsfw, get_detection_details, NSFWDetector


class TestNSFWDetector:
    """Test the NSFWDetector class."""
    
    def test_initialization_without_nudenet(self):
        """Test that detector handles missing NudeNet gracefully."""
        with patch('plugins.nsfw.NUDENET_AVAILABLE', False):
            detector = NSFWDetector()
            assert not detector.initialized
            assert detector.detector is None
    
    def test_is_nsfw_uninitialized_detector(self):
        """Test is_nsfw returns False when detector is not initialized."""
        detector = NSFWDetector()
        detector.initialized = False
        
        result = detector.is_nsfw("dummy_path.jpg")
        assert result is False
    
    def test_is_nsfw_nonexistent_file(self):
        """Test is_nsfw returns False for non-existent files."""
        detector = NSFWDetector()
        detector.initialized = True
        
        result = detector.is_nsfw("/nonexistent/file.jpg")
        assert result is False
    
    @patch('plugins.nsfw.NUDENET_AVAILABLE', True)
    def test_is_nsfw_with_mock_detector(self):
        """Test is_nsfw with mocked NudeNet detector."""
        # Create a temporary image file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(b'fake image data')
            temp_path = temp_file.name
        
        try:
            # Mock the detector
            mock_detector = Mock()
            mock_detector.detect.return_value = [
                {'class': 'exposed_breast_f', 'score': 0.8}
            ]
            
            detector = NSFWDetector()
            detector.detector = mock_detector
            detector.initialized = True
            
            result = detector.is_nsfw(temp_path)
            assert result is True
            
            # Test with low score
            mock_detector.detect.return_value = [
                {'class': 'exposed_breast_f', 'score': 0.3}
            ]
            result = detector.is_nsfw(temp_path, threshold=0.6)
            assert result is False
            
        finally:
            os.unlink(temp_path)
    
    @patch('plugins.nsfw.NUDENET_AVAILABLE', True)
    def test_is_nsfw_safe_content(self):
        """Test is_nsfw with safe content."""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(b'fake image data')
            temp_path = temp_file.name
        
        try:
            # Mock the detector to return safe content
            mock_detector = Mock()
            mock_detector.detect.return_value = [
                {'class': 'covered_belly', 'score': 0.9}
            ]
            
            detector = NSFWDetector()
            detector.detector = mock_detector
            detector.initialized = True
            
            result = detector.is_nsfw(temp_path)
            assert result is False
            
        finally:
            os.unlink(temp_path)
    
    @patch('plugins.nsfw.NUDENET_AVAILABLE', True)
    def test_get_detection_details(self):
        """Test get_detection_details function."""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(b'fake image data')
            temp_path = temp_file.name
        
        try:
            # Mock the detector
            mock_detector = Mock()
            mock_detector.detect.return_value = [
                {'class': 'exposed_breast_f', 'score': 0.8}
            ]
            
            detector = NSFWDetector()
            detector.detector = mock_detector
            detector.initialized = True
            
            details = detector.get_detection_details(temp_path)
            assert details['image_path'] == temp_path
            assert 'detections' in details
            assert 'is_nsfw' in details
            assert details['is_nsfw'] is True
            
        finally:
            os.unlink(temp_path)


class TestNSFWModule:
    """Test the module-level functions."""
    
    @patch('plugins.nsfw._detector')
    def test_is_nsfw_function(self, mock_detector):
        """Test the module-level is_nsfw function."""
        mock_detector.is_nsfw.return_value = True
        
        result = is_nsfw("test_image.jpg")
        assert result is True
        mock_detector.is_nsfw.assert_called_once_with("test_image.jpg", 0.6)
    
    @patch('plugins.nsfw._detector')
    def test_get_detection_details_function(self, mock_detector):
        """Test the module-level get_detection_details function."""
        expected_details = {
            'image_path': 'test_image.jpg',
            'detections': [],
            'is_nsfw': False
        }
        mock_detector.get_detection_details.return_value = expected_details
        
        result = get_detection_details("test_image.jpg")
        assert result == expected_details
        mock_detector.get_detection_details.assert_called_once_with("test_image.jpg")


def test_nsfw_classes_detection():
    """Test that the correct NSFW classes are detected."""
    nsfw_classes = [
        'exposed_anus', 'exposed_armpits', 'exposed_belly', 
        'exposed_breast_f', 'exposed_breast_m', 'exposed_buttocks',
        'exposed_genitalia_f', 'exposed_genitalia_m', 'exposed_thighs_f',
        'exposed_thighs_m'
    ]
    
    detector = NSFWDetector()
    detector.initialized = True
    
    # Mock detector for each NSFW class
    for nsfw_class in nsfw_classes:
        mock_detector = Mock()
        mock_detector.detect.return_value = [
            {'class': nsfw_class, 'score': 0.8}
        ]
        detector.detector = mock_detector
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(b'fake image data')
            temp_path = temp_file.name
        
        try:
            result = detector.is_nsfw(temp_path)
            assert result is True, f"Class {nsfw_class} should be detected as NSFW"
        finally:
            os.unlink(temp_path)