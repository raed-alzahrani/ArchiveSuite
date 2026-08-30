import os
import sys
import json
import shutil
import threading
import zipfile
import subprocess
import queue
import time
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import filedialog, messagebox

# Auto-check dependencies
REQUIRED_LIBS = {
    "customtkinter": "customtkinter",
    "PIL": "pillow",
    "py7zr": "py7zr"
}

missing = []
for mod, pkg in REQUIRED_LIBS.items():
    try:
        __import__(mod)
    except ImportError:
        missing.append(pkg)

if missing:
    root = tk.Tk()
    root.title("Missing Requirements")
    root.geometry("450x260")
    root.resizable(False, False)
    root.configure(bg="#0b0f17")

    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    root.geometry(f"450x260+{int((ws-450)/2)}+{int((hs-260)/2)}")

    tk.Label(root, text="Missing Python Packages", font=("Segoe UI", 12, "bold"), fg="#f87171", bg="#0b0f17").pack(pady=(20, 5))
    tk.Label(root, text="The following dependencies need to be installed:", font=("Segoe UI", 9), fg="#94a3b8", bg="#0b0f17").pack()

    box = tk.Frame(root, bg="#121926", bd=1, relief="solid")
    box.pack(fill="x", padx=30, pady=10)
    for pkg in missing:
        tk.Label(box, text=f"• {pkg}", font=("Consolas", 10, "bold"), fg="#10b981", bg="#121926").pack(anchor="w", padx=12, pady=2)

    def install_pkgs():
        root.destroy()
        py_exe = sys.executable
        if py_exe.lower().endswith("pythonw.exe"):
            py_exe = py_exe[:-10] + "python.exe"

        script_path = os.path.abspath(__file__)
        bat_cmd = f"""@echo off
title Installing ArchiveSuite Dependencies...
echo [*] Installing: {" ".join(missing)}
"{py_exe}" -m pip install --upgrade pip {" ".join(missing)}
echo.
echo [*] Launching application...
start "" "{sys.executable}" "{script_path}"
exit
"""
        bat_file = os.path.join(os.environ.get("TEMP", "."), "_install_arch_deps.bat")
        with open(bat_file, "w", encoding="utf-8") as f:
            f.write(bat_cmd)
        
        subprocess.Popen(f'start "" "{bat_file}"', shell=True)
        sys.exit()

    btns = tk.Frame(root, bg="#0b0f17")
    btns.pack(fill="x", padx=30, pady=(10, 15))
    tk.Button(btns, text="Cancel", font=("Segoe UI", 9), bg="#1e293b", fg="#fff", bd=0, padx=14, pady=5, command=sys.exit).pack(side="left")
    tk.Button(btns, text="Install Packages", font=("Segoe UI", 9, "bold"), bg="#10b981", fg="#042f2e", bd=0, padx=14, pady=5, command=install_pkgs).pack(side="right")
    
    root.mainloop()
    sys.exit()

from PIL import Image
import customtkinter as ctk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
ICON_PATH = os.path.join(BASE_DIR, "app_icon.ico")
CACHE_FILE = os.path.join(BASE_DIR, "scan_cache.txt")

ARCHIVE_FORMATS = ('.zip', '.7z', '.rar')
IMAGE_FORMATS = (('Images', '*.png;*.jpg;*.jpeg;*.webp;*.bmp;*.ico'), ('All Files', '*.*'))

FONT_PROFILES = {
    "Futuristic (Bahnschrift)": {
        "title": ("Bahnschrift", 16, "bold"),
        "ui_bold": ("Bahnschrift", 12, "bold"),
        "ui_sm": ("Bahnschrift", 11, "bold"),
        "row_main": ("Bahnschrift", 12, "bold"),
        "badge": ("Consolas", 10, "bold"),
        "mono": ("Consolas", 11, "bold")
    },
    "Modern Heavy (Segoe UI)": {
        "title": ("Segoe UI", 16, "bold"),
        "ui_bold": ("Segoe UI", 12, "bold"),
        "ui_sm": ("Segoe UI", 11, "bold"),
        "row_main": ("Segoe UI", 12, "bold"),
        "badge": ("Consolas", 10, "bold"),
        "mono": ("Consolas", 11, "bold")
    },
    "Cyber Terminal (Cascadia Mono)": {
        "title": ("Cascadia Mono", 15, "bold"),
        "ui_bold": ("Cascadia Mono", 11, "bold"),
        "ui_sm": ("Cascadia Mono", 10, "bold"),
        "row_main": ("Cascadia Mono", 11, "bold"),
        "badge": ("Cascadia Mono", 10, "bold"),
        "mono": ("Cascadia Mono", 10, "bold")
    },
    "Arcade Punch (Trebuchet MS)": {
        "title": ("Trebuchet MS", 16, "bold"),
        "ui_bold": ("Trebuchet MS", 12, "bold"),
        "ui_sm": ("Trebuchet MS", 11, "bold"),
        "row_main": ("Trebuchet MS", 12, "bold"),
        "badge": ("Consolas", 10, "bold"),
        "mono": ("Consolas", 11, "bold")
    },
    "Clean Solid (Arial)": {
        "title": ("Arial", 16, "bold"),
        "ui_bold": ("Arial", 12, "bold"),
        "ui_sm": ("Arial", 11, "bold"),
        "row_main": ("Arial", 12, "bold"),
        "badge": ("Consolas", 10, "bold"),
        "mono": ("Consolas", 11, "bold")
    }
}

