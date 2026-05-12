import pyautogui
import os
import time
import json
import keyboard
from PIL import Image

REQUIRED_BUTTONS = [
    "start_creating.png",
    "import.png",
    "add_to_timeline.png",
    "ratio_dropdown.png",
    "ratio_9_16.png",
    "video_tab.png",
    "mask_tab.png",
    "rectangle_mask.png",
    "basic_tab.png",
    "scale_input.png",
    "filters_tab.png",
    "add_filter.png",
    "text_tab.png",
    "auto_captions.png",
    "create_captions.png",
    "font_dropdown.png",
    "font_size.png",
    "export.png",
    "export_title.png",
    "export_folder.png",
    "final_export.png",
    "export_complete.png",
    "close_export.png"
]

def capture_button(button_name, save_dir):
    print(f"\n--- Capturing: {button_name} ---")
    print(f"1. Open CapCut and navigate so the button is visible.")
    print(f"2. Hover your mouse over the CENTER of the '{button_name}' button.")
    print(f"3. Press 'S' to capture a 50x50 area around your mouse, or 'F' for 100x100.")
    print(f"4. Press 'Q' to skip this button.")

    while True:
        if keyboard.is_pressed('s'):
            size = 50
            break
        if keyboard.is_pressed('f'):
            size = 100
            break
        if keyboard.is_pressed('q'):
            print(f"Skipped {button_name}")
            return

    x, y = pyautogui.position()
    left = x - size // 2
    top = y - size // 2

    screenshot = pyautogui.screenshot(region=(left, top, size, size))
    save_path = os.path.join(save_dir, button_name)
    screenshot.save(save_path)
    print(f"Saved to {save_path}")
    time.sleep(0.5) # Debounce

def main():
    with open('config/config.json', 'r') as f:
        config = json.load(f)

    save_dir = os.path.join(config['paths']['assets_path'], "buttons")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    print("CapCut Asset Capture Tool")
    print("=========================")

    for btn in REQUIRED_BUTTONS:
        capture_button(btn, save_dir)

    print("\nAll done! You can now run the automation.")

if __name__ == "__main__":
    main()
