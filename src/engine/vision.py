import cv2
import numpy as np
import pyautogui
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
        screen = self.capture_screen()
        template = cv2.imread(template_path)
        if template is None:
            logger.error(f"Template image not found: {template_path}")
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

    def find_text_and_click(self, text, region=None):
        """Very basic OCR-based clicking (complex to implement perfectly without specific regions)"""
        # This is a placeholder for more advanced OCR logic if needed
        full_text = self.read_text(region)
        if text.lower() in full_text.lower():
            logger.info(f"Detected text '{text}' on screen.")
            # Finding exact coordinates from OCR requires image_to_data
            return True
        return False
