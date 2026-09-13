# BatteryTrayPy

App tray Windows 10/11 hiển thị phần trăm pin, refresh mỗi 1 giây. Viết bằng Python.

## Cài đặt

```powershell
cd d:\IPAGEON\BatteryTrayPy
pip install -r requirements.txt
```

## Chạy

```powershell
pythonw battery_tray.py
```

Dùng `pythonw.exe` (không phải `python.exe`) để không hiện cửa sổ console nền.

## Tính năng

- Vẽ số % pin lên icon tray 32x32, refresh mỗi 1 giây
- Màu: trắng (bình thường), xanh (đang sạc), đỏ cam (≤20%), xám (không có pin)
- Right-click tray:
  - `Start with Windows` — auto-start qua `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
  - `Exit`
- Single-instance mutex
- Không cần quyền admin

## Đóng gói thành .exe standalone

Chạy trên máy có Python + đã `pip install -r requirements.txt`:

```
build_exe.bat
```

(Double-click file `build_exe.bat` cũng được. Hoặc dùng bản PowerShell: `.\build_exe.ps1`.)

Hoặc gọi trực tiếp:

```powershell
pip install pyinstaller
python -m PyInstaller --noconsole --onefile --name BatteryTray `
    --hidden-import PIL._tkinter_finder `
    --collect-submodules pystray `
    --collect-submodules PIL `
    battery_tray.py
```

File exe: `dist\BatteryTray.exe` (~12–15 MB), chạy được trên máy không cài Python.

**Flags giải thích:**
- `--noconsole` → không hiện cửa sổ CMD đen khi chạy
- `--onefile` → gộp mọi thứ vào 1 file duy nhất (chậm start ~1s do phải giải nén tạm)
- `--collect-submodules pystray` → pystray load backend Windows động qua importlib, PyInstaller không tự phát hiện được nên phải khai báo tay. Không có flag này exe sẽ crash khi khởi động.

## Ghi chú auto-start

- Khi chạy dạng script `.py`: registry lưu `"C:\...\pythonw.exe" "d:\...\battery_tray.py"`. Di chuyển file thì tắt/bật lại menu để cập nhật đường dẫn.
- Khi chạy `.exe` đã build: registry lưu thẳng `"C:\...\BatteryTray.exe"`. Di chuyển exe cũng cần tắt/bật lại.
