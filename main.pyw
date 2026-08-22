import os
import sys
import json
import shutil
import threading
import zipfile
import subprocess
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
    root.title("Missing Requirements")
    root.geometry("450x260")
    root.resizable(False, False)
    root.configure(bg="#111827")

    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    root.geometry(f"450x260+{int((ws-450)/2)}+{int((hs-260)/2)}")

    tk.Label(root, text="Missing Python Packages", font=("Segoe UI", 12, "bold"), fg="#f87171", bg="#111827").pack(pady=(20, 5))
    tk.Label(root, text="The following dependencies need to be installed:", font=("Segoe UI", 9), fg="#9ca3af", bg="#111827").pack()

    box = tk.Frame(root, bg="#1f2937", bd=1, relief="solid")
    box.pack(fill="x", padx=30, pady=10)
    for pkg in missing:
        tk.Label(box, text=f"• {pkg}", font=("Consolas", 10, "bold"), fg="#34d399", bg="#1f2937").pack(anchor="w", padx=12, pady=2)

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

    btns = tk.Frame(root, bg="#111827")
    btns.pack(fill="x", padx=30, pady=(10, 15))
    tk.Button(btns, text="Cancel", font=("Segoe UI", 9), bg="#374151", fg="#fff", bd=0, padx=14, pady=5, command=sys.exit).pack(side="left")
    tk.Button(btns, text="Install Packages", font=("Segoe UI", 9, "bold"), bg="#059669", fg="#fff", bd=0, padx=14, pady=5, command=install_pkgs).pack(side="right")
    
    root.mainloop()
    sys.exit()

from PIL import Image
import customtkinter as ctk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
ICON_PATH = os.path.join(BASE_DIR, "app_icon.ico")

ARCHIVE_FORMATS = ('.zip', '.7z', '.rar')
IMAGE_FORMATS = (('Images', '*.png;*.jpg;*.jpeg;*.webp;*.bmp;*.ico'), ('All Files', '*.*'))

THEMES = {
    "Green": {"primary": "#10b981", "hover": "#059669", "btn_bg": "#064e3b", "btn_hover": "#047857"},
    "Red": {"primary": "#f43f5e", "hover": "#e11d48", "btn_bg": "#881337", "btn_hover": "#9f1239"},
    "Blue": {"primary": "#0ea5e9", "hover": "#0284c7", "btn_bg": "#0c4a6e", "btn_hover": "#0369a1"},
    "Yellow": {"primary": "#eab308", "hover": "#ca8a04", "btn_bg": "#713f12", "btn_hover": "#854d0e"},
    "Purple": {"primary": "#a855f7", "hover": "#9333ea", "btn_bg": "#581c87", "btn_hover": "#6b21a8"},
    "Teal": {"primary": "#14b8a6", "hover": "#0d9488", "btn_bg": "#134e4a", "btn_hover": "#115e59"}
}