THEMES = {
    "Emerald": {
        "primary": "#10b981", "hover": "#059669", "btn_bg": "#064e3b", "btn_hover": "#047857",
        "menu_bg": "#064e3b", "menu_btn": "#10b981", "menu_hover": "#059669",
        "badge_dark": "#0c2822", "badge_text_dark": "#34d399", "badge_light": "#d1fae5", "badge_text_light": "#065f46"
    },
    "Nordic Blue": {
        "primary": "#38bdf8", "hover": "#0ea5e9", "btn_bg": "#0c4a6e", "btn_hover": "#0369a1",
        "menu_bg": "#0c4a6e", "menu_btn": "#38bdf8", "menu_hover": "#0284c7",
        "badge_dark": "#0e2c45", "badge_text_dark": "#7dd3fc", "badge_light": "#e0f2fe", "badge_text_light": "#0369a1"
    },
    "Amethyst": {
        "primary": "#c084fc", "hover": "#9333ea", "btn_bg": "#581c87", "btn_hover": "#6b21a8",
        "menu_bg": "#581c87", "menu_btn": "#c084fc", "menu_hover": "#9333ea",
        "badge_dark": "#2e1845", "badge_text_dark": "#d8b4fe", "badge_light": "#f3e8ff", "badge_text_light": "#6b21a8"
    }
}

THEME_MIGRATION = {
    "Green": "Emerald",
    "Blue": "Nordic Blue",
    "Purple": "Amethyst",
    "Red": "Emerald",
    "Yellow": "Emerald",
    "Teal": "Emerald"
}

def format_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:3.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"

def load_disk_cache():
    cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 3:
                        p, mtime, sz = parts
                        cache[p] = (float(mtime), int(sz))
        except Exception:
            pass
    return cache

def save_disk_cache(cache):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            for p, (mtime, sz) in cache.items():
                f.write(f"{p}|{mtime}|{sz}\n")
    except Exception:
        pass

