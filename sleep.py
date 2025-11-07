import os
import sys
import subprocess
import customtkinter as ctk


# --- Windows shutdown helpers ---
def schedule_shutdown(seconds: int) -> bool:
    try:
        subprocess.run(["shutdown", "/s", "/t", str(seconds)], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def abort_shutdown() -> bool:
    try:
        subprocess.run(["shutdown", "/a"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


# --- Hilfsfunktion für Ressourcenpfade (PyInstaller) ---
def resource_path(rel_path: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel_path)


class ShutdownTimerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Shutdown Timer")
        self.geometry("480x360")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")

        # State
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.countdown_running = False
        self.countdown_job = None  # after()-Job-ID

        # ===== Header =====
        header = ctk.CTkFrame(self)
        header.pack(padx=12, pady=(12, 6), fill="x")

        title_label = ctk.CTkLabel(
            header, text="Windows Shutdown Timer", font=("Segoe UI", 18, "bold")
        )
        title_label.grid(row=0, column=0, sticky="w")

        current_dark = ctk.get_appearance_mode().lower() == "dark"
        self.dark_var = ctk.BooleanVar(value=current_dark)
        self.theme_switch = ctk.CTkSwitch(
            header,
            text="Dark Mode" if current_dark else "Light Mode",
            variable=self.dark_var,
            command=self.on_toggle_theme,
        )
        self.theme_switch.grid(row=0, column=1, sticky="e")
        header.grid_columnconfigure(0, weight=1)

        # ===== Input row =====
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=6, padx=12, fill="x")

        minutes_label = ctk.CTkLabel(self.input_frame, text="Minuten bis Shutdown:")
        minutes_label.grid(row=0, column=0, padx=(12, 8), pady=12, sticky="w")

        self.minutes_entry = ctk.CTkEntry(self.input_frame, placeholder_text="z. B. 60")
        self.minutes_entry.grid(row=0, column=1, padx=(0, 12), pady=12, sticky="we")
        self.input_frame.grid_columnconfigure(1, weight=1)

        # ===== Buttons =====
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(pady=4, padx=12, fill="x")

        self.start_button = ctk.CTkButton(buttons_frame, text="Start", command=self.on_start)
        self.start_button.grid(row=0, column=0, padx=8, pady=8, sticky="we")

        self.abort_button = ctk.CTkButton(
            buttons_frame, text="Abbrechen", fg_color="gray", command=self.on_abort
        )
        self.abort_button.grid(row=0, column=1, padx=8, pady=8, sticky="we")

        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)

        # ===== Status & Countdown =====
        self.status_label = ctk.CTkLabel(self, text="Kein Shutdown geplant.", wraplength=420)
        self.status_label.pack(pady=(10, 0))

        self.countdown_label = ctk.CTkLabel(self, text="", font=("Consolas", 18))
        self.countdown_label.pack(pady=(6, 12))

        # Progressbar im Container (sauberes Layout)
        self.progress_container = ctk.CTkFrame(self)
        self.progress_container.pack(pady=(4, 8), padx=40, fill="x")
        self.progress = ctk.CTkProgressBar(self.progress_container, mode="determinate")
        self.progress.pack(fill="x")
        self.progress.set(0.0)

        # ===== Footer =====
        hint_label = ctk.CTkLabel(
            self,
            text="Hinweis: Bei Berechtigungsproblemen als Administrator starten.",
            font=("Segoe UI", 10),
        )
        hint_label.pack(pady=(0, 8))

        # Enter startet
        self.bind("<Return>", lambda _e: self.on_start())

    # ===== Theme Toggle =====
    def on_toggle_theme(self):
        new_mode = "dark" if self.dark_var.get() else "light"
        ctk.set_appearance_mode(new_mode)
        self.theme_switch.configure(text="Dark Mode" if new_mode == "dark" else "Light Mode")

    # ===== App-Logik =====
    def on_start(self):
        if self.countdown_running:
            return

        minutes_str = self.minutes_entry.get().strip()
        try:
            minutes = int(minutes_str)
        except ValueError:
            self.status_label.configure(text="Bitte eine ganze Zahl in Minuten eingeben.")
            return

        if minutes < 1:
            self.status_label.configure(text="Mindestens 1 Minute, sonst wird das sinnlos hektisch.")
            return

        seconds = minutes * 60
        if not schedule_shutdown(seconds):
            self.status_label.configure(text="Konnte Shutdown nicht planen. Starte die App ggf. als Administrator.")
            return

        # State setzen
        self.total_seconds = seconds
        self.remaining_seconds = seconds
        self.countdown_running = True

        # UI sperren
        self.start_button.configure(state="disabled")
        self.minutes_entry.configure(state="disabled")
        self.status_label.configure(text=f"Shutdown geplant in {minutes} Minute(n).")

        # Progress zurücksetzen
        self.progress.set(0.0)

        # Falls ein alter Timer rumhing, killen
        if self.countdown_job is not None:
            try:
                self.after_cancel(self.countdown_job)
            except Exception:
                pass
            self.countdown_job = None

        self.update_countdown()  # erster Tick

    def on_abort(self):
        aborted = abort_shutdown()
        if aborted:
            self.status_label.configure(text="Geplanter Shutdown abgebrochen.")
        else:
            self.status_label.configure(text="Kein geplanter Shutdown gefunden oder Abbruch fehlgeschlagen.")

        self._reset_ui()

    def update_countdown(self):
        if not self.countdown_running:
            return

        m, s = divmod(self.remaining_seconds, 60)
        h, m = divmod(m, 60)
        self.countdown_label.configure(text=f"{h:02d}:{m:02d}:{s:02d}")

        # Fortschritt 0.0–1.0
        if self.total_seconds > 0:
            progress_value = 1.0 - (self.remaining_seconds / self.total_seconds)
            progress_value = max(0.0, min(1.0, progress_value))
            self.progress.set(progress_value)

        if self.remaining_seconds <= 0:
            # kein after mehr, UI freigeben und Progress final voll
            self.progress.set(1.0)
            self.status_label.configure(text="Shutdown steht unmittelbar bevor.")
            self.countdown_running = False
            self.start_button.configure(state="normal")
            self.minutes_entry.configure(state="normal")
            return

        self.remaining_seconds -= 1
        self.countdown_job = self.after(1000, self.update_countdown)

    # ===== Helpers =====
    def _reset_ui(self):
        self.countdown_running = False
        if self.countdown_job is not None:
            try:
                self.after_cancel(self.countdown_job)
            except Exception:
                pass
            self.countdown_job = None

        self.countdown_label.configure(text="")
        self.start_button.configure(state="normal")
        self.minutes_entry.configure(state="normal")
        self.progress.set(0.0)


if __name__ == "__main__":
    app = ShutdownTimerApp()
    app.mainloop()
