import sys
import os
import datetime
from loguru import logger
import traceback
from .app_state import collect_app_state


APP_VERSION = "2.51"
_APP_VERSION_URL = (
    "https://raw.githubusercontent.com/ask3lad/wt-testdrive-db/main/app_version.json"
)


#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def write_crash_log(exc_type, exc_value, exc_tb):
    """Write a timestamped crash report to
    logs/app.log."""
    try:
        os.makedirs(_LOGS_DIR, exist_ok=True)

        # Prune old logs if over limit
        existing_logs = sorted(
            f
            for f in os.listdir(_LOGS_DIR)
            if f.startswith("crash_") and f.endswith(".txt")
        )
        while len(existing_logs) >= _MAX_CRASHES:
            os.remove(os.path.join(_LOGS_DIR, existing_logs.pop(0)))

        timestamp = datetime.datetime.now()
        crash_log = os.path.join(
            _LOGS_DIR, f"crash_{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        )

        tb_lines = traceback.format_exception(exc_type, exc_value, exc_tb)
        tb_str = "".join(tb_lines)
        state_str = collect_app_state()
        #  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        report = (
            f"{'=' * 60}\n"
            f"CRASH REPORT\n"
            f"Timestamp:  {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Version:    {APP_VERSION}\n"
            f"\n"
            f"--- Exception ---\n"
            f"Type:       {exc_type.__name__}\n"
            f"Message:    {exc_value}\n"
            f"\n"
            f"--- Traceback ---\n"
            f"{tb_str}\n"
            f"--- App State ---\n"
            f"{state_str}"
        )

        logger.add(sink="logs/app.log")
        logger.error(report)

        return crash_log
    except Exception:
        return None  # Never let the crash logger itself crash


def crash_handler(exc_type, exc_value, exc_tb):
    """Global unhandled exception hook — log then show a dialog."""
    crash_log = write_crash_log(exc_type, exc_value, exc_tb)
    try:
        from PyQt6.QtWidgets import QMessageBox

        msg = QMessageBox()
        msg.setWindowTitle("Unexpected Error")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(
            f"The application encountered an unexpected error and needs to close.\n\n"
            f"A crash report has been saved to:\n{crash_log or _LOGS_DIR}\n\n"
            f"Please send this file to Ask3lad so the issue can be fixed."
        )
        msg.exec()
    except Exception:
        pass
    sys.__excepthook__(exc_type, exc_value, exc_tb)


# When running as a PyInstaller exe, __file__ points to the temp extraction
# directory, not the exe's real location. Use sys.executable instead.
if getattr(sys, "frozen", False):
    _APP_DIR = os.path.dirname(sys.executable)
else:
    _APP_DIR = os.path.dirname(os.path.abspath(__file__))

_LOGS_DIR = os.path.join(_APP_DIR, "Logs")
_MAX_CRASHES = 10
