import os
import sys
import subprocess
import json
import shutil
import threading
import zipfile
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
    import tkinter as tk

    root = tk.Tk()
    root.title("Matrix Engine // Dependency Resolver")
    root.geometry("500x300")
    root.resizable(False, False)
    root.configure(bg="#080b0e")

    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    root.geometry(f"500x300+{int((ws-500)/2)}+{int((hs-300)/2)}")

    tk.Label(root, text="[!] MISSING SYSTEM DEPENDENCIES", font=("Consolas", 13, "bold"), fg="#ff3355", bg="#080b0e").pack(pady=(20, 8))
    tk.Label(root, text="The following required Python libraries were not located:", font=("Segoe UI", 10), fg="#94a3b8", bg="#080b0e").pack()

    list_frame = tk.Frame(root, bg="#0e161c", bd=1, relief="solid")
    list_frame.pack(fill="x", padx=30, pady=12)
    for pkg in missing:
        tk.Label(list_frame, text=f"• {pkg}", font=("Consolas", 11, "bold"), fg="#00ff66", bg="#0e161c").pack(anchor="w", padx=15, pady=3)

    def install_and_restart():
        root.destroy()
        py_exe = sys.executable
        if py_exe.lower().endswith("pythonw.exe"):
            py_exe = py_exe[:-10] + "python.exe"

        script_path = os.path.abspath(__file__)
        bat_cmd = f"""@echo off
title Installing Dependencies...
echo [*] Installing missing packages: {" ".join(missing)}
"{py_exe}" -m pip install --upgrade pip {" ".join(missing)}
echo.
echo [*] Launching application...
start "" "{sys.executable}" "{script_path}"
exit
"""
        bat_file = os.path.join(os.environ.get("TEMP", "."), "_install_matrix_deps.bat")
        with open(bat_file, "w", encoding="utf-8") as f:
            f.write(bat_cmd)
        
        subprocess.Popen(f'start "" "{bat_file}"', shell=True)
        sys.exit()

    btn_frame = tk.Frame(root, bg="#080b0e")
    btn_frame.pack(fill="x", padx=30, pady=(10, 15))
    tk.Button(btn_frame, text="EXIT", font=("Segoe UI", 10, "bold"), bg="#1e293b", fg="#ffffff", bd=0, padx=15, pady=6, command=sys.exit).pack(side="left")
    tk.Button(btn_frame, text="[► INSTALL DEPENDENCIES & LAUNCH]", font=("Segoe UI", 10, "bold"), bg="#005a24", fg="#00ff66", bd=0, padx=15, pady=6, command=install_and_restart).pack(side="right")

    root.mainloop()
    sys.exit()

from PIL import Image
import customtkinter as ctk

SCRIPT_FILE = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_FILE)
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")
APP_ICON_FILE = os.path.join(SCRIPT_DIR, "app_icon.ico")

ARCHIVE_EXTS = ('.zip', '.7z', '.rar')
IMAGE_EXTS = (('Image Files', '*.png;*.jpg;*.jpeg;*.webp;*.bmp;*.ico'), ('All Files', '*.*'))
DEFAULT_EXTRACT_HUB = "_EXTRACTED_PAYLOADS"
DEFAULT_COMPRESS_HUB = "_COMPRESSED_PAYLOADS"

FONT_PROFILES = {
    "Retro Matrix (Consolas)": {
        "title": ("Consolas", 17, "bold"), "ui_bold": ("Consolas", 12, "bold"),
        "ui_sm": ("Consolas", 11, "bold"), "file": ("Consolas", 12, "bold"), "console": ("Consolas", 11, "bold")
    },
    "Modern Bold (Segoe UI)": {
        "title": ("Segoe UI", 16, "bold"), "ui_bold": ("Segoe UI", 12, "bold"),
        "ui_sm": ("Segoe UI", 11, "bold"), "file": ("Segoe UI", 12, "bold"), "console": ("Consolas", 11, "bold")
    },
    "Cyber Terminal (Lucida Console)": {
        "title": ("Lucida Console", 15, "bold"), "ui_bold": ("Lucida Console", 11, "bold"),
        "ui_sm": ("Lucida Console", 10, "bold"), "file": ("Lucida Console", 11, "bold"), "console": ("Lucida Console", 10, "bold")
    },
    "Clean Roboto (Arial)": {
        "title": ("Arial", 16, "bold"), "ui_bold": ("Arial", 12, "bold"),
        "ui_sm": ("Arial", 11, "bold"), "file": ("Arial", 12, "bold"), "console": ("Consolas", 11, "bold")
    },
    "Developer Mono (Cascadia Mono)": {
        "title": ("Cascadia Mono", 15, "bold"), "ui_bold": ("Cascadia Mono", 11, "bold"),
        "ui_sm": ("Cascadia Mono", 10, "bold"), "file": ("Cascadia Mono", 11, "bold"), "console": ("Cascadia Mono", 10, "bold")
    },
    "Arcade Bold (Trebuchet MS)": {
        "title": ("Trebuchet MS", 16, "bold"), "ui_bold": ("Trebuchet MS", 12, "bold"),
        "ui_sm": ("Trebuchet MS", 11, "bold"), "file": ("Trebuchet MS", 12, "bold"), "console": ("Consolas", 11, "bold")
    },
    "Tactical Heavy (Impact)": {
        "title": ("Impact", 18), "ui_bold": ("Impact", 13), "ui_sm": ("Impact", 11),
        "file": ("Consolas", 12, "bold"), "console": ("Consolas", 11, "bold")
    },
    "Minimalist (Century Gothic)": {
        "title": ("Century Gothic", 16, "bold"), "ui_bold": ("Century Gothic", 12, "bold"),
        "ui_sm": ("Century Gothic", 10, "bold"), "file": ("Century Gothic", 11, "bold"), "console": ("Consolas", 11, "bold")
    },
    "Futuristic Clean (Bahnschrift)": {
        "title": ("Bahnschrift", 16, "bold"), "ui_bold": ("Bahnschrift", 12, "bold"),
        "ui_sm": ("Bahnschrift", 11, "bold"), "file": ("Bahnschrift", 12, "bold"), "console": ("Consolas", 11, "bold")
    },
    "Classic System (Courier New)": {
        "title": ("Courier New", 16, "bold"), "ui_bold": ("Courier New", 12, "bold"),
        "ui_sm": ("Courier New", 10, "bold"), "file": ("Courier New", 12, "bold"), "console": ("Courier New", 11, "bold")
    }
}

