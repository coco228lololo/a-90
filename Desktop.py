import os
import json
import stat
import ctypes
import shutil
import configparser
import comtypes
import comtypes.client
from pathlib import Path

# ---------- Повышение прав (UAC) ----------

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", ctypes.create_unicode_buffer(__file__), None, None, 1
        )
        raise SystemExit(0)

run_as_admin()


# ---------- Константы ----------

DESKTOPS = [
    str(Path.home() / "Desktop"),
    r"C:\Users\Public\Desktop",
]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(SCRIPT_DIR, "red_hand.ico")
WALLPAPER_PATH = os.path.join(SCRIPT_DIR, "desktop.jpg")  # ← добавлено
NEW_NAME_PREFIX = "ENCRYPTED"
BACKUP_FILE = os.path.join(str(Path.home() / "Desktop"), "icons_backup.json")

# Windows API константы для обоев
SPI_GETDESKWALLPAPER = 0x0073
SPI_SETDESKWALLPAPER = 0x0014
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02


# ---------- Обои ----------

def get_wallpaper():
    """Возвращает путь к текущим обоям рабочего стола."""
    buf = ctypes.create_unicode_buffer(260)
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_GETDESKWALLPAPER, 260, buf, 0
    )
    return buf.value


def set_wallpaper(path):
    """Устанавливает обои рабочего стола."""
    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    )
    if not result:
        raise ctypes.WinError(ctypes.windll.kernel32.GetLastError())


# ---------- Ярлыки ----------

def get_all_shortcuts():
    result = []
    for desk in DESKTOPS:
        if not os.path.isdir(desk):
            continue
        for f in os.listdir(desk):
            if f.lower().endswith((".lnk", ".url")):
                result.append(os.path.join(desk, f))
    return result


def make_writable(path):
    try:
        attrs = os.stat(path).st_mode
        os.chmod(path, attrs | stat.S_IWRITE)
    except OSError:
        pass
    try:
        FILE_ATTRIBUTE_READONLY = 0x1
        FILE_ATTRIBUTE_HIDDEN = 0x2
        FILE_ATTRIBUTE_SYSTEM = 0x4
        current = ctypes.windll.kernel32.GetFileAttributesW(path)
        if current != 0xFFFFFFFF:
            new_attrs = current & ~(FILE_ATTRIBUTE_READONLY | FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM)
            ctypes.windll.kernel32.SetFileAttributesW(path, new_attrs)
    except Exception:
        pass


def parse_icon_index(icon_loc):
    if not icon_loc or "," not in icon_loc:
        return "0"
    parts = icon_loc.rsplit(",", 1)
    idx = parts[1].strip()
    return idx if idx else "0"


# ---------- .lnk ----------

def read_icon_lnk(lnk_path):
    comtypes.CoInitialize()
    shell = comtypes.client.CreateObject("WScript.Shell", dynamic=True)
    shortcut = shell.CreateShortcut(lnk_path)
    return shortcut.IconLocation


def set_icon_lnk(lnk_path, new_icon, icon_index="0"):
    comtypes.CoInitialize()
    make_writable(lnk_path)
    shell = comtypes.client.CreateObject("WScript.Shell", dynamic=True)
    icon_loc = f"{new_icon},{icon_index}"
    try:
        shortcut = shell.CreateShortcut(lnk_path)
        shortcut.IconLocation = icon_loc
        shortcut.Save()
        return
    except Exception:
        pass
    tmp_path = lnk_path + ".tmp_lnk"
    try:
        if os.path.exists(tmp_path):
            make_writable(tmp_path)
            os.remove(tmp_path)
        shutil.copy2(lnk_path, tmp_path)
        make_writable(tmp_path)
        shortcut = shell.CreateShortcut(tmp_path)
        shortcut.IconLocation = icon_loc
        shortcut.Save()
        make_writable(lnk_path)
        os.replace(tmp_path, lnk_path)
    except Exception:
        if os.path.exists(tmp_path):
            try:
                make_writable(tmp_path)
                os.remove(tmp_path)
            except Exception:
                pass
        raise


# ---------- .url ----------

def read_icon_url(url_path):
    comtypes.CoInitialize()
    config = configparser.ConfigParser()
    config.read(url_path, encoding="utf-8")
    if "InternetShortcut" in config and "IconFile" in config["InternetShortcut"]:
        icon_file = config["InternetShortcut"]["IconFile"]
        icon_index = config["InternetShortcut"].get("IconIndex", "0")
        return f"{icon_file},{icon_index}"
    return ""


def set_icon_url(url_path, new_icon, icon_index="0"):
    comtypes.CoInitialize()
    make_writable(url_path)
    config = configparser.ConfigParser()
    config.read(url_path, encoding="utf-8")
    if "InternetShortcut" not in config:
        config["InternetShortcut"] = {}
    config["InternetShortcut"]["IconFile"] = new_icon
    config["InternetShortcut"]["IconIndex"] = icon_index
    try:
        with open(url_path, "w", encoding="utf-8") as f:
            config.write(f, space_around_delimiters=False)
    except PermissionError:
        tmp_path = url_path + ".tmp_url"
        with open(tmp_path, "w", encoding="utf-8") as f:
            config.write(f, space_around_delimiters=False)
        make_writable(url_path)
        os.replace(tmp_path, url_path)


# ---------- Универсальные обёртки ----------

