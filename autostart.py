import os
import sys
import winreg

_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
_NAME = "BatteryTray"


def _command() -> str:
    if getattr(sys, "frozen", False):
        return f'"{sys.executable}"'
    pyw = sys.executable
    if pyw.lower().endswith("python.exe"):
        candidate = pyw[:-len("python.exe")] + "pythonw.exe"
        if os.path.exists(candidate):
            pyw = candidate
    script = os.path.abspath(sys.argv[0])
    return f'"{pyw}" "{script}"'


def is_enabled() -> bool:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _KEY) as k:
            winreg.QueryValueEx(k, _NAME)
            return True
    except FileNotFoundError:
        return False


def set_enabled(enable: bool) -> None:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _KEY, 0,
                        winreg.KEY_SET_VALUE) as k:
        if enable:
            winreg.SetValueEx(k, _NAME, 0, winreg.REG_SZ, _command())
        else:
            try:
                winreg.DeleteValue(k, _NAME)
            except FileNotFoundError:
                pass
