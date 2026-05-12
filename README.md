# CapCut Desktop Automation System

## Setup Instructions

1.  **Install Python**: Ensure Python 3.10+ is installed.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Paths**: Open `config/config.json` and update `capcut_path` to your CapCut installation path.
4.  **Assets**: Place screenshots of CapCut buttons into `src/assets/buttons/`.
5.  **Tesseract OCR**: Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) and ensure it's in your system PATH.

## Folder Structure

- `src/engine/`: Automation and Vision logic.
- `src/gui/`: Dashboard and user controls.
- `config/`: Configuration files.
- `input_videos/`: Drop videos here to process.
- `output_videos/`: Processed videos will appear here.

## Build Instructions (Windows Executable)

To create a standalone `.exe`:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed src/gui/app.py
```

## Workflow details
- **Masking**: Applies a rectangle mask with rounded corners.
- **Scaling**: Dynamically adjusts to fill the frame.
- **Filters**: Applies 4K and Cinematic filters.
- **Captions**: Auto-generates and styles captions (ZY Brief, Size 8).