THEME_PALETTES = {
    "Green": {"primary": "#00ff66", "hover": "#00cc52", "border": "#10b981", "dark_bg": "#005a24", "dark_hover": "#008033"},
    "Red": {"primary": "#ff3355", "hover": "#e61e3f", "border": "#f43f5e", "dark_bg": "#7f1d1d", "dark_hover": "#991b1b"},
    "Blue": {"primary": "#38bdf8", "hover": "#0ea5e9", "border": "#0284c7", "dark_bg": "#0369a1", "dark_hover": "#0284c7"},
    "Yellow": {"primary": "#facc15", "hover": "#eab308", "border": "#ca8a04", "dark_bg": "#854d0e", "dark_hover": "#a16207"},
    "Purple": {"primary": "#c084fc", "hover": "#a855f7", "border": "#9333ea", "dark_bg": "#581c87", "dark_hover": "#6b21a8"},
    "Turquoise": {"primary": "#2dd4bf", "hover": "#14b8a6", "border": "#0d9488", "dark_bg": "#115e59", "dark_hover": "#0f766e"}
}

def process_and_save_ico(input_image_path, output_ico_path):
    try:
        img = Image.open(input_image_path).convert("RGBA")
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        cropped_img = img.crop((left, top, left + min_dim, top + min_dim))
        sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        cropped_img.save(output_ico_path, format="ICO", sizes=sizes)
        return True
    except Exception:
        return False

def make_desktop_shortcut(target, link_path, icon_path=None):
    try:
        working_dir = os.path.dirname(target)
        icon_line = f'oLink.IconLocation = "{icon_path}"' if (icon_path and os.path.exists(icon_path)) else ""
        vbs_script = f'''
        Set oWS = WScript.CreateObject("WScript.Shell")
        sLinkFile = "{link_path}"
        Set oLink = oWS.CreateShortcut(sLinkFile)
        oLink.TargetPath = "{target}"
        oLink.WorkingDirectory = "{working_dir}"
        oLink.Description = "Matrix Storage Suite"
        {icon_line}
        oLink.Save
        '''
        vbs_path = os.path.join(os.environ.get("TEMP", os.path.expanduser("~")), "_make_shortcut.vbs")
        with open(vbs_path, "w", encoding="utf-8") as f:
            f.write(vbs_script)
            
        subprocess.run(["wscript", vbs_path], creationflags=0x08000000 if sys.platform == "win32" else 0)
        if os.path.exists(vbs_path):
            os.remove(vbs_path)
            
        return os.path.exists(link_path)
    except Exception:
        return False

