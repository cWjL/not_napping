"""OS detection, WSL blocking, and platform constants."""

import sys
from platform import uname

SYSTEM = uname().system.lower()
RELEASE = uname().release.lower()

IS_LINUX = "linux" in SYSTEM
IS_MACOS = "darwin" in SYSTEM
IS_WINDOWS = "windows" in SYSTEM
IS_WSL = IS_LINUX and "microsoft" in RELEASE


def get_modifier_key():
    """Return the platform modifier key name for pyautogui."""
    if IS_MACOS:
        return "command"
    return "alt"


def check_platform():
    """Block execution under WSL; enable ANSI colors on Windows."""
    if IS_WSL:
        print("[X] ERROR: This script cannot be run from within WSL")
        sys.exit(1)

    if not (IS_LINUX or IS_MACOS or IS_WINDOWS):
        print(f"[X] ERROR: Unsupported platform: {uname().system}")
        sys.exit(1)

    if IS_WINDOWS:
        import os
        os.system("color")
