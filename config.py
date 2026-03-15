import os
import platform
import pathlib
from datetime import datetime

# Output directory (created at runtime)
CAPTURES_DIR = pathlib.Path("captures")

# App config storage
if platform.system() == "Darwin":
    APP_CONFIG_DIR = pathlib.Path.home() / "Library" / "Application Support" / "captureSolvedAC"
else:
    APP_CONFIG_DIR = pathlib.Path(os.environ.get('APPDATA', os.path.expanduser('~'))) / 'captureSolvedAC'
APP_CONFIG_FILE = APP_CONFIG_DIR / 'config.json'

# Browser settings
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 900
PAGE_TIMEOUT = 30000       # ms
HYDRATION_WAIT_MS = 2500   # ms after networkidle (React hydration)
STREAK_RENDER_TIMEOUT_MS = 15000  # ms waiting for heatmap to render

# Image composition
HEADER_HEIGHT = 48
SECTION_GAP = 4
HEADER_BG_COLOR = (15, 16, 22)        # dark bar above sections
HEADER_TEXT_COLOR = (224, 224, 224)
HEADER_DATE_COLOR = (120, 120, 140)


def get_output_path() -> str:
    """Returns output path for today's capture: captures/YYYY-MM-DD.png"""
    CAPTURES_DIR.mkdir(exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    return str(CAPTURES_DIR / f"{date_str}.png")
