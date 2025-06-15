import argparse
import importlib.util
import pathlib
import sys

from . import bt_logger

logger = bt_logger.get_logger(__name__)

BASE_COMMANDS_DIR = pathlib.Path(__file__).parent / "commands"


def import_command_module(path: pathlib.Path):
    """
    Imports a Python module from the given file path. The module is dynamically
    loaded using importlib utilities. If the import fails due to an invalid or
    unloadable module, an error is logged, and the program exits with status code 1.

    Parameters:
        path (pathlib.Path): The file path of the module to import.

    Returns:
        ModuleType: The dynamically imported module.
    """
    spec = importlib.util.spec_from_file_location(name=path.stem, location=str(path))
    if spec is None or spec.loader is None:
        logger.error(f"Cannot import module from {path}")
        sys.exit(1)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    logger.debug(f"Imported Module {path}")
    return module


def ensure_module_attributes(module, path, required_attrs):
    """
    Ensures the presence of required attributes in a module.

    This function checks if a given module contains all the attributes listed
    in the required attributes parameter. If any required attribute is
    missing, it logs a warning message and terminates the program with
    a status code of 1.

    Parameters:
        module: Any
            The module object to be checked for the presence of required
            attributes.
        path: str
            The path or name of the module being checked, used in the
            log message for context.
        required_attrs: List[str]
            A list of attribute names to check for within the module.

    Raises:
        SystemExit:
            If any required attribute is missing from the module, the system
            exits with a status code of 1.
    """
    for attr in required_attrs:
        if not hasattr(module, attr):
            logger.warning(f"'{path}' is missing required attribute: {attr}")
            sys.exit(1)


def parse():
    """
    Parses command-line arguments and configures the application command structure.

    This function defines a command-line interface (CLI) for managing various
    tools. It leverages hierarchical argument parsing to accommodate both
    single-command and multi-command groups, allowing for a flexible toolset
    architecture. The CLI consists of a global argument parser, group-level
    parsers for command categories, and subparsers for specific subcommands.
    Dynamic loading is used to incorporate commands declared in external
    modules based on a predefined directory structure.

    Arguments are parsed using the argparse library and are returned as a
    namespace. Handlers for commands are dynamically set at runtime and can
    be invoked later as per user input.

    Returns:
        argparse.Namespace: The parsed command-line arguments containing all
        flags, options, and other parameters, as well as the appropriate
        handler function for the selected command.

    Raises:
        SystemExit: If a command or group fails to provide a valid 'handle'
        function or if argument parsing encounters unrecoverable errors.
    """
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
