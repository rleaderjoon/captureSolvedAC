"""
Entry point for captureSolvedAC.

On first launch, checks whether Chrome or Playwright Chromium is installed.
If Chrome is found, uses it directly (no download needed).
If not, shows an install dialog then downloads Chromium (~100MB, one-time).
Then launches the main GUI.
"""
import os
import pathlib
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox


def _find_chrome() -> bool:
    """Check if Google Chrome is installed on this system."""
    candidates = [
        pathlib.Path(os.environ.get("PROGRAMFILES", "")) / "Google" / "Chrome" / "Application" / "chrome.exe",
        pathlib.Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Google" / "Chrome" / "Application" / "chrome.exe",
        pathlib.Path(os.environ.get("LOCALAPPDATA", "")) / "Google" / "Chrome" / "Application" / "chrome.exe",
    ]
    return any(p.exists() for p in candidates)


def _find_chromium() -> bool:
    """Check if Playwright's Chromium executable is installed and accessible."""
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if not local_app_data:
        return False
    ms_playwright = pathlib.Path(local_app_data) / "ms-playwright"
    if not ms_playwright.exists():
        return False
    for chromium_dir in ms_playwright.glob("chromium-*"):
        chrome_exe = chromium_dir / "chrome-win" / "chrome.exe"
        if chrome_exe.exists():
            return True
    return False


def _install_chromium():
    """Run 'playwright install chromium'. Works in both frozen and script mode."""
    if getattr(sys, "frozen", False):
        # Running as PyInstaller .exe — try bundled playwright driver
        driver = pathlib.Path(sys._MEIPASS) / "playwright" / "driver" / "playwright.exe"
        if driver.exists():
            subprocess.run([str(driver), "install", "chromium"], check=True)
            return
        # Fallback: try system playwright
        subprocess.run(["playwright", "install", "chromium"], check=True)
    else:
        # Running as Python script
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True
        )


def _show_install_ui() -> bool:
    """
    Show a Tkinter window for first-time Chromium installation.
    Returns True if installation succeeded, False if cancelled or failed.
    """
    result = {"ok": False, "error": ""}

    root = tk.Tk()
    root.title("captureSolvedAC - 초기 설정")
    root.resizable(False, False)

    # Center window
    root.update_idletasks()
    w, h = 380, 180
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    lbl_title = tk.Label(root, text="Chromium 브라우저 설치 필요", font=("", 12, "bold"), pady=12)
    lbl_title.pack()

    lbl_info = tk.Label(
        root,
        text="solved.ac 페이지 캡처를 위해 브라우저를 설치합니다.\n"
             "약 100~150MB이며, 처음 한 번만 필요합니다.",
        pady=4,
    )
    lbl_info.pack()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=16)

    def on_install():
        for w in root.winfo_children():
            w.destroy()
        tk.Label(root, text="설치 중입니다... 잠시 기다려주세요.", pady=60).pack()
        root.update()

        def do_install():
            try:
                _install_chromium()
                result["ok"] = True
            except Exception as e:
                result["error"] = str(e)
            finally:
                root.after(0, root.destroy)

        threading.Thread(target=do_install, daemon=True).start()

    def on_cancel():
        root.destroy()

    tk.Button(btn_frame, text="설치", width=12, command=on_install).pack(side="left", padx=10)
    tk.Button(btn_frame, text="취소", width=12, command=on_cancel).pack(side="left", padx=10)

    root.mainloop()

    if result["error"]:
        r = tk.Tk()
        r.withdraw()
        messagebox.showerror(
            "설치 실패",
            f"Chromium 설치에 실패했습니다:\n{result['error']}\n\n"
            "수동으로 설치하려면 setup.bat을 실행하세요."
        )
        r.destroy()
        return False

    return result["ok"]


def main():
    # 1. Ensure a browser is available (Chrome preferred, else Playwright Chromium)
    if not _find_chrome() and not _find_chromium():
        installed = _show_install_ui()
        if not installed:
            sys.exit(0)

    # 2. Launch main GUI
    from gui import App
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
