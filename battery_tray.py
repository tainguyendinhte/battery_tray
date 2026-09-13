import ctypes
import sys
import threading

import psutil
import pystray

import autostart
from icon_renderer import render

REFRESH_SEC = 1
MUTEX_NAME = "Global\\BatteryTrayApp_A7F3"
ERROR_ALREADY_EXISTS = 183


def ensure_single_instance() -> None:
    kernel32 = ctypes.windll.kernel32
    kernel32.CreateMutexW(None, False, MUTEX_NAME)
    if kernel32.GetLastError() == ERROR_ALREADY_EXISTS:
        sys.exit(0)


def read_battery():
    b = psutil.sensors_battery()
    if b is None:
        return False, 0, False
    return True, int(round(b.percent)), bool(b.power_plugged)


def build_menu():
    def toggle_autostart(_icon, item):
        autostart.set_enabled(not item.checked)

    return pystray.Menu(
        pystray.MenuItem(
            "Start with Windows",
            toggle_autostart,
            checked=lambda _: autostart.is_enabled(),
        ),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Exit", lambda ic, _: ic.stop()),
    )


def refresh_loop(icon: pystray.Icon, stop: threading.Event) -> None:
    while not stop.is_set():
        has_bat, pct, charging = read_battery()
        icon.icon = render(pct, charging, has_bat)
        icon.title = (
            f"Battery: {pct}%" + (" (charging)" if charging else "")
            if has_bat else "No battery detected"
        )
        stop.wait(REFRESH_SEC)


def main() -> None:
    ensure_single_instance()

    has_bat, pct, charging = read_battery()
    icon = pystray.Icon(
        "BatteryTray",
        icon=render(pct, charging, has_bat),
        title="Battery",
        menu=build_menu(),
    )

    stop = threading.Event()
    worker = threading.Thread(
        target=refresh_loop, args=(icon, stop), daemon=True
    )

    def on_ready(ic: pystray.Icon) -> None:
        ic.visible = True
        worker.start()

    try:
        icon.run(setup=on_ready)
    finally:
        stop.set()


if __name__ == "__main__":
    main()