def calculate_size_multithreaded(target_path, max_workers=16):
    if not os.path.exists(target_path):
        return 0

    try:
        st = os.lstat(target_path)
        if getattr(st, 'st_file_attributes', 0) & 0x400 or os.path.islink(target_path):
            return 0
        if not os.path.isdir(target_path):
            return st.st_size
    except (OSError, PermissionError):
        return 0

    total_bytes = 0
    size_lock = threading.Lock()
    work_q = queue.Queue()
    work_q.put(target_path)

    active_tasks = 0
    active_lock = threading.Lock()
    stop_event = threading.Event()

    def worker():
        nonlocal total_bytes, active_tasks
        while not stop_event.is_set():
            try:
                current_dir = work_q.get(timeout=0.03)
            except queue.Empty:
                with active_lock:
                    if active_tasks == 0 and work_q.empty():
                        stop_event.set()
                        return
                continue

            with active_lock:
                active_tasks += 1

            local_bytes = 0
            try:
                with os.scandir(current_dir) as entries:
                    for entry in entries:
                        try:
                            stat_res = entry.stat(follow_symlinks=False)
                            if getattr(stat_res, 'st_file_attributes', 0) & 0x400:
                                continue
                            if entry.is_dir(follow_symlinks=False):
                                work_q.put(entry.path)
                            else:
                                local_bytes += stat_res.st_size
                        except (PermissionError, OSError):
                            continue
            except (PermissionError, OSError):
                pass
            finally:
                if local_bytes > 0:
                    with size_lock:
                        total_bytes += local_bytes
                with active_lock:
                    active_tasks -= 1
                work_q.task_done()

    threads = []
    num_threads = min(max_workers, 24)
    for _ in range(num_threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return total_bytes

def convert_to_icon(src_image, out_icon):
    try:
        img = Image.open(src_image).convert("RGBA")
        dim = min(img.size)
        left = (img.width - dim) // 2
        top = (img.height - dim) // 2
        cropped = img.crop((left, top, left + dim, top + dim))
        cropped.save(out_icon, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
        return True
    except Exception:
        return False

def create_shortcut(target, destination, icon_path=None):
    try:
        working_dir = os.path.dirname(target)
        icon_line = f'oLink.IconLocation = "{icon_path}"' if (icon_path and os.path.exists(icon_path)) else ""
        vbs_script = f'''
        Set oWS = WScript.CreateObject("WScript.Shell")
        sLinkFile = "{destination}"
        Set oLink = oWS.CreateShortcut(sLinkFile)
        oLink.TargetPath = "{target}"
        oLink.WorkingDirectory = "{working_dir}"
        oLink.Description = "Archive Suite"
        {icon_line}
        oLink.Save
        '''
        vbs_path = os.path.join(os.environ.get("TEMP", os.path.expanduser("~")), "_make_shortcut.vbs")
        with open(vbs_path, "w", encoding="utf-8") as f:
            f.write(vbs_script)
            
        subprocess.run(["wscript", vbs_path], creationflags=0x08000000 if sys.platform == "win32" else 0)
        if os.path.exists(vbs_path):
            os.remove(vbs_path)
            
        return os.path.exists(destination)
    except Exception:
        return False

class CodeUpdateDialog(ctk.CTkToplevel):
    def __init__(self, parent, target_file, on_success, theme_name="Emerald", appearance_mode="Dark"):
        super().__init__(parent)
        self.title("Script Updater")
        self.geometry("840x600")
        self.target_file = target_file
        self.on_success = on_success
        self.palette = THEMES.get(theme_name, THEMES["Emerald"])
        
        self.configure(fg_color="#0b0f17" if appearance_mode == "Dark" else "#e2e8f0")
        self.transient(parent)
        self.grab_set()

        pri = self.palette["primary"]
        txt_main = "#ffffff" if appearance_mode == "Dark" else "#0f172a"
        inner_bg = "#080c12" if appearance_mode == "Dark" else "#f1f5f9"

        header_box = ctk.CTkFrame(self, fg_color="transparent")
        header_box.pack(fill="x", padx=20, pady=(15, 6))

        ctk.CTkLabel(header_box, text="Live Code Inspector & In-App Updater:", font=("Segoe UI", 12, "bold"), text_color=pri).pack(side="left")

        actions_box = ctk.CTkFrame(header_box, fg_color="transparent")
        actions_box.pack(side="right")

        ctk.CTkButton(
            actions_box, text="Copy Code", width=120, height=28,
            font=("Segoe UI", 11, "bold"), fg_color="#1e293b",
            hover_color="#334155", text_color="#ffffff", command=self.copy_code
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            actions_box, text="Paste Code", width=120, height=28,
            font=("Segoe UI", 11, "bold"), fg_color=self.palette["btn_bg"],
            hover_color=self.palette["hover"], text_color="#ffffff", command=self.paste_code
        ).pack(side="left")

        self.editor = ctk.CTkTextbox(
            self, font=("Consolas", 11), fg_color=inner_bg,
            border_color=pri, border_width=1, text_color=txt_main, undo=True
        )
        self.editor.pack(fill="both", expand=True, padx=20, pady=6)

        try:
            with open(self.target_file, "r", encoding="utf-8") as f:
                self.editor.insert("1.0", f.read())
        except Exception: pass

        self.editor.bind("<Control-v>", lambda _: self.paste_code() or "break")
        self.editor.bind("<Control-V>", lambda _: self.paste_code() or "break")

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=20, pady=(10, 15))

        ctk.CTkButton(actions, text="Cancel", width=90, font=("Segoe UI", 11, "bold"), fg_color="#334155", command=self.destroy).pack(side="left")
        ctk.CTkButton(
            actions, text="Apply & Restart Application", font=("Segoe UI", 12, "bold"),
            fg_color=self.palette["btn_bg"], hover_color=self.palette["btn_hover"],
            border_width=1, border_color=pri, text_color="#ffffff", command=self.apply
        ).pack(side="right", fill="x", expand=True, padx=(10, 0))

    def copy_code(self):
        try:
            with open(self.target_file, "r", encoding="utf-8") as f:
                code_data = f.read()
            self.clipboard_clear()
            self.clipboard_append(code_data)
            self.update()
            messagebox.showinfo("Clipboard", "Complete source code copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read source: {e}")

    def paste_code(self):
        try:
            clipboard_text = self.clipboard_get()
            if clipboard_text:
                self.editor.delete("1.0", "end")
                self.editor.insert("1.0", clipboard_text)
        except Exception as e:
            messagebox.showwarning("Warning", f"Could not read clipboard: {e}")

    def apply(self):
        new_code = self.editor.get("1.0", "end-1c").strip()
        if len(new_code) < 50 or "import" not in new_code:
            messagebox.showerror("Error", "Invalid script code provided.")
            return

        try:
            with open(self.target_file, 'w', encoding='utf-8') as f:
                f.write(new_code)
            self.destroy()
            self.on_success()
        except Exception as e:
            messagebox.showerror("Write Error", str(e))

class ArchiveSuiteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Archive Suite")
        self.minsize(980, 680)

        self.config = self.load_config()
        self.disk_cache = load_disk_cache()
        self.cache_lock = threading.Lock()

        raw_theme = self.config.get("theme", "Emerald")
        self.current_theme = THEME_MIGRATION.get(raw_theme, raw_theme)
        if self.current_theme not in THEMES:
            self.current_theme = "Emerald"

        self.current_font = self.config.get("font_profile", "Futuristic (Bahnschrift)")
        if self.current_font not in FONT_PROFILES:
            self.current_font = "Futuristic (Bahnschrift)"

        self.appearance_mode = self.config.get("appearance", "Dark")
        self.working_dir = self.config.get("working_dir", BASE_DIR)
        self.mode = self.config.get("mode", "EXTRACT")
        self.perf_mode = self.config.get("perf_mode", "Extreme")

        if not os.path.exists(self.working_dir):
            self.working_dir = BASE_DIR

        ctk.set_appearance_mode(self.appearance_mode)
        if os.path.exists(ICON_PATH):
            try: self.iconbitmap(ICON_PATH)
            except Exception: pass

        saved_geom = self.config.get("geometry", "1020x720")
        try: self.geometry(saved_geom)
        except Exception: self.geometry("1020x720")

        if self.config.get("maximized", False):
            self.after(100, lambda: self.state("zoomed"))

        self.file_vars = {}
        self.is_scanning = False

        self._apply_appearance_backgrounds()
        self.setup_ui()
        self.apply_theme(self.current_theme)
        self.apply_font(self.current_font)

        self.mode_selector.set("Extract Mode" if self.mode == "EXTRACT" else "Compress Mode")
        self.handle_mode_change(self.mode_selector.get())

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.refresh_list()

    def load_config(self):
        defaults = {
            "geometry": "1020x720", "maximized": False, "font_profile": "Futuristic (Bahnschrift)",
            "theme": "Emerald", "appearance": "Dark", "mode": "EXTRACT",
            "working_dir": BASE_DIR, "auto_purge": True, "isolate_dir": True,
            "use_hub": True, "comp_format": ".7z", "comp_level": "Ultra (9)",
            "perf_mode": "Extreme"
        }
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                    defaults.update(json.load(f))
            except Exception: pass
        t = defaults.get("theme", "Emerald")
        defaults["theme"] = THEME_MIGRATION.get(t, t if t in THEMES else "Emerald")
        return defaults

    def save_config(self):
        is_zoomed = (self.state() == "zoomed")
        geom = self.config.get("geometry", "1020x720") if is_zoomed else self.geometry()
        self.config = {
            "geometry": geom, "maximized": is_zoomed, "font_profile": self.current_font,
            "theme": self.current_theme, "appearance": self.appearance_mode, "mode": self.mode,
            "working_dir": self.working_dir, "auto_purge": self.purge_var.get(),
            "isolate_dir": self.isolate_var.get(), "use_hub": self.hub_var.get(),
            "comp_format": self.format_dropdown.get(), "comp_level": self.level_dropdown.get(),
            "perf_mode": self.perf_picker.get()
        }
        try:
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception: pass

    def on_close(self):
        self.save_config()
        save_disk_cache(self.disk_cache)
        self.destroy()

    def restart_app(self):
        self.save_config()
        save_disk_cache(self.disk_cache)
        script = os.path.abspath(__file__)
        subprocess.Popen([sys.executable.replace("python.exe", "pythonw.exe"), script], creationflags=0x08000000 if sys.platform == "win32" else 0)
        self.destroy()
        sys.exit()

    def _apply_appearance_backgrounds(self):
        if self.appearance_mode == "Dark":
            self.configure(fg_color="#0b0f17")
            self.card_bg = "#121926"
            self.inner_bg = "#080c12"
            self.panel_border = "#1f293d"
            self.text_main = "#f8fafc"
            self.text_muted = "#94a3b8"
        else:
            self.configure(fg_color="#f1f5f9")
            self.card_bg = "#ffffff"
            self.inner_bg = "#f8fafc"
            self.panel_border = "#cbd5e1"
            self.text_main = "#0f172a"
            self.text_muted = "#64748b"

    def setup_ui(self):
        self.header = ctk.CTkFrame(self, fg_color=self.card_bg, corner_radius=12, border_width=1, border_color=self.panel_border)
        self.header.pack(fill="x", padx=16, pady=(12, 4))

        top_row = ctk.CTkFrame(self.header, fg_color="transparent")
        top_row.pack(fill="x", padx=12, pady=(8, 4))

        self.app_title = ctk.CTkLabel(top_row, text="Archive Suite")
        self.app_title.pack(side="left", padx=4)

        ctrls = ctk.CTkFrame(top_row, fg_color="transparent")
        ctrls.pack(side="right")

        self.btn_shortcut = ctk.CTkButton(ctrls, text="Shortcut", width=85, height=30, fg_color="#1e293b", hover_color="#334155", command=self.create_desktop_shortcut)
        self.btn_shortcut.pack(side="left", padx=2)

        self.btn_icon = ctk.CTkButton(ctrls, text="Icon", width=65, height=30, fg_color="#1e293b", hover_color="#334155", command=self.update_icon)
        self.btn_icon.pack(side="left", padx=2)

        self.btn_update = ctk.CTkButton(ctrls, text="Update", width=75, height=30, fg_color="#0369a1", hover_color="#0284c7", command=lambda: CodeUpdateDialog(self, os.path.abspath(__file__), self.restart_app, self.current_theme, self.appearance_mode))
        self.btn_update.pack(side="left", padx=2)

        self.perf_picker = ctk.CTkOptionMenu(ctrls, values=["Normal", "Extreme"], width=95, height=30, command=self.handle_perf_change)
        self.perf_picker.set(self.perf_mode)
        self.perf_picker.pack(side="left", padx=2)

        self.font_picker = ctk.CTkOptionMenu(ctrls, values=list(FONT_PROFILES.keys()), width=175, height=30, command=self.handle_font_change)
        self.font_picker.set(self.current_font)
        self.font_picker.pack(side="left", padx=2)

        self.theme_picker = ctk.CTkOptionMenu(ctrls, values=list(THEMES.keys()), width=115, height=30, command=self.handle_theme_change)
        self.theme_picker.set(self.current_theme)
        self.theme_picker.pack(side="left", padx=2)

        self.btn_mode_toggle = ctk.CTkButton(ctrls, text="Dark" if self.appearance_mode == "Dark" else "Light", width=70, height=30, fg_color="#1e293b", hover_color="#334155", command=self.toggle_appearance)
        self.btn_mode_toggle.pack(side="left", padx=2)

        mode_row = ctk.CTkFrame(self.header, fg_color="transparent")
        mode_row.pack(fill="x", padx=12, pady=(4, 8))
        self.mode_selector = ctk.CTkSegmentedButton(mode_row, values=["Extract Mode", "Compress Mode"], height=36, command=self.handle_mode_change)
        self.mode_selector.pack(fill="x", expand=True)

        self.dir_frame = ctk.CTkFrame(self, fg_color=self.card_bg, corner_radius=10, border_width=1, border_color=self.panel_border)
        self.dir_frame.pack(fill="x", padx=16, pady=4)

        self.lbl_path = ctk.CTkLabel(self.dir_frame, text="Working Path:", text_color=self.text_muted)
        self.lbl_path.pack(side="left", padx=(12, 6), pady=6)

        self.entry_path = ctk.CTkEntry(self.dir_frame, height=32, fg_color=self.inner_bg, border_color=self.panel_border, text_color=self.text_main)
        self.entry_path.insert(0, self.working_dir)
        self.entry_path.pack(side="left", fill="x", expand=True, padx=4, pady=6)
        self.entry_path.bind("<Return>", lambda _: self.refresh_list())

        self.btn_browse = ctk.CTkButton(self.dir_frame, text="Browse", width=95, height=32, fg_color="#1e293b", hover_color="#334155", command=self.choose_directory)
        self.btn_browse.pack(side="right", padx=(4, 10), pady=6)

        self.opts_frame = ctk.CTkFrame(self, fg_color=self.card_bg, corner_radius=10, border_width=1, border_color=self.panel_border)
        self.opts_frame.pack(fill="x", padx=16, pady=4)
        self.opts_frame.grid_columnconfigure((0, 1), weight=1)

        self.purge_var = ctk.BooleanVar(value=self.config.get("auto_purge", True))
        self.chk_purge = ctk.CTkCheckBox(self.opts_frame, text="Delete source files after process", variable=self.purge_var, command=self.save_config)
        self.chk_purge.grid(row=0, column=0, sticky="w", padx=14, pady=8)

        self.hub_var = ctk.BooleanVar(value=self.config.get("use_hub", True))
        self.chk_hub = ctk.CTkCheckBox(self.opts_frame, text="Output to dedicated payload folder", variable=self.hub_var, command=self.save_config)
        self.chk_hub.grid(row=0, column=1, sticky="w", padx=14, pady=8)

        self.isolate_var = ctk.BooleanVar(value=self.config.get("isolate_dir", True))
        self.chk_isolate = ctk.CTkCheckBox(self.opts_frame, text="Extract each archive to individual subfolder", variable=self.isolate_var, command=self.save_config)
        self.chk_isolate.grid(row=1, column=0, sticky="w", padx=14, pady=(0, 8))

        self.btn_select_all = ctk.CTkButton(self.opts_frame, text="Toggle All", width=110, height=30, fg_color="#1e293b", hover_color="#334155", command=self.toggle_all)
        self.btn_select_all.grid(row=1, column=1, sticky="e", padx=14, pady=(0, 8))

        self.format_dropdown = ctk.CTkOptionMenu(self.opts_frame, values=[".7z", ".zip"], height=30, command=lambda _: self.save_config())
        self.format_dropdown.set(self.config.get("comp_format", ".7z"))

        self.level_dropdown = ctk.CTkOptionMenu(
            self.opts_frame, 
            values=["Ultra (9)", "Maximum (7)", "Normal (5)", "Fast (3)", "Store (0)"], 
            height=30,
            command=lambda _: self.save_config()
        )
        self.level_dropdown.set(self.config.get("comp_level", "Ultra (9)"))

        self.list_title = ctk.CTkLabel(self, text="Target Items:", text_color=self.text_muted, anchor="w")
        self.list_title.pack(fill="x", padx=20, pady=(4, 2))

        self.scroll_area = ctk.CTkScrollableFrame(self, height=190, corner_radius=10, fg_color=self.card_bg, border_width=1, border_color=self.panel_border)
        self.scroll_area.pack(fill="both", expand=True, padx=16, pady=4)
        self.scroll_area._parent_canvas.bind("<MouseWheel>", self._on_mousewheel, add="+")

        self.progress_bar = ctk.CTkProgressBar(self, height=10, corner_radius=4)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=16, pady=(6, 4))

        self.log_view = ctk.CTkTextbox(self, height=110, corner_radius=8, fg_color=self.inner_bg, border_width=1, border_color=self.panel_border, text_color=self.text_main)
        self.log_view.pack(fill="both", padx=16, pady=(2, 8))

        bottom_bar = ctk.CTkFrame(self, fg_color="transparent")
        bottom_bar.pack(fill="x", padx=16, pady=(0, 10))

        self.btn_refresh = ctk.CTkButton(bottom_bar, text="Refresh Directory", height=38, command=self.refresh_list)
        self.btn_refresh.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_execute = ctk.CTkButton(bottom_bar, text="Start Extraction", height=38, command=self.start_thread)
        self.btn_execute.pack(side="right", fill="x", expand=True, padx=(6, 0))

    def _on_mousewheel(self, event):
        try:
            self.scroll_area._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass

    def log(self, text):
        self.log_view.insert("end", text + "\n")
        self.log_view.see("end")

    def handle_perf_change(self, mode):
        self.perf_mode = mode
        self.save_config()
        self.log(f"Performance mode set to: {mode}")

    def handle_font_change(self, font_name):
        self.apply_font(font_name)
        self.save_config()
        self.refresh_list()

    def handle_theme_change(self, theme_name):
        if theme_name not in THEMES:
            theme_name = "Emerald"
        self.apply_theme(theme_name)
        self.save_config()
        self.refresh_list()

    def apply_font(self, font_name):
        self.current_font = font_name
        f = FONT_PROFILES.get(font_name, FONT_PROFILES["Futuristic (Bahnschrift)"])

        self.app_title.configure(font=f["title"])
        self.btn_shortcut.configure(font=f["ui_sm"])
        self.btn_icon.configure(font=f["ui_sm"])
        self.btn_update.configure(font=f["ui_sm"])
        self.perf_picker.configure(font=f["ui_sm"], dropdown_font=f["ui_sm"])
        self.font_picker.configure(font=f["ui_sm"], dropdown_font=f["ui_sm"])
        self.theme_picker.configure(font=f["ui_sm"], dropdown_font=f["ui_sm"])
        self.btn_mode_toggle.configure(font=f["ui_bold"])
        self.mode_selector.configure(font=f["ui_bold"])
        self.lbl_path.configure(font=f["ui_bold"])
        self.entry_path.configure(font=f["mono"])
        self.btn_browse.configure(font=f["ui_bold"])
        self.chk_purge.configure(font=f["ui_bold"])
        self.chk_hub.configure(font=f["ui_bold"])
        self.chk_isolate.configure(font=f["ui_bold"])
        self.btn_select_all.configure(font=f["ui_bold"])
        self.format_dropdown.configure(font=f["ui_sm"], dropdown_font=f["ui_sm"])
        self.level_dropdown.configure(font=f["ui_sm"], dropdown_font=f["ui_sm"])
        self.list_title.configure(font=f["ui_bold"])
        self.log_view.configure(font=f["mono"])
        self.btn_refresh.configure(font=f["ui_bold"])
        self.btn_execute.configure(font=f["ui_bold"])

    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        palette = THEMES.get(theme_name, THEMES["Emerald"])
        pri = palette["primary"]

        self.app_title.configure(text_color=pri)
        self.progress_bar.configure(progress_color=pri)
        self.mode_selector.configure(selected_color=pri, selected_hover_color=palette["hover"])
        self.btn_execute.configure(fg_color=palette["btn_bg"], hover_color=palette["btn_hover"], border_color=pri, border_width=1, text_color="#fff")
        self.btn_refresh.configure(fg_color=palette["btn_bg"], hover_color=palette["btn_hover"], border_color=pri, border_width=1, text_color="#fff")
        
        self.perf_picker.configure(fg_color=palette["menu_bg"], button_color=pri, button_hover_color=palette["hover"])
        self.font_picker.configure(fg_color=palette["menu_bg"], button_color=pri, button_hover_color=palette["hover"])
        self.theme_picker.configure(fg_color=palette["menu_bg"], button_color=pri, button_hover_color=palette["hover"])
        self.format_dropdown.configure(fg_color=palette["menu_bg"], button_color=pri, button_hover_color=palette["hover"])
        self.level_dropdown.configure(fg_color=palette["menu_bg"], button_color=pri, button_hover_color=palette["hover"])

        self.chk_purge.configure(fg_color=pri, hover_color=palette["hover"])
        self.chk_hub.configure(fg_color=pri, hover_color=palette["hover"])
        self.chk_isolate.configure(fg_color=pri, hover_color=palette["hover"])

    def toggle_appearance(self):
        self.appearance_mode = "Light" if self.appearance_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(self.appearance_mode)
        self.btn_mode_toggle.configure(text="Dark" if self.appearance_mode == "Dark" else "Light")
        self._apply_appearance_backgrounds()

        self.header.configure(fg_color=self.card_bg, border_color=self.panel_border)
        self.dir_frame.configure(fg_color=self.card_bg, border_color=self.panel_border)
        self.opts_frame.configure(fg_color=self.card_bg, border_color=self.panel_border)
        self.scroll_area.configure(fg_color=self.card_bg, border_color=self.panel_border)
        self.entry_path.configure(fg_color=self.inner_bg, border_color=self.panel_border, text_color=self.text_main)
        self.log_view.configure(fg_color=self.inner_bg, border_color=self.panel_border, text_color=self.text_main)
        self.lbl_path.configure(text_color=self.text_muted)
        self.list_title.configure(text_color=self.text_muted)

        self.apply_theme(self.current_theme)
        self.save_config()
        self.refresh_list()

    def handle_mode_change(self, value):
        if "Compress" in value:
            self.mode = "COMPRESS"
            self.list_title.configure(text="Raw Items for Compression:")
            self.btn_execute.configure(text="Start Compression")
            self.chk_isolate.grid_forget()
            self.btn_select_all.grid_forget()
            self.format_dropdown.grid(row=1, column=0, sticky="w", padx=14, pady=(0, 8))
            self.level_dropdown.grid(row=1, column=1, sticky="w", padx=14, pady=(0, 8))
        else:
            self.mode = "EXTRACT"
            self.list_title.configure(text="Detected Archives:")
            self.btn_execute.configure(text="Start Extraction")
            self.format_dropdown.grid_forget()
            self.level_dropdown.grid_forget()
            self.chk_isolate.grid(row=1, column=0, sticky="w", padx=14, pady=(0, 8))
            self.btn_select_all.grid(row=1, column=1, sticky="e", padx=14, pady=(0, 8))

        self.save_config()
        self.refresh_list()

    def choose_directory(self):
        folder = filedialog.askdirectory(initialdir=self.working_dir)
        if folder:
            self.working_dir = os.path.abspath(folder)
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, self.working_dir)
            self.save_config()
            self.refresh_list()

    def create_desktop_shortcut(self):
        desktop_dir = ""
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
            desktop_dir, _ = winreg.QueryValueEx(key, "Desktop")
            desktop_dir = os.path.expandvars(desktop_dir)
        except Exception:
            desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")

        desktop_lnk = os.path.join(desktop_dir, "Archive Suite.lnk")
        icon = ICON_PATH if os.path.exists(ICON_PATH) else None

        if create_shortcut(os.path.abspath(__file__), desktop_lnk, icon):
            messagebox.showinfo("Success", f"Shortcut created on Desktop:\n{desktop_lnk}")
        else:
            messagebox.showerror("Error", "Could not create shortcut. Check permissions.")

    def update_icon(self):
        file = filedialog.askopenfilename(filetypes=IMAGE_FORMATS)
        if file and convert_to_icon(file, ICON_PATH):
            try: self.iconbitmap(ICON_PATH)
            except Exception: pass
            messagebox.showinfo("Success", "Icon updated.")

    def toggle_all(self):
        if not self.file_vars: return
        target = not all(v.get() for v in self.file_vars.values())
        for v in self.file_vars.values(): v.set(target)

    def refresh_list(self):
        if self.is_scanning: return
        typed_path = self.entry_path.get().strip()
        if os.path.isdir(typed_path):
            self.working_dir = os.path.abspath(typed_path)

        if not os.path.exists(self.working_dir):
            self.log(f"Invalid path: {self.working_dir}")
            return

        self.is_scanning = True
        self.btn_refresh.configure(state="disabled", text="Scanning...")

        for w in self.scroll_area.winfo_children(): w.destroy()
        self.file_vars.clear()

        threading.Thread(target=self._scan_worker, daemon=True).start()

    def _scan_worker(self):
        start_time = time.time()
        try:
            all_items = os.listdir(self.working_dir)
        except Exception:
            all_items = []

        if self.mode == "EXTRACT":
            targets = [f for f in all_items if f.lower().endswith(ARCHIVE_FORMATS)]
        else:
            targets = [
                f for f in all_items 
                if f not in ("_EXTRACTED", "_COMPRESSED", "config.json", "app_icon.ico", "scan_cache.txt")
                and not f.startswith('.') 
                and not (os.path.isfile(os.path.join(self.working_dir, f)) and f.lower().endswith(ARCHIVE_FORMATS))
                and not f.endswith(('.py', '.pyw', '.exe', '.bat'))
            ]

        cpu_threads = os.cpu_count() or 4
        if self.perf_mode == "Extreme":
            top_workers = max(16, cpu_threads * 2)
            sub_workers = 16
        else:
            top_workers = 4
            sub_workers = 2

        cache_hits = 0
        cache_hits_lock = threading.Lock()

        def process_item(item):
            nonlocal cache_hits
            p = os.path.join(self.working_dir, item)
            is_dir = os.path.isdir(p)
            try:
                current_mtime = os.path.getmtime(p)
            except OSError:
                current_mtime = 0

            size_bytes = None
            with self.cache_lock:
                if p in self.disk_cache:
                    cached_mtime, cached_sz = self.disk_cache[p]
                    if abs(cached_mtime - current_mtime) < 0.001:
                        size_bytes = cached_sz
                        with cache_hits_lock:
                            cache_hits += 1

            if size_bytes is None:
                size_bytes = calculate_size_multithreaded(p, max_workers=sub_workers)
                with self.cache_lock:
                    self.disk_cache[p] = (current_mtime, size_bytes)

            return (item, size_bytes, is_dir)

        with ThreadPoolExecutor(max_workers=top_workers) as executor:
            processed = list(executor.map(process_item, targets))

        save_disk_cache(self.disk_cache)
        elapsed = time.time() - start_time
        self.after(0, lambda: self.log(
            f"Indexed {len(targets)} item(s) in {elapsed:.2f}s ({self.perf_mode} mode | Cache hits: {cache_hits}/{len(targets)})"
        ))
        self.after(0, lambda: self._render_scanned_items(processed))

    def _render_scanned_items(self, targets):
        for w in self.scroll_area.winfo_children(): w.destroy()
        self.file_vars.clear()

        f = FONT_PROFILES.get(self.current_font, FONT_PROFILES["Futuristic (Bahnschrift)"])
        if not targets:
            ctk.CTkLabel(self.scroll_area, text="No items found.", font=f["ui_bold"], text_color=self.text_muted).pack(pady=25)
        else:
            palette = THEMES.get(self.current_theme, THEMES["Emerald"])
            badge_bg = palette["badge_dark"] if self.appearance_mode == "Dark" else palette["badge_light"]
            badge_fg = palette["badge_text_dark"] if self.appearance_mode == "Dark" else palette["badge_text_light"]

            for item, size_bytes, is_dir in targets:
                icon_tag = "📁" if is_dir else "📄"
                size_str = format_size(size_bytes)
                var = ctk.BooleanVar(value=True)

                row_frame = ctk.CTkFrame(self.scroll_area, fg_color="transparent", corner_radius=8)
                row_frame.pack(fill="x", padx=4, pady=2)

                left_box = ctk.CTkFrame(row_frame, fg_color="transparent")
                left_box.pack(side="left", fill="x", expand=True, padx=4, pady=3)

                chk = ctk.CTkCheckBox(
                    left_box, text="", variable=var, width=20,
                    fg_color=palette["primary"], hover_color=palette["hover"]
                )
                chk.pack(side="left", padx=(4, 6))

                lbl_icon = ctk.CTkLabel(left_box, text=icon_tag, font=("Segoe UI Emoji", 12))
                lbl_icon.pack(side="left", padx=(0, 6))

                display_name = item if len(item) <= 45 else item[:42] + "..."
                lbl_name = ctk.CTkLabel(
                    left_box, text=display_name, font=f["row_main"],
                    text_color=self.text_main, anchor="w"
                )
                lbl_name.pack(side="left", fill="x", expand=True)

                right_box = ctk.CTkFrame(row_frame, fg_color="transparent")
                right_box.pack(side="right", padx=6, pady=3)

                lbl_size = ctk.CTkLabel(
                    right_box, text=f" {size_str} ", font=f["badge"],
                    fg_color=badge_bg, text_color=badge_fg, corner_radius=6, height=24
                )
                lbl_size.pack(side="left", padx=4)

                self.file_vars[item] = var

        # Force scrollregion update to fix empty canvas rendering
        self.update_idletasks()
        try:
            canvas = self.scroll_area._parent_canvas
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.yview_moveto(0.0)
        except Exception:
            pass

        self.btn_refresh.configure(state="normal", text="Refresh Directory")
        self.is_scanning = False

    def run_tasks(self):
        items = [name for name, var in self.file_vars.items() if var.get()]
        if not items:
            self.log("No items selected.")
            self.toggle_ui(True)
            return

        total = len(items)
        out_hub = os.path.join(self.working_dir, "_EXTRACTED" if self.mode == "EXTRACT" else "_COMPRESSED")

        for idx, item in enumerate(items, 1):
            item_path = os.path.join(self.working_dir, item)
            self.log(f"[{idx}/{total}] Processing: {item}")
            try:
                if self.mode == "EXTRACT":
                    dest = os.path.join(out_hub if self.hub_var.get() else self.working_dir, os.path.splitext(item)[0] if self.isolate_var.get() else "")
                    os.makedirs(dest, exist_ok=True)
                    ext = os.path.splitext(item)[1].lower()

                    if ext == '.zip':
                        with zipfile.ZipFile(item_path, 'r') as z: z.extractall(dest)
                    elif ext in ('.7z', '.rar'):
                        subprocess.run(["7z", "x", item_path, f"-o{dest}", "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x08000000 if sys.platform == "win32" else 0)
                else:
                    dest_dir = out_hub if self.hub_var.get() else self.working_dir
                    os.makedirs(dest_dir, exist_ok=True)
                    fmt = self.format_dropdown.get()
                    out_archive = os.path.join(dest_dir, f"{item}{fmt}")
                    level = int(self.level_dropdown.get().split("(")[1].replace(")", ""))

                    if fmt == ".zip":
                        comp = zipfile.ZIP_STORED if level == 0 else zipfile.ZIP_DEFLATED
                        with zipfile.ZipFile(out_archive, 'w', comp, compresslevel=level if level > 0 else None) as z:
                            if os.path.isfile(item_path): z.write(item_path, arcname=item)
                            else:
                                for root, _, files in os.walk(item_path):
                                    for file in files:
                                        fp = os.path.join(root, file)
                                        z.write(fp, arcname=os.path.join(item, os.path.relpath(fp, item_path)))
                    elif fmt == ".7z":
                        subprocess.run(["7z", "a", "-t7z", f"-mx={level}", out_archive, item_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x08000000 if sys.platform == "win32" else 0)

                if self.purge_var.get():
                    shutil.rmtree(item_path) if os.path.isdir(item_path) else os.remove(item_path)
                    with self.cache_lock:
                        self.disk_cache.pop(item_path, None)

                self.log(f"Done: {item}")
            except Exception as e:
                self.log(f"Error: {e}")

            self.progress_bar.set(idx / total)

        save_disk_cache(self.disk_cache)
        self.log("Batch processing complete.")
        self.toggle_ui(True)
        self.refresh_list()

    def toggle_ui(self, enabled):
        state = "normal" if enabled else "disabled"
        self.btn_execute.configure(state=state)
        self.btn_refresh.configure(state=state)
        self.btn_browse.configure(state=state)
        self.btn_select_all.configure(state=state)

    def start_thread(self):
        self.toggle_ui(False)
        self.progress_bar.set(0)
        threading.Thread(target=self.run_tasks, daemon=True).start()

if __name__ == "__main__":
    app = ArchiveSuiteApp()
    app.mainloop()
