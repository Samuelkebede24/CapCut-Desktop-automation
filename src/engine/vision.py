import cv2
import numpy as np
import pyautogui
import os
import pytesseract
from PIL import Image
import time
import logging

logger = logging.getLogger("CapCutAuto")

class VisionEngine:
    def __init__(self, debug_mode=True):
        self.debug_mode = debug_mode
        self.confidence_threshold = 0.8

    def capture_screen(self):
        screenshot = pyautogui.screenshot()
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    def find_image(self, template_path, region=None):
        """Finds an image on screen and returns its center coordinates."""
        if not os.path.exists(template_path):
            logger.error(f"Asset file MISSING from disk: {template_path}")
            return None

        screen = self.capture_screen()
        template = cv2.imread(template_path)
        if template is None:
            logger.error(f"Failed to load image (corrupt?): {template_path}")
            return None

        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val >= self.confidence_threshold:
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2

            if self.debug_mode:
                logger.debug(f"Found {template_path} at {max_loc} with confidence {max_val:.2f}")
                # In a real scenario, we'd draw on a debug window here

            return (center_x, center_y)
        return None

    def click_image(self, template_path, clicks=1, interval=0.1, retries=3):
        for i in range(retries):
            pos = self.find_image(template_path)
            if pos:
                pyautogui.click(pos[0], pos[1], clicks=clicks, interval=interval)
                return True
            logger.warning(f"Retry {i+1}/{retries} for {template_path}")
            time.sleep(1)
        return False

    def wait_for_image(self, template_path, timeout=10):
        start_time = time.time()
        while time.time() - start_time < timeout:
            pos = self.find_image(template_path)
            if pos:
                return pos
            time.sleep(0.5)
        return None

    def read_text(self, region=None):
        """Uses OCR to read text from a specific screen region."""
        screenshot = pyautogui.screenshot(region=region) if region else pyautogui.screenshot()
        text = pytesseract.image_to_string(screenshot)
        return text.strip()

    def find_text_and_click(self, target_text, region=None):
        """Finds text on screen and clicks it."""
        screenshot = pyautogui.screenshot(region=region) if region else pyautogui.screenshot()
        data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

        offset_x = region[0] if region else 0
        offset_y = region[1] if region else 0

        for i, text in enumerate(data['text']):
            if target_text.lower() in text.lower():
                x = data['left'][i] + data['width'][i] // 2 + offset_x
                y = data['top'][i] + data['height'][i] // 2 + offset_y
                pyautogui.click(x, y)
                logger.info(f"Clicked text '{target_text}' at ({x}, {y})")
                return True
        return False
