"""Colored terminal output."""

RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[31m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"

PREFIX_OK = f"[{GREEN}*{RESET}] "
PREFIX_ERR = f"[{RED}!{RESET}] "
PREFIX_WARN = f"[{YELLOW}*{RESET}] "
PREFIX_INFO = f"[{CYAN}>{RESET}] "


def ok(msg):
    print(f"{PREFIX_OK}{msg}")


def err(msg):
    print(f"{PREFIX_ERR}{msg}")


def warn(msg):
    print(f"{PREFIX_WARN}{msg}")


def info(msg):
    print(f"{PREFIX_INFO}{msg}")


def verbose(msg, enabled):
    """Print only when verbose mode is on."""
    if enabled:
        print(f"{PREFIX_INFO}{msg}")
