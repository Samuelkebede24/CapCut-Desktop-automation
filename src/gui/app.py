import customtkinter as ctk
import threading
import queue
import time
import os
import json
try:
    import pyautogui
except ImportError:
    pyautogui = None
from PIL import Image, ImageTk
from src.utils.logger import setup_logger
from src.engine.automation import CapCutAutomation

class CapCutGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CapCut Desktop Automation")
        self.attributes("-topmost", True)
        self.geometry("1000x800")

        # Load Config
        with open('config/config.json', 'r') as f:
            self.config = json.load(f)

        self.log_queue = queue.Queue()
        self.logger = setup_logger(self.log_queue)
        self.automation = CapCutAutomation(self.config)

        self.setup_ui()
        self.update_logs()

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.start_btn = ctk.CTkButton(self.sidebar, text="Start", command=self.start_automation)
        self.start_btn.pack(pady=10, padx=20)

        self.pause_btn = ctk.CTkButton(self.sidebar, text="Pause", command=self.toggle_pause)
        self.pause_btn.pack(pady=10, padx=20)

        self.stop_btn = ctk.CTkButton(self.sidebar, text="Stop", command=self.stop_automation, fg_color="red")
        self.stop_btn.pack(pady=10, padx=20)

        # Main Content
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Progress
        self.progress_label = ctk.CTkLabel(self.main_frame, text="Status: Idle", font=("Arial", 16))
        self.progress_label.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=10)
        self.progress_bar.set(0)

        # Live Preview
        self.preview_label = ctk.CTkLabel(self.main_frame, text="Live Preview", font=("Arial", 14))
        self.preview_label.pack(pady=5)
        self.preview_canvas = ctk.CTkLabel(self.main_frame, text="", height=200, fg_color="black")
        self.preview_canvas.pack(fill="x", padx=20, pady=5)

        # Logs
        self.log_text = ctk.CTkTextbox(self.main_frame, height=200)
        self.log_text.pack(fill="both", padx=20, pady=20, expand=True)

    def update_logs(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_text.insert("end", msg + "\n")
                self.log_text.see("end")
        except queue.Empty:
            pass

        # Update Preview
        try:
            screenshot = pyautogui.screenshot()
            screenshot.thumbnail((400, 225))
            self.preview_img = ImageTk.PhotoImage(screenshot)
            self.preview_canvas.configure(image=self.preview_img)
        except:
            pass

        self.after(200, self.update_logs)

    def start_automation(self):
        self.automation.stop_requested = False
        threading.Thread(target=self.run_automation_loop, daemon=True).start()

    def toggle_pause(self):
        self.automation.paused = not self.automation.paused
        self.pause_btn.configure(text="Resume" if self.automation.paused else "Pause")

    def stop_automation(self):
        self.automation.stop_requested = True
        self.logger.info("Stop requested...")

    def run_automation_loop(self):
        self.logger.info("Automation started.")
        watch_folder = self.config['paths']['watch_folder']

        if not os.path.exists(watch_folder):
            os.makedirs(watch_folder)

        while not self.automation.stop_requested:
            videos = [f for f in os.listdir(watch_folder) if f.endswith(('.mp4', '.mov', '.avi'))]
            if videos:
                self.progress_label.configure(text=f"Processing {len(videos)} videos...")
                for i, video in enumerate(videos):
                    if self.automation.stop_requested: break

                    video_path = os.path.join(watch_folder, video)
                    self.logger.info(f"Processing {video} ({i+1}/{len(videos)})")

                    if self.automation.process_video(video_path):
                        self.logger.info(f"Successfully processed {video}")
                        # Move to processed/completed if needed
                    else:
                        self.logger.error(f"Failed to process {video}")

                    self.progress_bar.set((i + 1) / len(videos))
            else:
                self.progress_label.configure(text="Status: Waiting for videos...")
                self.logger.debug(f"Watching for videos in {watch_folder}...")

            time.sleep(5)

if __name__ == "__main__":
    app = CapCutGUI()
    app.mainloop()
