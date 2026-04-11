"""

CLI entry point and argument parser for Sentinel & Sage

"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

from sent_sage import __version__
from sent_sage.config import Config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sent-sage",
        description="Dual-agent CLI Security Suite for threat analysis and pentesting."
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "-c", "--config",
        type=Path,
        default=None,
        help="Path to a custom TOML config file (default: config/default.toml)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable debug mode (verbose logging)",
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("ui", help="Launch the TUI.")
    subparsers.add_parser("run", help="Run in CLI mode.")

    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        config = Config.load(config_path=args.config)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error, invalid configuration: {e}", file=sys.stderr)
        sys.exit(1)

    if args.debug:
        config.app.debug = True

    if args.command == "ui":
        from sent_sage.ui.app import SentSageApp
        SentSageApp().run()
    elif args.command == "run":
        ...
    else:
        parser.print_help()

    # To be replaced once TUI is designed, simply here to test!
    print(f"Sentinel & Sage v{__version__}")
    print(f"Config file loaded: model={config.model.primary}, budget=${config.budget.max_per_run_usd}")
    print(f"Debug: {config.app.debug}")
    print(f"TUI launch point; app.py not written!")

