# ArchiveSuite

A modern, high-performance archive manager and batch compression suite built with Python and CustomTkinter. Designed to handle extraction and packing workflows with zero clutter and blazing-fast disk indexing.

---

## Features

- **Dual-Engine Pipeline:** Seamlessly extract archives (`.zip`, `.7z`, `.rar`) or batch-compress raw files and folders directly.
- **Ultra-Fast Sizing Engine:** Multi-threaded non-blocking directory scanner with Windows junction/symlink loop protection.
- **Auto-Purge & Payload Hubs:** Option to automatically delete source files post-processing or route outputs to clean dedicated payload directories.
- **Modern Minimalist UI:** Sleek card row layout with pill size badges, live color palette switching, and typography font profiles.
- **In-App Hot Updater:** Inspect and inject live code updates directly from within the application interface.
- **Desktop Link & Icon Generator:** 1-click desktop shortcut builder and automated image-to-ICO icon converter.
- **Dependency Self-Healer:** Automatically detects missing packages on startup with automated 1-click installer.

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/raed-alzahrani/ArchiveSuite.git](https://github.com/raed-alzahrani/ArchiveSuite.git)
   cd ArchiveSuite
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.pyw
   ```
   *(On Windows, double-click `main.pyw` directly without opening a terminal window).*

> **Note:** For handling `.7z` and `.rar` archives, ensure [7-Zip](https://www.7-zip.org/) is installed on your system.

---

## Requirements

- Python 3.8+
- `customtkinter >= 5.2.0`
- `pillow >= 10.0.0`
- `py7zr >= 0.20.0`

---

## License

This project is licensed under the [MIT License](LICENSE).