import os
import subprocess
import webbrowser
import urllib.parse
from datetime import datetime


def copy_image_to_clipboard(image_path: str) -> bool:
    """Copy image file to Windows clipboard using PowerShell.
    Returns True on success. User can then Ctrl+V in Twitter."""
    try:
        abs_path = os.path.abspath(image_path).replace("'", "''")
        ps_script = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "Add-Type -AssemblyName System.Drawing; "
            f"$img = [System.Drawing.Image]::FromFile('{abs_path}'); "
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
    """Open the captures folder in Windows Explorer."""
    os.makedirs(folder_path, exist_ok=True)
    os.startfile(folder_path)
