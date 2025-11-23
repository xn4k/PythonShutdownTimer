# ⚡ Shutdown Timer (Windows, Python + CustomTkinter)

<img width="641" height="772" alt="image" src="https://github.com/user-attachments/assets/3bc26b3d-7545-4b3f-9d76-1ac512d1a339" />


A sleek desktop app that schedules a Windows shutdown in X minutes, displays a live countdown, and allows you to cancel it anytime.  
Built with [CustomTkinter].

---

## ⚙️ Features

- ⏱️ Countdown in HH:MM:SS format with a progress bar  
- 🌗 Switchable Light/Dark Mode  
- ⌨️ Press **Enter** to start immediately  
- 🛑 Cancel a scheduled shutdown with one click  
- 🔧 PyInstaller-friendly resource paths (`resource_path`)  
- 🪟 Uses native Windows commands (`shutdown /s /t` and `shutdown /a`)

---

## 🖥️ Preview

> Minimalist GUI with a minute input field, Start/Cancel buttons, status text, countdown timer, and progress bar.

---

## 📋 Requirements

- **OS:** Windows 10 or 11  
- **Python:** 3.9+ (3.11 recommended)  
- **Dependencies:**
  - `customtkinter`  
  - `tkinter` (included in standard Python installations on Windows)

---

## 🚀 Installation

```bash
# 1️⃣ Clone the repository
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO

# 2️⃣ (Optional) Create a virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3️⃣ Install dependencies
pip install customtkinter
```
▶️ Usage
```
python main.py
```

Enter the number of minutes until shutdown (e.g. 60).

Click Start to schedule the shutdown.

The countdown and progress bar will start running.

Click Cancel to abort the planned shutdown.

Keyboard shortcut:

Enter starts the timer.

💡 Note: Depending on your system policies, you may need to run the app as Administrator
to allow Windows to execute or cancel shutdown commands successfully.

🧱 Building an Executable (PyInstaller)

The script is fully prepared for PyInstaller (resource_path support).
To create a single-file executable:
```
pip install pyinstaller

pyinstaller ^
  --name "ShutdownTimer" ^
  --onefile ^
  --noconsole ^
  main.py

```
The built executable will be located in:

dist/ShutdownTimer.exe

🔨 Build Notes

If you add extra resources, include them with:

```
--add-data "path;."
```
If Windows Defender flags the EXE, sign it or exclude it manually
(false positives are common).

| Component               | Description                                                                |
| ----------------------- | -------------------------------------------------------------------------- |
| **GUI**                 | `customtkinter`                                                            |
| **Shutdown scheduling** | `subprocess.run(["shutdown", "/s", "/t", <seconds>], check=True)`          |
| **Shutdown abort**      | `subprocess.run(["shutdown", "/a"], check=True)`                           |
| **Countdown**           | Uses `after(1000, ...)` for 1-second updates                               |
| **Progress**            | 0.0–1.0 based on remaining time                                            |
| **State management**    | `remaining_seconds`, `total_seconds`, `countdown_running`, `countdown_job` |


🧩 Troubleshooting
“Could not schedule shutdown”

Run the app as Administrator.

Check Group Policies — shutdown may be restricted.

“No scheduled shutdown found” when canceling

No active timer or another process modified the shutdown schedule.

Countdown not updating

Verify after() isn’t called multiple times.
This code safely cancels old jobs before starting new ones.

⚠️ Safety & Responsibility

This app actually shuts down your computer — save your work first.

In corporate environments, admin policies may block shutdown commands.

🛠️ Roadmap

🔔 Optional notification before shutdown

☠️ “Force shutdown” checkbox (use with caution)

🌐 Multilanguage support (EN/DE via config)

📄 License

MIT License
See LICENSE
 for details.

👤 Author

Mikhail Zhivoderov
