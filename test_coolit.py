#!/usr/bin/env python3
"""
Basic test script for Cool It application
Tests core functionality without hardware access
"""

import sys
import os
import unittest
from unittest.mock import patch, mock_open

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestCoolItCore(unittest.TestCase):
    """Test core Cool It functionality"""
    
    def test_imports(self):
        """Test that all required modules can be imported"""
        try:
            import coolit
            self.assertTrue(hasattr(coolit, 'MODES'))
            self.assertTrue(hasattr(coolit, 'THEMES'))
            self.assertTrue(hasattr(coolit, 'CPU_CURVES'))
        except ImportError as e:
            self.fail(f"Failed to import coolit module: {e}")
    
    def test_modes_validation(self):
        """Test that all modes have valid configurations"""
        import coolit
        
        for mode, config in coolit.MODES.items():
            self.assertIsInstance(mode, str)
            self.assertIn('gpu', config)
            self.assertIsInstance(config['gpu'], int)
            self.assertTrue(0 <= config['gpu'] <= 100)
    
    def test_cpu_curves_validation(self):
        """Test that CPU curves have valid PWM values"""
        import coolit
        
        for mode, config in coolit.CPU_CURVES.items():
            self.assertIsInstance(mode, str)
            self.assertIn('pwms', config)
            
            if config['pwms'] is not None:
                self.assertIsInstance(config['pwms'], list)
                for pwm in config['pwms']:
                    self.assertIsInstance(pwm, int)
                    self.assertTrue(0 <= pwm <= 255)
    
    def test_themes_validation(self):
        """Test that all themes have required color keys"""
        import coolit
        
        required_keys = {
            'bg', 'title_bg', 'title_text', 'status_bg', 'status_text',
            'monitor_bg', 'monitor_border', 'monitor_text', 'btn_bg',
            'btn_text', 'btn_border', 'btn_hover', 'btn_active', 'label_text'
        }
        
        for theme_name, theme_config in coolit.THEMES.items():
            self.assertIsInstance(theme_name, str)
            self.assertIsInstance(theme_config, dict)
            
            for key in required_keys:
                self.assertIn(key, theme_config, f"Missing key '{key}' in theme '{theme_name}'")
                self.assertTrue(theme_config[key].startswith('#'), f"Invalid color format in theme '{theme_name}' key '{key}'")

if __name__ == '__main__':
    print("🧪 Running Cool It Core Tests")
    print("=============================")
    
    # Check PyQt5 availability
    try:
        from PyQt5.QtWidgets import QApplication
        print("✅ PyQt5 is available")
    except ImportError:
        print("❌ PyQt5 not available - some tests may fail")
    
    # Run the tests
    unittest.main(verbosity=2)