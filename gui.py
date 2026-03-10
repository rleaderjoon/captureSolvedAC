"""
CustomTkinter GUI for captureSolvedAC.

Layout:
  - Username input
  - Capture button
  - Progress bar + status label
  - Image preview (thumbnail)
  - Action buttons: 폴더 열기 / 이미지 복사 / 트위터에 올리기
"""
import asyncio
import json
import threading
from pathlib import Path
from typing import Optional

import customtkinter as ctk
from PIL import Image

import capture as cap
import compose as comp
import twitter as twit
from config import CAPTURES_DIR, APP_CONFIG_DIR, APP_CONFIG_FILE, get_output_path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("captureSolvedAC")
        self.geometry("520x680")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)

        self._last_output_path: Optional[str] = None
        self._current_handle: str = ""

        self._build_ui()
        self._load_config()

    # ------------------------------------------------------------------ UI

    def _build_ui(self):
        # --- Username input ---
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.grid(row=0, column=0, padx=20, pady=(20, 8), sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            input_frame, text="solved.ac 핸들 (username)", anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.entry_handle = ctk.CTkEntry(
            input_frame,
            placeholder_text="예: intars",
            height=40,
            font=ctk.CTkFont(size=15),
        )
        self.entry_handle.grid(row=1, column=0, sticky="ew")
        self.entry_handle.bind("<Return>", lambda _: self._on_capture())

        # --- Capture button ---
        self.btn_capture = ctk.CTkButton(
            self,
            text="📸  캡처하기",
            height=44,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self._on_capture,
        )
        self.btn_capture.grid(row=1, column=0, padx=20, pady=(8, 8), sticky="ew")

        # --- Progress ---
        progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        progress_frame.grid(row=2, column=0, padx=20, pady=(0, 8), sticky="ew")
        progress_frame.grid_columnconfigure(0, weight=1)

        self.progress_bar = ctk.CTkProgressBar(progress_frame, mode="indeterminate")
        self.progress_bar.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        self.progress_bar.set(0)

        self.lbl_status = ctk.CTkLabel(
            progress_frame, text="준비됨", anchor="w", text_color="gray"
        )
        self.lbl_status.grid(row=1, column=0, sticky="w")

        # --- Preview area ---
        self.preview_frame = ctk.CTkFrame(self, height=320)
        self.preview_frame.grid(row=3, column=0, padx=20, pady=(0, 12), sticky="nsew")
        self.grid_rowconfigure(3, weight=1)

        self.lbl_preview = ctk.CTkLabel(
            self.preview_frame,
            text="캡처 결과가 여기에 표시됩니다.",
            text_color="gray",
        )
        self.lbl_preview.place(relx=0.5, rely=0.5, anchor="center")

        # --- Action buttons ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.btn_folder = ctk.CTkButton(
            btn_frame, text="폴더 열기", state="disabled",
            command=self._on_open_folder,
        )
        self.btn_folder.grid(row=0, column=0, padx=(0, 4), sticky="ew")

        self.btn_copy = ctk.CTkButton(
            btn_frame, text="이미지 복사", state="disabled",
            command=self._on_copy_image,
        )
        self.btn_copy.grid(row=0, column=1, padx=4, sticky="ew")

        self.btn_tweet = ctk.CTkButton(
            btn_frame,
            text="트위터 올리기",
            state="disabled",
            fg_color="#1d9bf0",
            hover_color="#1a8cd8",
            command=self._on_tweet,
        )
        self.btn_tweet.grid(row=0, column=2, padx=(4, 0), sticky="ew")

    # ------------------------------------------------------------------ Config

    def _load_config(self):
        try:
            if APP_CONFIG_FILE.exists():
                with open(APP_CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                handle = cfg.get("handle", "")
                if handle:
                    self.entry_handle.insert(0, handle)
        except Exception:
            pass

    def _save_config(self, handle: str):
        try:
            APP_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(APP_CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump({"handle": handle}, f)
        except Exception:
            pass

    # ------------------------------------------------------------------ Helpers

    def _set_status(self, msg: str, color: str = "gray"):
        self.after(0, lambda: self.lbl_status.configure(text=msg, text_color=color))

    def _set_buttons_active(self, active: bool):
        state = "normal" if active else "disabled"
        self.btn_folder.configure(state=state)
        self.btn_copy.configure(state=state)
        self.btn_tweet.configure(state=state)

    # ------------------------------------------------------------------ Actions

    def _on_capture(self):
        handle = self.entry_handle.get().strip()
        if not handle:
            self._set_status("핸들을 입력해주세요.", "#ff6b6b")
            return

        self._current_handle = handle
        self.btn_capture.configure(state="disabled")
        self._set_buttons_active(False)
        self.progress_bar.start()
        self._set_status("시작 중...")

        def run():
            try:
                rating_png, streak_png = asyncio.run(
                    cap.capture_sections(handle, on_status=self._set_status)
                )
                self._set_status("이미지 합성 중...")
                output_path = get_output_path()
                comp.compose_image(rating_png, streak_png, handle, output_path)
                self._last_output_path = output_path
                self._save_config(handle)
                self.after(0, lambda: self._on_success(output_path))
            except Exception as e:
                self.after(0, lambda err=str(e): self._on_error(err))

        threading.Thread(target=run, daemon=True).start()

    def _on_success(self, output_path: str):
        self.progress_bar.stop()
        self.progress_bar.set(1)
        short_path = str(Path(output_path))
        self._set_status(f"저장됨: {short_path}", "#51cf66")
        self.btn_capture.configure(state="normal")
        self._set_buttons_active(True)
        self._show_thumbnail(output_path)

    def _on_error(self, error_msg: str):
        self.progress_bar.stop()
        self.progress_bar.set(0)
        self._set_status(f"오류: {error_msg}", "#ff6b6b")
        self.btn_capture.configure(state="normal")

    def _show_thumbnail(self, image_path: str):
        try:
            img = Image.open(image_path)
            # Scale to fit preview area (max 460x300)
            max_w, max_h = 460, 300
            ratio = min(max_w / img.width, max_h / img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)

            photo = ctk.CTkImage(light_image=img, dark_image=img, size=new_size)
            self.lbl_preview.configure(image=photo, text="")
            self.lbl_preview._ctk_image = photo  # prevent garbage collection
        except Exception as e:
            self.lbl_preview.configure(text=f"미리보기 오류: {e}", image=None)

    def _on_open_folder(self):
        twit.open_captures_folder(str(CAPTURES_DIR))

    def _on_copy_image(self):
        if not self._last_output_path:
            return
        ok = twit.copy_image_to_clipboard(self._last_output_path)
        if ok:
            self._set_status("클립보드에 복사됨! 트위터에서 Ctrl+V로 이미지 붙여넣기", "#51cf66")
        else:
            self._set_status("클립보드 복사 실패. 폴더 열기로 직접 파일을 첨부하세요.", "#ff6b6b")

    def _on_tweet(self):
        if not self._last_output_path:
            return
        twit.copy_image_to_clipboard(self._last_output_path)
        twit.open_twitter_compose(self._current_handle)
        self._set_status(
            "트위터 창 열림! 이미지가 클립보드에 복사됨 → Ctrl+V로 붙여넣기",
            "#1d9bf0",
        )
