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
    """
    Adds a specified folder to the user's PATH environment variable.

    This function modifies the PATH environment variable for the current user
    by appending the provided folder. If the folder already exists in the PATH,
    it will not be added. Additionally, it logs information about whether the
    folder was added or was already present. The change requires a terminal
    restart or user sign-out/in for it to take effect.

    Parameters:
        folder (str): The folder path to be added to the user's PATH environment variable.

    Raises:
        FileNotFoundError: If the "Path" registry key is not found during the query.
    """
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
    """
    Creates and installs a wrapper script as a shortcut in the target directory.
    This function checks the existence of the wrapper script, creates the target directory
    if it does not exist, then creates a shortcut file with the wrapper script as its content.
    Additionally, it ensures the target directory is included in the system PATH.

    Args:
        None

    Raises:
        None

    Returns:
        None
    """
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
    """
    Removes a shortcut file from the target directory if it exists.

    This function checks for the existence of a specific shortcut file in the
    target directory. If the shortcut file is found, it is deleted, and the
    operation is logged. This function is intended for cleanup purposes to
    remove leftover or unnecessary shortcut files.

    Raises:
        FileNotFoundError: Raised by os.remove if the file cannot be found
        during the deletion attempt. This is unlikely due to the pre-check
        with os.path.exists.

    """
    shortcut_path = os.path.join(TARGET_DIR, SHORTCUT_NAME)

    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
        logger.info(f"Removed {shortcut_path}")