FONTS = {
    "Segoe UI": {"title": ("Segoe UI", 16, "bold"), "ui": ("Segoe UI", 11, "bold"), "mono": ("Consolas", 11, "bold")},
    "Consolas": {"title": ("Consolas", 16, "bold"), "ui": ("Consolas", 11, "bold"), "mono": ("Consolas", 11, "bold")},
    "Cascadia Mono": {"title": ("Cascadia Mono", 14, "bold"), "ui": ("Cascadia Mono", 10, "bold"), "mono": ("Cascadia Mono", 10, "bold")},
    "Lucida Console": {"title": ("Lucida Console", 14, "bold"), "ui": ("Lucida Console", 10, "bold"), "mono": ("Lucida Console", 10, "bold")},
    "Arial": {"title": ("Arial", 15, "bold"), "ui": ("Arial", 11, "bold"), "mono": ("Consolas", 11, "bold")},
    "Trebuchet MS": {"title": ("Trebuchet MS", 15, "bold"), "ui": ("Trebuchet MS", 11, "bold"), "mono": ("Consolas", 11, "bold")},
    "Impact": {"title": ("Impact", 17), "ui": ("Impact", 12), "mono": ("Consolas", 11, "bold")},
    "Century Gothic": {"title": ("Century Gothic", 15, "bold"), "ui": ("Century Gothic", 10, "bold"), "mono": ("Consolas", 11, "bold")},
    "Bahnschrift": {"title": ("Bahnschrift", 15, "bold"), "ui": ("Bahnschrift", 11, "bold"), "mono": ("Consolas", 11, "bold")},
    "Courier New": {"title": ("Courier New", 15, "bold"), "ui": ("Courier New", 10, "bold"), "mono": ("Courier New", 10, "bold")}
}

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
    def __init__(self, parent, target_file, on_success, theme_name="Green", appearance_mode="Dark"):
        super().__init__(parent)
        self.title("Script Updater")
        self.geometry("840x600")
        self.target_file = target_file
        self.on_success = on_success
        self.palette = THEMES.get(theme_name, THEMES["Green"])
        
        self.configure(fg_color="#0f172a" if appearance_mode == "Dark" else "#e2e8f0")
        self.transient(parent)
        self.grab_set()

        pri = self.palette["primary"]
        txt_main = "#ffffff" if appearance_mode == "Dark" else "#0f172a"
        inner_bg = "#020617" if appearance_mode == "Dark" else "#f1f5f9"

        header_box = ctk.CTkFrame(self, fg_color="transparent")
        header_box.pack(fill="x", padx=20, pady=(15, 6))

        ctk.CTkLabel(header_box, text="Live Code Inspector & In-App Updater:", font=("Segoe UI", 12, "bold"), text_color=pri).pack(side="left")

        actions_box = ctk.CTkFrame(header_box, fg_color="transparent")
        actions_box.pack(side="right")

        ctk.CTkButton(
            actions_box, text="📋 Copy Code", width=120, height=28,
            font=("Segoe UI", 11, "bold"), fg_color="#1e293b",
            hover_color="#334155", text_color="#ffffff", command=self.copy_code
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            actions_box, text="📥 Paste Code", width=120, height=28,
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
        self.minsize(1050, 750)

        self.config = self.load_config()
        self.current_theme = self.config.get("theme", "Green")
        self.current_font = self.config.get("font", "Segoe UI")
        self.appearance_mode = self.config.get("appearance", "Dark")
        self.working_dir = self.config.get("working_dir", BASE_DIR)
        self.mode = self.config.get("mode", "EXTRACT")

        if not os.path.exists(self.working_dir):
            self.working_dir = BASE_DIR

        ctk.set_appearance_mode(self.appearance_mode)
        if os.path.exists(ICON_PATH):
            try: self.iconbitmap(ICON_PATH)
            except Exception: pass

        saved_geom = self.config.get("geometry", "1120x900")
        try: self.geometry(saved_geom)
        except Exception: self.geometry("1120x900")

        if self.config.get("maximized", False):
            self.after(100, lambda: self.state("zoomed"))

        self.file_vars = {}
        self.checkbox_refs = []
        self.is_scanning = False

        self.setup_ui()
        self.apply_theme(self.current_theme)
        self.apply_font(self.current_font)

        self.mode_selector.set("Extract Mode" if self.mode == "EXTRACT" else "Compress Mode")
        self.handle_mode_change(self.mode_selector.get())

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.refresh_list()

    def load_config(self):
        defaults = {
            "geometry": "1120x900", "maximized": False, "font": "Segoe UI",
            "theme": "Green", "appearance": "Dark", "mode": "EXTRACT",
            "working_dir": BASE_DIR, "auto_purge": True, "isolate_dir": True,
            "use_hub": True, "comp_format": ".7z", "comp_level": "Ultra (9)"
        }
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                    defaults.update(json.load(f))
            except Exception: pass
        return defaults

    def save_config(self):
        is_zoomed = (self.state() == "zoomed")
        geom = self.config.get("geometry", "1120x900") if is_zoomed else self.geometry()
        self.config = {
            "geometry": geom, "maximized": is_zoomed, "font": self.current_font,
            "theme": self.current_theme, "appearance": self.appearance_mode, "mode": self.mode,
            "working_dir": self.working_dir, "auto_purge": self.purge_var.get(),
            "isolate_dir": self.isolate_var.get(), "use_hub": self.hub_var.get(),
            "comp_format": self.format_dropdown.get(), "comp_level": self.level_dropdown.get()
        }
        try:
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception: pass

    def on_close(self):
        self.save_config()
        self.destroy()

    def restart_app(self):
        self.save_config()
        script = os.path.abspath(__file__)
        subprocess.Popen([sys.executable.replace("python.exe", "pythonw.exe"), script], creationflags=0x08000000 if sys.platform == "win32" else 0)
        self.destroy()
        sys.exit()

    def setup_ui(self):
        self.header = ctk.CTkFrame(self, corner_radius=10)
        self.header.pack(fill="x", padx=16, pady=(12, 6))

        top_row = ctk.CTkFrame(self.header, fg_color="transparent")
        top_row.pack(fill="x", padx=10, pady=(8, 4))

        self.app_title = ctk.CTkLabel(top_row, text="Archive Suite")
        self.app_title.pack(side="left", padx=6)

        ctrls = ctk.CTkFrame(top_row, fg_color="transparent")
        ctrls.pack(side="right")

        self.btn_shortcut = ctk.CTkButton(ctrls, text="Create Shortcut", width=110, fg_color="#334155", hover_color="#475569", command=self.create_desktop_shortcut)
        self.btn_shortcut.pack(side="left", padx=3)

        self.btn_icon = ctk.CTkButton(ctrls, text="Set Icon", width=80, fg_color="#475569", hover_color="#64748b", command=self.update_icon)
        self.btn_icon.pack(side="left", padx=3)

        self.btn_update = ctk.CTkButton(ctrls, text="Update", width=75, fg_color="#0369a1", hover_color="#0284c7", command=lambda: CodeUpdateDialog(self, os.path.abspath(__file__), self.restart_app, self.current_theme, self.appearance_mode))
        self.btn_update.pack(side="left", padx=3)

        self.font_picker = ctk.CTkOptionMenu(ctrls, values=list(FONTS.keys()), width=130, command=self.handle_font_change)
        self.font_picker.set(self.current_font)
        self.font_picker.pack(side="left", padx=3)

        self.theme_picker = ctk.CTkOptionMenu(ctrls, values=list(THEMES.keys()), width=95, command=self.handle_theme_change)
        self.theme_picker.set(self.current_theme)
        self.theme_picker.pack(side="left", padx=3)

        self.btn_mode_toggle = ctk.CTkButton(ctrls, text="Mode", width=65, fg_color="#1e293b", hover_color="#334155", command=self.toggle_appearance)
        self.btn_mode_toggle.pack(side="left", padx=3)

        mode_row = ctk.CTkFrame(self.header, fg_color="transparent")
        mode_row.pack(fill="x", padx=10, pady=(4, 8))
        self.mode_selector = ctk.CTkSegmentedButton(mode_row, values=["Extract Mode", "Compress Mode"], height=36, command=self.handle_mode_change)
        self.mode_selector.pack(fill="x", expand=True)

        self.dir_frame = ctk.CTkFrame(self, corner_radius=8)
        self.dir_frame.pack(fill="x", padx=16, pady=4)

        self.lbl_path = ctk.CTkLabel(self.dir_frame, text="Working Path:")
        self.lbl_path.pack(side="left", padx=(12, 6), pady=8)

        self.entry_path = ctk.CTkEntry(self.dir_frame)
        self.entry_path.insert(0, self.working_dir)
        self.entry_path.pack(side="left", fill="x", expand=True, padx=6, pady=8)

        self.btn_browse = ctk.CTkButton(self.dir_frame, text="Browse", width=100, fg_color="#334155", hover_color="#475569", command=self.choose_directory)
        self.btn_browse.pack(side="right", padx=(6, 12), pady=8)

        self.opts_frame = ctk.CTkFrame(self, corner_radius=8)
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

        self.btn_select_all = ctk.CTkButton(self.opts_frame, text="Select / Deselect All", width=140, fg_color="#334155", hover_color="#475569", command=self.toggle_all)
        self.btn_select_all.grid(row=1, column=1, sticky="e", padx=14, pady=(0, 8))

        self.format_dropdown = ctk.CTkOptionMenu(self.opts_frame, values=[".7z", ".zip"], command=lambda _: self.save_config())
        self.format_dropdown.set(self.config.get("comp_format", ".7z"))

        self.level_dropdown = ctk.CTkOptionMenu(
            self.opts_frame, 
            values=["Ultra (9)", "Maximum (7)", "Normal (5)", "Fast (3)", "Store (0)"], 
            command=lambda _: self.save_config()
        )
        self.level_dropdown.set(self.config.get("comp_level", "Ultra (9)"))

        self.list_title = ctk.CTkLabel(self, text="Target Items:", anchor="w")
        self.list_title.pack(fill="x", padx=20, pady=(6, 2))

        self.scroll_area = ctk.CTkScrollableFrame(self, height=180, corner_radius=8)
        self.scroll_area.pack(fill="both", expand=True, padx=16, pady=4)

        self.progress_bar = ctk.CTkProgressBar(self, height=10, corner_radius=4)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=16, pady=(6, 4))

        self.log_view = ctk.CTkTextbox(self, height=130, font=("Consolas", 10), corner_radius=8)
        self.log_view.pack(fill="both", padx=16, pady=(2, 8))

        bottom_bar = ctk.CTkFrame(self, fg_color="transparent")
        bottom_bar.pack(fill="x", padx=16, pady=(0, 12))

        self.btn_refresh = ctk.CTkButton(bottom_bar, text="Refresh Directory", fg_color="#334155", hover_color="#475569", height=40, command=self.refresh_list)
        self.btn_refresh.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_execute = ctk.CTkButton(bottom_bar, text="Start Extraction", height=40, command=self.start_thread)
        self.btn_execute.pack(side="right", fill="x", expand=True, padx=(6, 0))

    def log(self, text):
        self.log_view.insert("end", text + "\n")
        self.log_view.see("end")

    def handle_font_change(self, font_name):
        self.apply_font(font_name)
        self.save_config()

    def handle_theme_change(self, theme_name):
        self.apply_theme(theme_name)
        self.save_config()

    def apply_font(self, font_name):
        self.current_font = font_name
        f = FONTS.get(font_name, FONTS["Segoe UI"])

        self.app_title.configure(font=f["title"])
        self.btn_shortcut.configure(font=f["ui"])
        self.btn_icon.configure(font=f["ui"])
        self.btn_update.configure(font=f["ui"])
        self.font_picker.configure(font=f["ui"], dropdown_font=f["ui"])
        self.theme_picker.configure(font=f["ui"], dropdown_font=f["ui"])
        self.btn_mode_toggle.configure(font=f["ui"])
        self.mode_selector.configure(font=f["ui"])
        self.lbl_path.configure(font=f["ui"])
        self.entry_path.configure(font=f["mono"])
        self.btn_browse.configure(font=f["ui"])
        self.chk_purge.configure(font=f["ui"])
        self.chk_hub.configure(font=f["ui"])
        self.chk_isolate.configure(font=f["ui"])
        self.btn_select_all.configure(font=f["ui"])
        self.format_dropdown.configure(font=f["ui"], dropdown_font=f["ui"])
        self.level_dropdown.configure(font=f["ui"], dropdown_font=f["ui"])
        self.list_title.configure(font=f["ui"])
        self.btn_refresh.configure(font=f["ui"])
        self.btn_execute.configure(font=f["ui"])

        for chk in self.checkbox_refs:
            chk.configure(font=f["mono"])

    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        t = THEMES.get(theme_name, THEMES["Green"])

        self.app_title.configure(text_color=t["primary"])
        self.progress_bar.configure(progress_color=t["primary"])
        self.mode_selector.configure(selected_color=t["primary"], selected_hover_color=t["hover"])
        self.btn_execute.configure(fg_color=t["btn_bg"], hover_color=t["btn_hover"], text_color="#fff")
        self.chk_purge.configure(fg_color=t["primary"], hover_color=t["hover"])
        self.chk_hub.configure(fg_color=t["primary"], hover_color=t["hover"])
        self.chk_isolate.configure(fg_color=t["primary"], hover_color=t["hover"])

    def toggle_appearance(self):
        self.appearance_mode = "Light" if self.appearance_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(self.appearance_mode)
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
        self.checkbox_refs.clear()

        threading.Thread(target=self._scan_worker, daemon=True).start()

    def _scan_worker(self):
        try:
            all_items = os.listdir(self.working_dir)
        except Exception:
            all_items = []

        if self.mode == "EXTRACT":
            targets = [f for f in all_items if f.lower().endswith(ARCHIVE_FORMATS)]
        else:
            targets = [
                f for f in all_items 
                if f not in ("_EXTRACTED", "_COMPRESSED", "config.json", "app_icon.ico")
                and not f.startswith('.') 
                and not (os.path.isfile(os.path.join(self.working_dir, f)) and f.lower().endswith(ARCHIVE_FORMATS))
                and not f.endswith(('.py', '.pyw', '.exe', '.bat'))
            ]

        processed = []
        for item in targets:
            p = os.path.join(self.working_dir, item)
            size_mb = (os.path.getsize(p) if os.path.isfile(p) else sum(os.path.getsize(os.path.join(d, fl)) for d, _, fls in os.walk(p) for fl in fls)) / (1024 * 1024)
            is_dir = os.path.isdir(p)
            processed.append((item, size_mb, is_dir))

        self.after(0, lambda: self._render_scanned_items(processed))

    def _render_scanned_items(self, targets):
        if not targets:
            ctk.CTkLabel(self.scroll_area, text="No items found.", text_color="#64748b").pack(pady=25)
        else:
            t = THEMES.get(self.current_theme, THEMES["Green"])
            f = FONTS.get(self.current_font, FONTS["Segoe UI"])
            for item, size_mb, is_dir in targets:
                icon = "📁" if is_dir else "📄"
                var = ctk.BooleanVar(value=True)
                chk = ctk.CTkCheckBox(
                    self.scroll_area, 
                    text=f"{icon} {item:<40} [{size_mb:>7.2f} MB]", 
                    variable=var, 
                    font=f["mono"],
                    fg_color=t["primary"], 
                    hover_color=t["hover"]
                )
                chk.pack(anchor="w", padx=10, pady=4)
                self.file_vars[item] = var
                self.checkbox_refs.append(chk)

            self.log(f"Scanned {len(targets)} item(s) in {self.working_dir}")

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

                self.log(f"Done: {item}")
            except Exception as e:
                self.log(f"Error: {e}")

            self.progress_bar.set(idx / total)

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
