import pytest
import os
import json
import sys
from unittest.mock import MagicMock

# Mock modules that require GUI/Display
sys.modules['pyautogui'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['pytesseract'] = MagicMock()
sys.modules['pywinauto'] = MagicMock()
sys.modules['customtkinter'] = MagicMock()

from src.engine.vision import VisionEngine
from src.engine.automation import CapCutAutomation

def test_config_load():
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    assert 'paths' in config
    assert 'filters' in config

def test_vision_engine_init():
    ve = VisionEngine(debug_mode=False)
    assert ve.confidence_threshold == 0.8

def test_automation_init():
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    ca = CapCutAutomation(config)
    assert ca.paused == False
    assert ca.stop_requested == False

def test_folder_structure():
    assert os.path.exists('src/engine/automation.py')
    assert os.path.exists('src/gui/app.py')
    assert os.path.exists('config/config.json')
