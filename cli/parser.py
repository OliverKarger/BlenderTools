import argparse
import importlib.util
import pathlib
import sys

from . import bt_logger

logger = bt_logger.get_logger(__name__)

BASE_COMMANDS_DIR = pathlib.Path(__file__).parent / "commands"


def import_command_module(path: pathlib.Path):
    """Import a module from a given file path."""
    spec = importlib.util.spec_from_file_location(name=path.stem, location=str(path))
    if spec is None or spec.loader is None:
        logger.error(f"Cannot import module from {path}")
        sys.exit(1)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    logger.debug(f"Imported Module {path}")
    return module


def ensure_module_attributes(module, path, required_attrs):
    """Ensure a module has all required attributes, or exit."""
    for attr in required_attrs:
        if not hasattr(module, attr):
            logger.warning(f"'{path}' is missing required attribute: {attr}")
            sys.exit(1)


def parse():
    # Global flags
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    global_parser.add_argument("-oe", "--on-exit", type=str, help="Action to perform on exit")
    global_parser.add_argument("-dr", "--dry-run", help="Dry Run", default=False, action="store_true")

    # Root CLI parser
    parser = argparse.ArgumentParser(
        prog="BlenderTools CLI", description="Command Line Interface Tools", parents=[global_parser]
    )

    main_subparsers = parser.add_subparsers(dest="group", required=True)

    for group_dir in BASE_COMMANDS_DIR.iterdir():
        if not group_dir.is_dir() or group_dir.name.startswith("__"):
            continue

        group_name = group_dir.name
        main_command_file = group_dir / "main.py"

        if main_command_file.exists():
            # Handle single-command group (e.g., wf)
            module = import_command_module(main_command_file)
            ensure_module_attributes(module, main_command_file, ["COMMAND_NAME", "HELP", "setup"])

            group_parser = main_subparsers.add_parser(group_name, help=module.HELP, parents=[global_parser])
            module.setup(group_parser)

            handler = getattr(module, "handle", None)
            if not callable(handler):
                logger.error(f"'{main_command_file}' must define a callable 'handle(args)' function")
                sys.exit(1)

            group_parser.set_defaults(handler=handler)

        else:
            # Handle multi-command group (e.g., render/single.py, render/batch.py)
            group_parser = main_subparsers.add_parser(
                group_name, help=f"{group_name} commands", parents=[global_parser]
            )
            group_subparsers = group_parser.add_subparsers(dest="command", required=True)

            for file in group_dir.glob("*.py"):
                if file.name == "__init__.py":
                    continue

                module = import_command_module(file)
                ensure_module_attributes(module, file, ["COMMAND_NAME", "HELP", "setup"])

                subparser = group_subparsers.add_parser(module.COMMAND_NAME, help=module.HELP, parents=[global_parser])
                module.setup(subparser)

                handler = getattr(module, "handle", None)
                if not callable(handler):
                    logger.error(f"'{file}' must define a callable 'handle(args)' function")
                    sys.exit(1)

                subparser.set_defaults(handler=handler)

    args = parser.parse_args()

    if args.verbose:
        logger.debug("Parsed args:", vars(args))

    if not hasattr(args, "handler") or not callable(args.handler):
        logger.error("No valid handler defined for the selected command.")
        sys.exit(1)

    return args