class HotCodeUpdaterModal(ctk.CTkToplevel):
    def __init__(self, parent, target_file, restart_callback, theme_color="Green", appearance_mode="Dark"):
        super().__init__(parent)
        self.title("Matrix Hot-Code Engine Overhaul")
        self.geometry("860x620")
        self.target_file = target_file
        self.restart_callback = restart_callback
        self.palette = THEME_PALETTES.get(theme_color, THEME_PALETTES["Green"])
        
        bg_color = "#080b0e" if appearance_mode == "Dark" else "#e2e8f0"
        self.configure(fg_color=bg_color)
        self.transient(parent)
        self.grab_set()

        pri = self.palette["primary"]
        txt_main = "#ffffff" if appearance_mode == "Dark" else "#0f172a"
        inner_bg = "#050709" if appearance_mode == "Dark" else "#f1f5f9"

        header_box = ctk.CTkFrame(self, fg_color="transparent")
        header_box.pack(fill="x", padx=20, pady=(16, 6))

        lbl = ctk.CTkLabel(header_box, text="[❖] CODE PAYLOAD INJECTION / EXPORT:", font=("Consolas", 13, "bold"), text_color=pri)
        lbl.pack(side="left")

        actions_box = ctk.CTkFrame(header_box, fg_color="transparent")
        actions_box.pack(side="right")

        ctk.CTkButton(
            actions_box, text="📋 COPY CODE", width=120, height=28,
            font=("Segoe UI", 11, "bold"), fg_color="#1e293b",
            hover_color="#334155", text_color="#ffffff", command=self.copy_current_code
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            actions_box, text="📥 PASTE CODE", width=120, height=28,
            font=("Segoe UI", 11, "bold"), fg_color=self.palette["dark_bg"],
            hover_color=self.palette["hover"], text_color=pri if appearance_mode == "Dark" else "#ffffff", command=self.paste_from_clipboard
        ).pack(side="left")

        self.txt_code = ctk.CTkTextbox(
            self, font=("Consolas", 11), fg_color=inner_bg,
            border_color=pri, border_width=1, text_color=txt_main, undo=True
        )
        self.txt_code.pack(fill="both", expand=True, padx=20, pady=8)

        try:
            with open(self.target_file, "r", encoding="utf-8") as f:
                self.txt_code.insert("1.0", f.read())
        except Exception:
            pass

        self.txt_code.bind("<Control-v>", lambda _: self.paste_from_clipboard() or "break")
        self.txt_code.bind("<Control-V>", lambda _: self.paste_from_clipboard() or "break")

        btn_box = ctk.CTkFrame(self, fg_color="transparent")
        btn_box.pack(fill="x", padx=20, pady=(0, 16))

        ctk.CTkButton(btn_box, text="CANCEL", width=110, font=("Segoe UI", 11, "bold"), fg_color="#1e293b", command=self.destroy).pack(side="left")
        ctk.CTkButton(
            btn_box, text="[► INJECT CODE & RESTART INSTANCE]", font=("Segoe UI", 12, "bold"),
            fg_color=self.palette["dark_bg"], hover_color=self.palette["dark_hover"],
            border_width=1, border_color=pri, text_color=pri if appearance_mode == "Dark" else "#ffffff",
            command=self.apply_update
        ).pack(side="right", fill="x", expand=True, padx=(10, 0))

    def copy_current_code(self):
        try:
            with open(self.target_file, "r", encoding="utf-8") as f:
                code_data = f.read()
            self.clipboard_clear()
            self.clipboard_append(code_data)
            self.update()
            messagebox.showinfo("Clipboard", "Complete application code copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read source: {e}")

    def paste_from_clipboard(self):
        try:
            clipboard_text = self.clipboard_get()
            if clipboard_text:
                self.txt_code.delete("1.0", "end")
                self.txt_code.insert("1.0", clipboard_text)
        except Exception as e:
            messagebox.showwarning("Clipboard Warning", f"Could not access clipboard: {e}")

    def apply_update(self):
        code = self.txt_code.get("1.0", "end-1c").strip()
        if len(code) < 50 or "import" not in code:
            messagebox.showerror("Payload Error", "Invalid script payload provided.")
            return

        try:
            with open(self.target_file, 'w', encoding='utf-8') as f:
                f.write(code)
            messagebox.showinfo("Success", "Engine updated successfully! Restarting instance...")
            self.destroy()
            self.restart_callback()
        except Exception as e:
            messagebox.showerror("Write Error", f"Failed to rewrite source: {str(e)}")

