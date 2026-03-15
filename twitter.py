import os
import platform
import subprocess
import webbrowser
import urllib.parse
from datetime import datetime


def copy_image_to_clipboard(image_path: str) -> bool:
    """Copy image file to clipboard. Returns True on success."""
    try:
        abs_path = os.path.abspath(image_path)
        if platform.system() == "Darwin":
            script = f'set the clipboard to (read (POSIX file "{abs_path}") as «class PNGf»)'
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                timeout=15
            )
            return result.returncode == 0
        else:
            abs_path_ps = abs_path.replace("'", "''")
            ps_script = (
                "Add-Type -AssemblyName System.Windows.Forms; "
                "Add-Type -AssemblyName System.Drawing; "
                f"$img = [System.Drawing.Image]::FromFile('{abs_path_ps}'); "
                "[System.Windows.Forms.Clipboard]::SetImage($img); "
                "$img.Dispose()"
            )
            result = subprocess.run(
                ['powershell', '-NoProfile', '-NonInteractive', '-Command', ps_script],
                capture_output=True,
                timeout=15
            )
            return result.returncode == 0
    except Exception:
        return False


def open_twitter_compose(handle: str) -> None:
    """Open Twitter web compose window with pre-filled text."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    tweet_text = f"solved.ac {date_str}\n@{handle}\n#solvedac #BOJ"
    url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(tweet_text)}"
    webbrowser.open(url)


def open_captures_folder(folder_path: str) -> None:
    """Open the captures folder in Finder (macOS) or Explorer (Windows)."""
    os.makedirs(folder_path, exist_ok=True)
    if platform.system() == "Darwin":
        subprocess.run(['open', folder_path])
    else:
        os.startfile(folder_path)
