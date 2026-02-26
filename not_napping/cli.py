"""CLI argument parsing, startup, and Ctrl+C handling."""

import argparse
import sys

from . import __version__
from .platform_check import check_platform
from . import output
from .scheduler import Scheduler


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="not-napping",
        description="Simulate realistic user activity to appear active.",
    )
    parser.add_argument(
        "-d", "--max-delay",
        type=int,
        required=True,
        metavar="SECONDS",
        dest="max_delay",
        help="Maximum seconds between activity bursts",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="Print each action as it happens",
    )
    parser.add_argument(
        "--no-mouse",
        action="store_true",
        default=False,
        help="Disable mouse movement",
    )
    parser.add_argument(
        "--no-typing",
        action="store_true",
        default=False,
        help="Disable typing simulation",
    )
    parser.add_argument(
        "--no-switching",
        action="store_true",
        default=False,
        help="Disable app switching",
    )
    parser.add_argument(
        "--no-scrolling",
        action="store_true",
        default=False,
        help="Disable scrolling",
    )
    parser.add_argument(
        "--no-files",
        action="store_true",
        default=False,
        help="Disable file access simulation",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def _build_behaviors(args):
    """Import and instantiate only the enabled behaviors."""
    behaviors = []

    if not args.no_mouse:
        from .behaviors.mouse import MouseBehavior
        behaviors.append(MouseBehavior())

    if not args.no_typing:
        from .behaviors.typing import TypingBehavior
        behaviors.append(TypingBehavior())

    if not args.no_scrolling:
        from .behaviors.scroll import ScrollBehavior
        behaviors.append(ScrollBehavior())

    if not args.no_switching:
        from .behaviors.app_switch import AppSwitchBehavior
        behaviors.append(AppSwitchBehavior())

    if not args.no_files:
        from .behaviors.file_access import FileAccessBehavior
        behaviors.append(FileAccessBehavior())

    return behaviors


def main():
    check_platform()

    parser = _build_parser()
    args = parser.parse_args()

    if args.max_delay <= 0:
        output.err("Max delay must be a positive integer.")
        sys.exit(1)

    behaviors = _build_behaviors(args)
    if not behaviors:
        output.err("All behaviors disabled. Enable at least one.")
        sys.exit(1)

    names = ", ".join(b.name for b in behaviors)
    output.ok(f"Behaviors: {names}")
    output.ok(f"Max delay: {args.max_delay}s")

    scheduler = Scheduler(behaviors, args.max_delay, verbose=args.verbose)

    try:
        scheduler.run()
    except KeyboardInterrupt:
        scheduler.stop()
        output.warn("Stopped. Goodbye!")
        sys.exit(0)
