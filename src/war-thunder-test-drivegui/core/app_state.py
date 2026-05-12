from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
)
import os


def collect_app_state():
    """Collects current app state from the running GUI window, if available."""
    try:
        app = QApplication.instance()
        if not app:
            return "  App not initialised\n"
        # PyRight (Why not PyLeft) complaining on "topLevelWidgets"
        for widget in app.topLevelWidgets():  # pyright: ignore
            if isinstance(widget, QMainWindow):
                w = widget
                break
        else:
            return "  Window not found\n"

        lines = []
        mode = getattr(w, "mode_tabs", None)
        if mode and mode.currentIndex == 0:
            mode_name = "Ground"
        else:
            mode_name = "Naval"

        lines.append(f"  Mode:                {mode_name}")

        #  ━━━━━━━━━━ Ground state ━━━━━━━━━━
        lines.append("")
        lines.append("  [Ground]")
        vid = getattr(w, "Current_Vehicle_ID", None)
        lines.append(f"  Selected Vehicle:    {vid or 'Not set'}")

        wo_mode = getattr(w, "weapon_override_mode", "none")
        if wo_mode != "none":
            donor = (
                getattr(w, "weapon_override_donor_id", "")
                or getattr(w, "naval_weapon_override_donor_id", "")
                or getattr(w, "aircraft_weapon_override_donor_id", "")
            )
            weapon_blk = (
                getattr(w, "weapon_override_current_weapon_blk", "")
                or getattr(w, "naval_weapon_override_current_weapon_blk", "")
                or getattr(w, "aircraft_weapon_override_current_weapon_blk", "")
            )
            weapon_name = (
                weapon_blk.split("/")[-1].replace(".blk", "")
                if weapon_blk
                else "Not set"
            )
            lines.append(
                f"  Weapon Override:     {wo_mode} / {donor or 'Not set'} / {
                    weapon_name
                }"
            )
            vel_active = getattr(w, "velocity_override_active", False)
            cal_active = getattr(w, "caliber_override_active", False)
            lines.append(
                f"  Velocity Override:   {'Enabled' if vel_active else 'Disabled'}"
            )
            lines.append(
                f"  Caliber Override:    {'Enabled' if cal_active else 'Disabled'}"
            )
            wt_dir = getattr(w, "_wt_dir", None)
            if wt_dir and (vel_active or cal_active):
                big_path = os.path.join(
                    wt_dir,
                    "content",
                    "pkg_local",
                    "gameData",
                    "weapons",
                    "ask3lad",
                    "Ask3ladBigWeaponSir.blk",
                )
                lines.append(f"  BigWeaponSir.blk path: {big_path}")
                if os.path.exists(big_path):
                    try:
                        with open(big_path, encoding="utf-8") as _f:
                            lines.append("  BigWeaponSir.blk contents:")
                            for _line in _f.read().splitlines():
                                lines.append(f"    {_line}")
                    except Exception as _e:
                        lines.append(f"  (Could not read BigWeaponSir.blk: {_e})")
                else:
                    lines.append("  BigWeaponSir.blk: (not found)")
        else:
            lines.append("  Weapon Override:     None")

        lines.append(
            f"  Target 03:           {getattr(w, 'target03_id', None) or 'Not set'}"
        )
        lines.append(
            f"  Target 04:           {getattr(w, 'target04_id', None) or 'Not set'}"
        )
        lines.append(
            f"  Target 05:           {getattr(w, 'target05_id', None) or 'Not set'}"
        )
        lines.append(
            f"  Moving Target:       {getattr(w, 'target06_id', None) or 'Not set'}"
        )
        lines.append(
            f"  Naval Target:        {getattr(w, 'ship_target_id', None) or 'Not set'}"
        )
        lines.append(
            f"  Air 01 (5km):        {getattr(w, 'air01_id', None) or 'Not set'}"
        )
        lines.append(
            f"  Air 02 (2.5km):      {getattr(w, 'air02_id', None) or 'Not set'}"
        )
        lines.append(
            f"  Helicopter (2km):    {getattr(w, 'heli_id', None) or 'Not set'}"
        )

        #  ━━━━━━━━━━ Naval state ━━━━━━━━━━━
        lines.append("")
        lines.append("  [Naval]")
        lines.append(
            f"  You (Naval):         {
                getattr(w, 'current_naval_vehicle_id', None) or 'Not set'
            }"
        )
        lines.append(
            f"  Target 01:           {
                getattr(w, 'naval_target01_id', None) or 'Not set'
            }"
        )
        lines.append(
            f"  Target 02:           {
                getattr(w, 'naval_target02_id', None) or 'Not set'
            }"
        )
        lines.append(
            f"  Target 03:           {
                getattr(w, 'naval_target03_id', None) or 'Not set'
            }"
        )
        lines.append(
            f"  Target 04:           {
                getattr(w, 'naval_target04_id', None) or 'Not set'
            }"
        )
        lines.append(
            f"  Air 01:              {getattr(w, 'naval_air01_id', None) or 'Not set'}"
        )
        lines.append(
            f"  Air 02:              {getattr(w, 'naval_air02_id', None) or 'Not set'}"
        )

        return "\n".join(lines) + "\n"
    except Exception as e:
        return f"  (Could not collect state: {e})\n"