class MatrixArchiveSuite(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MATRIX // STORAGE_ENGINE_SUITE_V6.0")
        self.minsize(1120, 800)

        self.config = self.load_config()

        if os.path.exists(APP_ICON_FILE):
            try: self.iconbitmap(APP_ICON_FILE)
            except Exception: pass

        saved_geometry = self.config.get("window_geometry", "1180x960")
        try: self.geometry(saved_geometry)
        except Exception: self.geometry("1180x960")

        if self.config.get("is_maximized", False):
            self.after(100, lambda: self.state("zoomed"))

        self.current_font_profile = self.config.get("font_profile", "Retro Matrix (Consolas)")
        self.current_theme_color = self.config.get("theme_color", "Green")
        self.current_appearance = self.config.get("appearance_mode", "Dark")
        self.target_dir = self.config.get("target_dir", SCRIPT_DIR)
        self.active_mode = self.config.get("active_mode", "EXTRACT")

        if not os.path.exists(self.target_dir):
            self.target_dir = SCRIPT_DIR

        ctk.set_appearance_mode(self.current_appearance)

        self.file_vars = {}
        self.checkbox_widgets = []
        self.is_processing = False
        self.is_scanning = False

        self._apply_appearance_backgrounds()
        self._build_matrix_ui()
        self.apply_theme(self.current_theme_color)
        self.apply_font_profile(self.current_font_profile)

        if self.active_mode == "COMPRESS":
            self.mode_switcher.set("📦 COMPRESS RAW MODE")
            self.on_mode_change("📦 COMPRESS RAW MODE")
        else:
            self.mode_switcher.set("⚡ EXTRACT PAYLOAD MODE")
            self.on_mode_change("⚡ EXTRACT PAYLOAD MODE")

        self.protocol("WM_DELETE_WINDOW", self.on_app_close)
        self.refresh_file_list()

    def load_config(self):
        default_cfg = {
            "window_geometry": "1180x960", "is_maximized": False,
            "font_profile": "Retro Matrix (Consolas)", "theme_color": "Green",
            "appearance_mode": "Dark", "active_mode": "EXTRACT",
            "target_dir": SCRIPT_DIR,
            "auto_purge": True, "isolate_dir": True, "route_hub": True,
            "compress_format": ".7z (Ultra Fast/Solid)", "compress_level": "Ultra (9 - Highest Ratio)"
        }
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    default_cfg.update(json.load(f))
            except Exception: pass
        return default_cfg

    def save_config(self):
        try:
            is_max = (self.state() == "zoomed")
            current_geom = self.config.get("window_geometry", "1180x960") if is_max else self.geometry()

            self.config = {
                "window_geometry": current_geom, "is_maximized": is_max,
                "font_profile": self.current_font_profile, "theme_color": self.current_theme_color,
                "appearance_mode": self.current_appearance, "active_mode": self.active_mode,
                "target_dir": self.target_dir, "auto_purge": self.delete_var.get(),
                "isolate_dir": self.isolate_var.get(), "route_hub": self.hub_var.get(),
                "compress_format": self.compress_fmt_menu.get(), "compress_level": self.compress_level_menu.get()
            }
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except Exception: pass

    def on_app_close(self):
        self.save_config()
        self.destroy()

    def restart_application(self):
        self.save_config()
        subprocess.Popen([sys.executable.replace("python.exe", "pythonw.exe"), SCRIPT_FILE], creationflags=0x08000000 if sys.platform == "win32" else 0)
        self.destroy()
        sys.exit()

    def open_hot_updater(self):
        HotCodeUpdaterModal(self, SCRIPT_FILE, self.restart_application, self.current_theme_color, self.current_appearance)

    def create_desktop_shortcut_now(self):
        desktop_dir = ""
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
            desktop_dir, _ = winreg.QueryValueEx(key, "Desktop")
            desktop_dir = os.path.expandvars(desktop_dir)
        except Exception:
            desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")

        desktop_lnk = os.path.join(desktop_dir, "Matrix Storage Suite.lnk")
        icon_arg = APP_ICON_FILE if os.path.exists(APP_ICON_FILE) else None
        
        if make_desktop_shortcut(SCRIPT_FILE, desktop_lnk, icon_path=icon_arg):
            messagebox.showinfo("Success", f"[❖] DESKTOP PAYLOAD LINK GENERATED:\n{desktop_lnk}")
        else:
            messagebox.showerror("Error", "[!] Failed to establish desktop shortcut link.")

    def change_app_icon_live(self):
        img_p = filedialog.askopenfilename(title="Select New Icon / Image File", filetypes=IMAGE_EXTS)
        if img_p:
            if process_and_save_ico(img_p, APP_ICON_FILE):
                try:
                    self.iconbitmap(APP_ICON_FILE)
                    messagebox.showinfo("Icon Updated", "App icon generated and applied successfully!")
                except Exception as e:
                    messagebox.showwarning("Warning", f"Icon saved, restart app to fully reflect: {e}")

    def _apply_appearance_backgrounds(self):
        if self.current_appearance == "Dark":
            self.configure(fg_color="#080b0e")
            self.card_bg = "#0d1318"
            self.inner_bg = "#050709"
            self.panel_border = "#1e2d38"
            self.text_main = "#ffffff"
            self.text_muted = "#94a3b8"
        else:
            self.configure(fg_color="#e2e8f0")
            self.card_bg = "#cbd5e1"
            self.inner_bg = "#f1f5f9"
            self.panel_border = "#94a3b8"
            self.text_main = "#0f172a"
            self.text_muted = "#334155"

    def _build_matrix_ui(self):
        f = FONT_PROFILES.get(self.current_font_profile, FONT_PROFILES["Retro Matrix (Consolas)"])

        self.header_frame = ctk.CTkFrame(self, fg_color=self.card_bg, corner_radius=12, border_width=1, border_color=self.panel_border)
        self.header_frame.pack(fill="x", padx=20, pady=(12, 6))

        top_bar = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        top_bar.pack(fill="x", padx=12, pady=(8, 4))

        self.title_lbl = ctk.CTkLabel(top_bar, text="[❖] MATRIX STORAGE SUITE", font=f["title"], text_color="#00ff66")
        self.title_lbl.pack(side="left", padx=6, pady=4)

        ctrl_top_box = ctk.CTkFrame(top_bar, fg_color="transparent")
        ctrl_top_box.pack(side="right", padx=4, pady=4)

        self.btn_shortcut = ctk.CTkButton(ctrl_top_box, text="📌 SHORTCUT", width=110, font=f["ui_sm"], fg_color="#1e293b", hover_color="#334155", command=self.create_desktop_shortcut_now)
        self.btn_shortcut.pack(side="left", padx=3)

        self.btn_change_icon = ctk.CTkButton(ctrl_top_box, text="🖼️ ICON", width=70, font=f["ui_sm"], fg_color="#581c87", hover_color="#6b21a8", command=self.change_app_icon_live)
        self.btn_change_icon.pack(side="left", padx=3)

        self.btn_update = ctk.CTkButton(ctrl_top_box, text="⚡ UPDATE", width=80, font=f["ui_sm"], fg_color="#0369a1", hover_color="#0284c7", command=self.open_hot_updater)
        self.btn_update.pack(side="left", padx=3)

        self.font_menu = ctk.CTkOptionMenu(ctrl_top_box, values=list(FONT_PROFILES.keys()), command=self.on_font_selected, width=175, font=f["ui_sm"], dropdown_font=f["ui_sm"])
        self.font_menu.set(self.current_font_profile)
        self.font_menu.pack(side="left", padx=3)

        self.theme_menu = ctk.CTkOptionMenu(ctrl_top_box, values=list(THEME_PALETTES.keys()), command=self.on_theme_selected, width=105, font=f["ui_sm"], dropdown_font=f["ui_sm"])
        self.theme_menu.set(self.current_theme_color)
        self.theme_menu.pack(side="left", padx=3)

        self.btn_toggle_mode = ctk.CTkButton(ctrl_top_box, text="🌙 DARK" if self.current_appearance == "Dark" else "☀️ LIGHT", width=80, font=f["ui_sm"], fg_color="#1e293b", hover_color="#334155", command=self.toggle_appearance_mode)
        self.btn_toggle_mode.pack(side="left", padx=3)

        mode_bar = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        mode_bar.pack(fill="x", padx=12, pady=(2, 8))

        self.mode_switcher = ctk.CTkSegmentedButton(
            mode_bar, 
            values=["⚡ EXTRACT PAYLOAD MODE", "📦 COMPRESS RAW MODE"], 
            command=self.on_mode_change, 
            font=f["ui_bold"], 
            height=38
        )
        self.mode_switcher.pack(fill="x", expand=True, padx=4)

        self.dir_frame = ctk.CTkFrame(self, fg_color=self.card_bg, corner_radius=10, border_width=1, border_color=self.panel_border)
        self.dir_frame.pack(fill="x", padx=20, pady=4)

        self.dir_lbl = ctk.CTkLabel(self.dir_frame, text="TARGET DIRECTORY:", font=f["ui_bold"], text_color=self.text_muted)
        self.dir_lbl.pack(side="left", padx=(14, 8), pady=8)

        self.dir_entry = ctk.CTkEntry(self.dir_frame, font=f["console"], fg_color=self.inner_bg, border_color=self.panel_border, text_color=self.text_main, height=34)
        self.dir_entry.insert(0, self.target_dir)
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=6, pady=8)

        self.btn_browse = ctk.CTkButton(self.dir_frame, text="[📁 BROWSE]", width=120, font=f["ui_bold"], fg_color="#1e293b", hover_color="#334155", command=self.browse_directory, height=34)
        self.btn_browse.pack(side="right", padx=(6, 14), pady=8)

        self.opts_frame = ctk.CTkFrame(self, fg_color=self.card_bg, corner_radius=10, border_width=1, border_color=self.panel_border)
        self.opts_frame.pack(fill="x", padx=20, pady=4)
        self.opts_frame.grid_columnconfigure(0, weight=1)
        self.opts_frame.grid_columnconfigure(1, weight=1)

        self.delete_var = ctk.BooleanVar(value=self.config.get("auto_purge", True))
        self.delete_chk = ctk.CTkCheckBox(self.opts_frame, text="[AUTO_PURGE] Wipe source items post-operation", variable=self.delete_var, font=f["ui_bold"], text_color="#ca8a04" if self.current_appearance == "Light" else "#facc15", checkmark_color="#080b0e", command=self.save_config)
        self.delete_chk.grid(row=0, column=0, sticky="w", padx=16, pady=(10, 5))

        self.hub_var = ctk.BooleanVar(value=self.config.get("route_hub", True))
        self.hub_chk = ctk.CTkCheckBox(self.opts_frame, text=f"[TARGET_HUB] Route all into '{DEFAULT_EXTRACT_HUB}'", variable=self.hub_var, font=f["ui_bold"], text_color=self.text_main, checkmark_color="#080b0e", command=self.save_config)
        self.hub_chk.grid(row=0, column=1, sticky="w", padx=16, pady=(10, 5))

        self.isolate_var = ctk.BooleanVar(value=self.config.get("isolate_dir", True))
        self.isolate_chk = ctk.CTkCheckBox(self.opts_frame, text="[ISOLATE_DIR] Extract into separate folder per archive", variable=self.isolate_var, font=f["ui_bold"], text_color=self.text_main, checkmark_color="#080b0e", command=self.save_config)
        self.isolate_chk.grid(row=1, column=0, sticky="w", padx=16, pady=(5, 10))

        self.btn_select_all = ctk.CTkButton(self.opts_frame, text="TOGGLE ALL", width=130, font=f["ui_bold"], command=self.toggle_all_selection, fg_color="#1e293b", hover_color="#334155", border_width=1, border_color=self.panel_border)
        self.btn_select_all.grid(row=1, column=1, sticky="e", padx=16, pady=(5, 10))

        self.compress_fmt_menu = ctk.CTkOptionMenu(self.opts_frame, values=[".7z (Ultra Fast/Solid)", ".zip (Universal Compatibility)"], font=f["ui_bold"], dropdown_font=f["ui_bold"], height=32, command=lambda _: self.save_config())
        self.compress_fmt_menu.set(self.config.get("compress_format", ".7z (Ultra Fast/Solid)"))

        self.compress_level_menu = ctk.CTkOptionMenu(self.opts_frame, values=["Ultra (9 - Highest Ratio)", "Maximum (7 - High)", "Normal (5 - Balanced)", "Fast (3 - Quick)", "Store (0 - Packing Only)"], font=f["ui_bold"], dropdown_font=f["ui_bold"], height=32, command=lambda _: self.save_config())
        self.compress_level_menu.set(self.config.get("compress_level", "Ultra (9 - Highest Ratio)"))

        self.list_lbl = ctk.CTkLabel(self, text=">>> DETECTED ARCHIVES PAYLOAD:", anchor="w", font=f["ui_bold"], text_color=self.text_muted)
        self.list_lbl.pack(fill="x", padx=22, pady=(4, 2))

        self.scroll_frame = ctk.CTkScrollableFrame(self, height=190, corner_radius=10, fg_color=self.card_bg, border_width=1, border_color=self.panel_border)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=4)

        self.progress = ctk.CTkProgressBar(self, height=12, corner_radius=4)
        self.progress.set(0)
        self.progress.configure(fg_color="#334155" if self.current_appearance == "Dark" else "#94a3b8")
        self.progress.pack(fill="x", padx=20, pady=(8, 4))

        console_lbl = ctk.CTkLabel(self, text=">>> SYSTEM ACTIVITY LOG:", anchor="w", font=f["ui_bold"], text_color=self.text_muted)
        console_lbl.pack(fill="x", padx=22, pady=(4, 2))

        self.console = ctk.CTkTextbox(self, height=140, font=f["console"], corner_radius=10, fg_color=self.inner_bg, border_width=1, border_color=self.panel_border, text_color=self.text_main)
        self.console.pack(fill="both", padx=20, pady=(0, 8))

        self.console.tag_config("primary", foreground="#00ff66")
        self.console.tag_config("cyan", foreground="#00f0ff")
        self.console.tag_config("crimson", foreground="#ff3366")
        self.console.tag_config("gold", foreground="#facc15")
        self.console.tag_config("ghost", foreground="#94a3b8")

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 14))

        self.btn_refresh = ctk.CTkButton(btn_frame, text="[⟳ SCAN DIRECTORY]", font=f["ui_bold"], fg_color="#0f172a" if self.current_appearance == "Dark" else "#475569", hover_color="#1e293b" if self.current_appearance == "Dark" else "#334155", border_width=1, border_color=self.panel_border, text_color="#ffffff", command=self.refresh_file_list, height=44)
        self.btn_refresh.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.btn_start = ctk.CTkButton(btn_frame, text="[► INITIALIZE EXTRACTION]", font=f["ui_bold"], command=self.start_thread, height=44)
        self.btn_start.pack(side="right", fill="x", expand=True, padx=(8, 0))

    def on_font_selected(self, font_name):
        self.apply_font_profile(font_name)
        self.save_config()

    def on_theme_selected(self, theme_name):
        self.apply_theme(theme_name)
        self.save_config()

    def apply_font_profile(self, profile_name):
        self.current_font_profile = profile_name
        f = FONT_PROFILES.get(profile_name, FONT_PROFILES["Retro Matrix (Consolas)"])

        self.title_lbl.configure(font=f["title"])
        self.btn_shortcut.configure(font=f["ui_sm"])
        self.btn_update.configure(font=f["ui_sm"])
        self.btn_change_icon.configure(font=f["ui_sm"])
        self.font_menu.configure(font=f["ui_sm"], dropdown_font=f["ui_sm"])
        self.theme_menu.configure(font=f["ui_sm"], dropdown_font=f["ui_sm"])
        self.btn_toggle_mode.configure(font=f["ui_sm"])
        self.mode_switcher.configure(font=f["ui_bold"])
        self.dir_lbl.configure(font=f["ui_bold"])
        self.dir_entry.configure(font=f["console"])
        self.btn_browse.configure(font=f["ui_bold"])
        self.delete_chk.configure(font=f["ui_bold"])
        self.hub_chk.configure(font=f["ui_bold"])
        self.isolate_chk.configure(font=f["ui_bold"])
        self.btn_select_all.configure(font=f["ui_bold"])
        self.compress_fmt_menu.configure(font=f["ui_bold"], dropdown_font=f["ui_bold"])
        self.compress_level_menu.configure(font=f["ui_bold"], dropdown_font=f["ui_bold"])
        self.list_lbl.configure(font=f["ui_bold"])
        self.console.configure(font=f["console"])
        self.btn_refresh.configure(font=f["ui_bold"])
        self.btn_start.configure(font=f["ui_bold"])

        for chk in self.checkbox_widgets:
            chk.configure(font=f["file"])

    def toggle_appearance_mode(self):
        if self.current_appearance == "Dark":
            self.current_appearance = "Light"
            ctk.set_appearance_mode("Light")
            self.btn_toggle_mode.configure(text="☀️ LIGHT")
        else:
            self.current_appearance = "Dark"
            ctk.set_appearance_mode("Dark")
            self.btn_toggle_mode.configure(text="🌙 DARK")

        self._apply_appearance_backgrounds()
        self.header_frame.configure(fg_color=self.card_bg, border_color=self.panel_border)
        self.dir_frame.configure(fg_color=self.card_bg, border_color=self.panel_border)
        self.opts_frame.configure(fg_color=self.card_bg, border_color=self.panel_border)
        self.scroll_frame.configure(fg_color=self.card_bg, border_color=self.panel_border)
        self.dir_entry.configure(fg_color=self.inner_bg, border_color=self.panel_border, text_color=self.text_main)
        self.console.configure(fg_color=self.inner_bg, border_color=self.panel_border, text_color=self.text_main)
        self.list_lbl.configure(text_color=self.text_muted)
        self.dir_lbl.configure(text_color=self.text_muted)
        self.isolate_chk.configure(text_color=self.text_main)
        self.hub_chk.configure(text_color=self.text_main)
        self.delete_chk.configure(text_color="#ca8a04" if self.current_appearance == "Light" else "#facc15")
        self.progress.configure(fg_color="#334155" if self.current_appearance == "Dark" else "#94a3b8")
        self.btn_refresh.configure(fg_color="#0f172a" if self.current_appearance == "Dark" else "#475569", hover_color="#1e293b" if self.current_appearance == "Dark" else "#334155", border_color=self.panel_border)

        self.apply_theme(self.current_theme_color)
        self.save_config()
        self.refresh_file_list()

    def apply_theme(self, theme_name):
        self.current_theme_color = theme_name
        palette = THEME_PALETTES.get(theme_name, THEME_PALETTES["Green"])
        pri = palette["primary"]

        self.title_lbl.configure(text_color=pri)
        self.header_frame.configure(border_color=pri)
        self.progress.configure(progress_color=pri)
        self.console.configure(border_color=pri)
        self.console.tag_config("primary", foreground=pri)

        self.mode_switcher.configure(selected_color=pri, selected_hover_color=palette["hover"], text_color="#080b0e" if self.current_appearance == "Dark" else "#ffffff")
        self.theme_menu.configure(fg_color=palette["dark_bg"], button_color=pri, button_hover_color=palette["hover"])
        self.font_menu.configure(fg_color=palette["dark_bg"], button_color=pri, button_hover_color=palette["hover"])
        self.compress_fmt_menu.configure(fg_color=palette["dark_bg"], button_color=pri, button_hover_color=palette["hover"])
        self.compress_level_menu.configure(fg_color=palette["dark_bg"], button_color=pri, button_hover_color=palette["hover"])

        self.btn_start.configure(fg_color=palette["dark_bg"], hover_color=palette["dark_hover"], border_width=1, border_color=pri, text_color=pri if self.current_appearance == "Dark" else "#ffffff")
        self.delete_chk.configure(fg_color=pri, hover_color=palette["hover"])
        self.isolate_chk.configure(fg_color=pri, hover_color=palette["hover"])
        self.hub_chk.configure(fg_color=pri, hover_color=palette["hover"])

    def on_mode_change(self, value):
        if "COMPRESS" in value:
            self.active_mode = "COMPRESS"
            self.list_lbl.configure(text=">>> DETECTED RAW PAYLOADS (FOLDERS & ROMS):")
            self.btn_start.configure(text="[► INITIALIZE COMPRESSION PIPELINE]")
            self.isolate_chk.grid_forget()
            self.btn_select_all.grid_forget()
            self.compress_fmt_menu.grid(row=1, column=0, sticky="w", padx=16, pady=(5, 10))
            self.compress_level_menu.grid(row=1, column=1, sticky="w", padx=16, pady=(5, 10))
            self.hub_chk.configure(text=f"[TARGET_HUB] Route all into '{DEFAULT_COMPRESS_HUB}'")
        else:
            self.active_mode = "EXTRACT"
            self.list_lbl.configure(text=">>> DETECTED ARCHIVES PAYLOAD:")
            self.btn_start.configure(text="[► INITIALIZE EXTRACTION]")
            self.compress_fmt_menu.grid_forget()
            self.compress_level_menu.grid_forget()
            self.isolate_chk.grid(row=1, column=0, sticky="w", padx=16, pady=(5, 10))
            self.btn_select_all.grid(row=1, column=1, sticky="e", padx=16, pady=(5, 10))
            self.hub_chk.configure(text=f"[TARGET_HUB] Route all into '{DEFAULT_EXTRACT_HUB}'")

        self.save_config()
        self.refresh_file_list()

    def log(self, text, color_tag="primary"):
        self.console.insert("end", text + "\n", color_tag)
        self.console.see("end")

    def browse_directory(self):
        selected_dir = filedialog.askdirectory(initialdir=self.target_dir, title="Select Operational Directory")
        if selected_dir:
            self.target_dir = os.path.abspath(selected_dir)
            self.dir_entry.delete(0, "end")
            self.dir_entry.insert(0, self.target_dir)
            self.save_config()
            self.refresh_file_list()

    def toggle_all_selection(self):
        if not self.file_vars: return
        new_val = not all(v.get() for v in self.file_vars.values())
        for var in self.file_vars.values():
            var.set(new_val)

    def get_path_size(self, path):
        if os.path.isfile(path): return os.path.getsize(path)
        total_size = 0
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                total_size += os.path.getsize(os.path.join(dirpath, f))
        return total_size

    def refresh_file_list(self):
        if self.is_scanning: return
        custom_path = self.dir_entry.get().strip()
        if os.path.isdir(custom_path):
            self.target_dir = os.path.abspath(custom_path)

        if not os.path.exists(self.target_dir):
            self.log(f"[WARN] Invalid Path: {self.target_dir}", "crimson")
            return

        self.is_scanning = True
        self.btn_refresh.configure(state="disabled", text="[SCANNING...]")

        for widget in self.scroll_frame.winfo_children(): widget.destroy()
        self.file_vars.clear()
        self.checkbox_widgets.clear()

        threading.Thread(target=self._scan_thread_worker, daemon=True).start()

    def _scan_thread_worker(self):
        try:
            all_items = os.listdir(self.target_dir)
        except Exception:
            all_items = []

        if self.active_mode == "EXTRACT":
            targets = [f for f in all_items if f.lower().endswith(ARCHIVE_EXTS)]
        else:
            targets = [f for f in all_items if f not in (DEFAULT_EXTRACT_HUB, DEFAULT_COMPRESS_HUB, "config.json", "app_icon.ico")
                       and not f.startswith('.') and not (os.path.isfile(os.path.join(self.target_dir, f)) and f.lower().endswith(ARCHIVE_EXTS))
                       and not f.endswith(('.py', '.pyw', '.exe', '.ico', '.bat'))]

        processed = []
        for name in targets:
            item_path = os.path.join(self.target_dir, name)
            size_mb = self.get_path_size(item_path) / (1024 * 1024)
            is_dir = os.path.isdir(item_path)
            processed.append((name, size_mb, is_dir))

        self.after(0, lambda: self._render_file_list(processed))

    def _render_file_list(self, targets):
        f = FONT_PROFILES.get(self.current_font_profile, FONT_PROFILES["Retro Matrix (Consolas)"])
        if not targets:
            empty_msg = "[!] NO ARCHIVES LOCATED." if self.active_mode == "EXTRACT" else "[!] NO RAW FILES/FOLDERS FOR COMPRESSION."
            lbl = ctk.CTkLabel(self.scroll_frame, text=empty_msg, font=f["ui_bold"], text_color=self.text_muted)
            lbl.pack(pady=35)
        else:
            palette = THEME_PALETTES[self.current_theme_color]
            for name, size_mb, is_dir in targets:
                icon_tag = "📁" if is_dir else "📄"
                var = ctk.BooleanVar(value=True)
                chk = ctk.CTkCheckBox(
                    self.scroll_frame, text=f"{icon_tag} {name:<45} [{size_mb:>7.2f} MB]",
                    variable=var, font=f["file"], text_color=self.text_main,
                    fg_color=palette["primary"], hover_color=palette["hover"], checkmark_color="#080b0e"
                )
                chk.pack(anchor="w", padx=12, pady=4)
                self.file_vars[name] = var
                self.checkbox_widgets.append(chk)

            self.log(f"[SYS] Indexed {len(targets)} item(s) in: {self.target_dir} ({self.active_mode})", "cyan")

        self.btn_refresh.configure(state="normal", text="[⟳ SCAN DIRECTORY]")
        self.is_scanning = False

    def resolve_extract_dest(self, filename):
        name_without_ext = os.path.splitext(filename)[0]
        base_dir = os.path.join(self.target_dir, DEFAULT_EXTRACT_HUB) if self.hub_var.get() else self.target_dir
        dest_dir = os.path.join(base_dir, name_without_ext) if self.isolate_var.get() else base_dir
        os.makedirs(dest_dir, exist_ok=True)
        return dest_dir

    def extract_file(self, filename):
        file_path = os.path.join(self.target_dir, filename)
        dest_dir = self.resolve_extract_dest(filename)
        ext = os.path.splitext(filename)[1].lower()

        if ext == '.zip':
            with zipfile.ZipFile(file_path, 'r') as archive:
                archive.extractall(dest_dir)
        elif ext in ('.7z', '.rar'):
            cmd = ["7z", "x", file_path, f"-o{dest_dir}", "-y"]
            creation_flags = 0x08000000 if sys.platform == "win32" else 0
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=creation_flags)
            if res.returncode != 0: raise RuntimeError(f"7z Engine failed to extract {ext} archive.")
        return dest_dir

    def get_compression_level_digit(self):
        c = self.compress_level_menu.get()
        if "Ultra" in c: return 9
        if "Maximum" in c: return 7
        if "Normal" in c: return 5
        if "Fast" in c: return 3
        return 0

    def compress_item(self, item_name):
        item_path = os.path.join(self.target_dir, item_name)
        target_format = ".7z" if ".7z" in self.compress_fmt_menu.get() else ".zip"
        level_digit = self.get_compression_level_digit()
        base_dir = os.path.join(self.target_dir, DEFAULT_COMPRESS_HUB) if self.hub_var.get() else self.target_dir
        os.makedirs(base_dir, exist_ok=True)

        archive_path = os.path.join(base_dir, f"{item_name}{target_format}")
        if target_format == ".zip":
            comp_mode = zipfile.ZIP_STORED if level_digit == 0 else zipfile.ZIP_DEFLATED
            compresslevel = 9 if level_digit >= 7 else (level_digit if level_digit > 0 else None)
            kwargs = {'compression': comp_mode}
            if compresslevel is not None: kwargs['compresslevel'] = compresslevel

            with zipfile.ZipFile(archive_path, 'w', **kwargs) as zipf:
                if os.path.isfile(item_path): zipf.write(item_path, arcname=item_name)
                else:
                    for root, _, files in os.walk(item_path):
                        for file in files:
                            full_p = os.path.join(root, file)
                            zipf.write(full_p, arcname=os.path.join(item_name, os.path.relpath(full_p, item_path)))

        elif target_format == ".7z":
            cmd = ["7z", "a", "-t7z", f"-mx={level_digit}", archive_path, item_path]
            creation_flags = 0x08000000 if sys.platform == "win32" else 0
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=creation_flags)
            if res.returncode != 0: raise RuntimeError("7z Engine compression failed.")
        return archive_path

    def run_pipeline(self):
        selected_items = [name for name, var in self.file_vars.items() if var.get()]
        total = len(selected_items)
        if total == 0:
            self.log("[WARN] Pipeline aborted: No items targeted.", "crimson")
            self.set_ui_state(True)
            return

        mode_title = "EXTRACTION" if self.active_mode == "EXTRACT" else "COMPRESSION"
        self.log(f"[EXEC] Initializing {mode_title} Pipeline: {total} items queued...", "cyan")

        for idx, item_name in enumerate(selected_items, start=1):
            item_path = os.path.join(self.target_dir, item_name)
            self.log(f"[{idx}/{total}] Processing: {item_name}", "gold")
            try:
                if self.active_mode == "EXTRACT":
                    dest_path = self.extract_file(item_name)
                    self.log(f"  └─► [OK] Extracted To: ./{os.path.relpath(dest_path, self.target_dir)}", "primary")
                else:
                    dest_archive = self.compress_item(item_name)
                    self.log(f"  └─► [OK] Packed Into: ./{os.path.relpath(dest_archive, self.target_dir)}", "primary")
                
                if self.delete_var.get():
                    shutil.rmtree(item_path) if os.path.isdir(item_path) else os.remove(item_path)
                    self.log(f"  └─► [PURGED] Source payload deleted.", "ghost")
            except Exception as e:
                self.log(f"  └─► [FAIL] Error: {str(e)}", "crimson")

            self.progress.set(idx / total)

        self.log(f"[SUCCESS] All targeted {mode_title.lower()} tasks completed.", "primary")
        self.set_ui_state(True)
        self.refresh_file_list()

    def set_ui_state(self, enabled):
        state = "normal" if enabled else "disabled"
        self.btn_start.configure(state=state)
        self.btn_refresh.configure(state=state)
        self.btn_browse.configure(state=state)
        self.btn_select_all.configure(state=state)
        self.mode_switcher.configure(state=state)
        self.btn_toggle_mode.configure(state=state)
        self.theme_menu.configure(state=state)
        self.font_menu.configure(state=state)
        self.btn_update.configure(state=state)
        self.btn_change_icon.configure(state=state)
        self.btn_shortcut.configure(state=state)

    def start_thread(self):
        self.set_ui_state(False)
        self.progress.set(0)
        thread = threading.Thread(target=self.run_pipeline, daemon=True)
        thread.start()

if __name__ == "__main__":
    app = MatrixArchiveSuite()
    app.mainloop()
