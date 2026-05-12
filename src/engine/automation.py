import os
import time
import logging
import pyautogui
from pywinauto import Application
from .vision import VisionEngine

logger = logging.getLogger("CapCutAuto")

class CapCutAutomation:
    def __init__(self, config):
        self.config = config
        self.vision = VisionEngine(debug_mode=config['automation']['debug_mode'])
        self.app = None
        self.paused = False
        self.stop_requested = False

    def check_pause(self):
        while self.paused:
            time.sleep(0.5)
        if self.stop_requested:
            raise Exception("Automation stopped by user")

    def start_capcut(self):
        logger.info("Starting CapCut...")
        try:
            self.app = Application(backend="uia").start(self.config['paths']['capcut_path'])
            time.sleep(5) # Wait for splash screen
            return True
        except Exception as e:
            logger.error(f"Failed to start CapCut: {e}")
            return False

    def create_new_project(self):
        logger.info("Creating new project...")
        self.check_pause()
        # Look for "Start creating" button
        if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/start_creating.png")):
            time.sleep(3)
            return True
        return False

    def import_video(self, video_path):
        logger.info(f"Importing video: {video_path}")
        self.check_pause()
        # Click Import button
        if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/import.png")):
            time.sleep(2)
            # Type path into Windows file dialog
            pyautogui.write(video_path)
            pyautogui.press('enter')
            time.sleep(2)
            # Drag to timeline (simplified for now: double click or click '+' if available)
            # Assuming there's a '+' button on the imported media
            if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/add_to_timeline.png")):
                return True
        return False

    def set_aspect_ratio_9_16(self):
        logger.info("Setting aspect ratio to 9:16...")
        self.check_pause()
        # Click Ratio dropdown
        if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/ratio_dropdown.png")):
            time.sleep(1)
            if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/ratio_9_16.png")):
                return True
        return False

    def apply_rectangle_mask(self):
        logger.info("Applying rectangle mask...")
        self.check_pause()
        # Go to Video -> Mask tab
        if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/video_tab.png")):
            time.sleep(0.5)
            if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/mask_tab.png")):
                time.sleep(0.5)
                # Select Rectangle
                if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/rectangle_mask.png")):
                    # Set rounded corners - usually a slider or input
                    # For automation, we might need to click and drag or type value
                    logger.info("Setting rounded corners...")
                    # Placeholder for rounded corner logic
                    return True
        return False

    def scale_to_fit_mask(self):
        logger.info("Scaling video to fit mask...")
        self.check_pause()
        # Go to Video -> Basic tab
        if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/video_tab.png")):
            time.sleep(0.5)
            if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/basic_tab.png")):
                # Find scale input and increase value
                # This often involves double clicking the scale percentage and typing
                scale_pos = self.vision.wait_for_image(os.path.join(self.config['paths']['assets_path'], "buttons/scale_input.png"))
                if scale_pos:
                    pyautogui.click(scale_pos)
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.press('backspace')
                    pyautogui.write("150") # Example scale, might need dynamic adjustment
                    pyautogui.press('enter')
                    return True
        return False

    def apply_filters(self):
        logger.info("Applying filters...")
        self.check_pause()
        # Apply 4K filter
        if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/filters_tab.png")):
            time.sleep(1)
            pyautogui.write(self.config['filters']['enhancement'])
            pyautogui.press('enter')
            time.sleep(1)
            # Click first result and add to timeline
            if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/add_filter.png")):
                logger.info(f"Applied {self.config['filters']['enhancement']} filter")

            # Apply Cinematic filter
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            pyautogui.write(self.config['filters']['cinematic'])
            pyautogui.press('enter')
            time.sleep(1)
            if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/add_filter.png")):
                logger.info(f"Applied {self.config['filters']['cinematic']} filter")
        return True

    def generate_captions(self):
        logger.info("Generating auto captions...")
        self.check_pause()
        if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/text_tab.png")):
            time.sleep(0.5)
            if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/auto_captions.png")):
                time.sleep(0.5)
                if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/create_captions.png")):
                    logger.info("Waiting for captions to generate...")
                    # Wait until "Generating" dialog disappears or success message appears
                    time.sleep(10)

                    # Style captions
                    logger.info("Styling captions...")
                    # Find font dropdown
                    font_pos = self.vision.wait_for_image(os.path.join(self.config['paths']['assets_path'], "buttons/font_dropdown.png"))
                    if font_pos:
                        pyautogui.click(font_pos)
                        pyautogui.write(self.config['captions']['font'])
                        pyautogui.press('enter')

                    # Set size
                    size_pos = self.vision.wait_for_image(os.path.join(self.config['paths']['assets_path'], "buttons/font_size.png"))
                    if size_pos:
                        pyautogui.click(size_pos)
                        pyautogui.hotkey('ctrl', 'a')
                        pyautogui.write(str(self.config['captions']['size']))
                        pyautogui.press('enter')
                    return True
        return False

    def export_video(self, output_filename):
        logger.info(f"Exporting video as {output_filename}...")
        self.check_pause()
        if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/export.png")):
            time.sleep(2)

            # Set Title
            title_pos = self.vision.wait_for_image(os.path.join(self.config['paths']['assets_path'], "buttons/export_title.png"))
            if title_pos:
                pyautogui.click(title_pos)
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.write(output_filename)

            # Set export location
            folder_pos = self.vision.wait_for_image(os.path.join(self.config['paths']['assets_path'], "buttons/export_folder.png"))
            if folder_pos:
                pyautogui.click(folder_pos)
                pyautogui.write(os.path.abspath(self.config['paths']['output_folder']))
                pyautogui.press('enter')

            # Set resolution, quality, etc. (Simplified)
            # This would involve clicking the dropdowns and selecting the config values
            logger.info("Setting export parameters...")

            # Click final Export button
            if self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/final_export.png")):
                logger.info("Export started. Waiting for completion...")
                # Monitor export progress (OCR or image matching for "Open Folder" button)
                if self.vision.wait_for_image(os.path.join(self.config['paths']['assets_path'], "buttons/export_complete.png"), timeout=300):
                    logger.info("Export complete.")
                    self.vision.click_image(os.path.join(self.config['paths']['assets_path'], "buttons/close_export.png"))
                    return True
        return False

    def is_capcut_running(self):
        try:
            # Check if CapCut process exists
            return "CapCut.exe" in os.popen('tasklist').read()
        except:
            return False

    def process_video(self, video_path):
        """Full pipeline for a single video."""
        try:
            if not self.is_capcut_running():
                if not self.start_capcut():
                    return False

            filename = os.path.basename(video_path).split('.')[0]
            if not self.create_new_project(): return False
            if not self.import_video(video_path): return False
            if not self.set_aspect_ratio_9_16(): return False
            if not self.apply_rectangle_mask(): return False
            if not self.scale_to_fit_mask(): return False
            if not self.apply_filters(): return False
            if not self.generate_captions(): return False
            if not self.export_video(filename): return False
            return True
        except Exception as e:
            logger.error(f"Error processing {video_path}: {e}")
            return False
