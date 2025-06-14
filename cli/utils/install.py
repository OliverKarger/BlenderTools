import os
import sys
import winreg

from .. import bt_logger

logger = bt_logger.get_logger(__name__)

APPDATA = os.environ["APPDATA"]
SHORTCUT_NAME = "blender-cli.cmd"
TARGET_DIR = os.path.expanduser(r"~\bin")

WRAPPER_SCRIPT = os.path.join(
    APPDATA, "Blender Foundation", "Blender", "4.3", "scripts", "addons", "blendertools", "cli", "wrapper.cmd"
)


def __add_to_user_path(folder):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
        try:
            current_path, _ = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current_path = ""

        paths = current_path.split(";") if current_path else []
        if folder not in paths:
            new_path = current_path + ";" + folder if current_path else folder
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
            logger.info(f"Added to PATH: {folder}")
            logger.info("You may need to restart your terminal or sign out/in for changes to take effect.")
        else:
            logger.info(f"'{folder}' is already in PATH.")


def install_wrapper():
    if not os.path.exists(WRAPPER_SCRIPT):
        print(f"Could not find Wrapper Script {WRAPPER_SCRIPT}")
        exit

    os.makedirs(TARGET_DIR, exist_ok=True)

    shortcut_path = os.path.join(TARGET_DIR, SHORTCUT_NAME)

    with open(shortcut_path, "w") as f:
        f.write(f'@echo off\n"{WRAPPER_SCRIPT}" %*\n')

    logger.info(f"Installed to {shortcut_path}")

    if TARGET_DIR not in sys.path:
        __add_to_user_path(TARGET_DIR)
        logger.info(f"Added {TARGET_DIR} to PATH")


def uninstall_wrapper():
    shortcut_path = os.path.join(TARGET_DIR, SHORTCUT_NAME)

    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
        logger.info(f"Removed {shortcut_path}")