def read_icon(path):
    if path.lower().endswith(".lnk"):
        return read_icon_lnk(path)
    else:
        return read_icon_url(path)


def set_icon(path, new_icon, icon_index="0"):
    if path.lower().endswith(".lnk"):
        set_icon_lnk(path, new_icon, icon_index)
    else:
        set_icon_url(path, new_icon, icon_index)


# ---------- Смена имени ----------

def rename_shortcut(old_path, new_name):
    make_writable(old_path)
    ext = os.path.splitext(old_path)[1]
    desk_dir = os.path.dirname(old_path)
    new_path = os.path.join(desk_dir, new_name + ext)
    if os.path.normpath(old_path) == os.path.normpath(new_path):
        return old_path
    while os.path.exists(new_path):
        new_path = os.path.join(desk_dir, f"{new_name}_{ext}")
    os.rename(old_path, new_path)
    return new_path


# ---------- Основные функции ----------

def backup_icons():
    data = {}
    for path in get_all_shortcuts():
        name = os.path.basename(path)
        try:
            data[path] = {
                "icon": read_icon(path),
                "name": name,
            }
        except Exception as e:
            print(f"  пропущен {name}: {e}")

    # Сохраняем текущие обои  # ← добавлено
    data["__wallpaper__"] = get_wallpaper()

    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Сохранено {len(data) - 1} ярлыков в {BACKUP_FILE}")  # -1 потому что __wallpaper__ не ярлык


def apply_new_icon():
    if not os.path.exists(ICON_PATH):
        print(f"Файл иконки не найден: {ICON_PATH}")
        return
    if not os.path.exists(BACKUP_FILE):
        print("Сначала запустите backup_icons()!")
        return

    with open(BACKUP_FILE, "r", encoding="utf-8") as f:
        backup = json.load(f)

    ok, fail = 0, 0
    counter = 0
    for path in get_all_shortcuts():
        name = os.path.basename(path)
        try:
            original_icon = backup.get(path, {}).get("icon", "")
            original_index = parse_icon_index(original_icon)

            set_icon(path, ICON_PATH, original_index)
            counter += 1
            ok_count = ok + 1
            new_base = f"{NEW_NAME_PREFIX}_{counter}{ok_count}"
            new_path = rename_shortcut(path, new_base)

            if path in backup:
                backup[path]["new_path"] = new_path
            else:
                backup[path] = {
                    "icon": ICON_PATH,
                    "name": name,
                    "new_path": new_path,
                }

            ok += 1
        except Exception as e:
            print(f"  ошибка {name}: {e}")
            fail += 1

    # Меняем обои  # ← добавлено
    if os.path.exists(WALLPAPER_PATH):
        try:
            set_wallpaper(WALLPAPER_PATH)
            print(f"Обои изменены на: {WALLPAPER_PATH}")
        except Exception as e:
            print(f"  ошибка при смене обоев: {e}")
    else:
        print(f"Файл обоев не найден: {WALLPAPER_PATH}")

    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(backup, f, ensure_ascii=False, indent=2)
    print(f"Изменено {ok} ярлыков, ошибок: {fail}")


def restore_icons():
    if not os.path.exists(BACKUP_FILE):
        print("Файл бэкапа не найден.")
        return
    with open(BACKUP_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    ok, fail = 0, 0
    for old_path, info in data.items():
        if old_path == "__wallpaper__":  # ← пропускаем, обои восстанавливаем отдельно
            continue
        current_path = info.get("new_path", old_path)
        if not os.path.exists(current_path):
            current_path = old_path
        if not os.path.exists(current_path):
            print(f"  файл не найден: {os.path.basename(old_path)}")
            fail += 1
            continue
        try:
            icon_loc = info["icon"]
            if icon_loc:
                icon_path_part, icon_idx = (
                    icon_loc.rsplit(",", 1) if "," in icon_loc else (icon_loc, "0")
                )
                set_icon(current_path, icon_path_part, icon_idx)
            elif current_path.lower().endswith(".url"):
                make_writable(current_path)
                config = configparser.ConfigParser()
                config.read(current_path, encoding="utf-8")
                if "InternetShortcut" in config:
                    config.remove_option("InternetShortcut", "IconFile")
                    config.remove_option("InternetShortcut", "IconIndex")
                    try:
                        with open(current_path, "w", encoding="utf-8") as f:
                            config.write(f, space_around_delimiters=False)
                    except PermissionError:
                        tmp = current_path + ".tmp_url"
                        with open(tmp, "w", encoding="utf-8") as f:
                            config.write(f, space_around_delimiters=False)
                        make_writable(current_path)
                        os.replace(tmp, current_path)

            original_name = info["name"]
            rename_shortcut(current_path, os.path.splitext(original_name)[0])
            ok += 1
        except Exception as e:
            print(f"  ошибка {os.path.basename(current_path)}: {e}")
            fail += 1

    # Восстанавливаем обои  # ← добавлено
    saved_wallpaper = data.get("__wallpaper__", "")
    if saved_wallpaper:
        try:
            set_wallpaper(saved_wallpaper)
            print(f"Обои восстановлены: {saved_wallpaper}")
        except Exception as e:
            print(f"  ошибка при восстановлении обоев: {e}")

    print(f"Восстановлено {ok} ярлыков, ошибок: {fail}")


def EnabledIcons(b: bool):
    if b:
        backup_icons()
        apply_new_icon()
    elif not b:
        restore_icons()