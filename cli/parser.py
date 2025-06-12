import argparse
import importlib.util
import pathlib

BASE_COMMANDS_DIR = pathlib.Path(__file__).parent / "commands"

def import_command_module(path: pathlib.Path):
    """Import a module from a file path."""
    spec = importlib.util.spec_from_file_location(
        name=path.stem,
        location=str(path)
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def parse():
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    global_parser.add_argument("-oe", "--on-exit", type=str, help="Action to perform on exit")

    parser = argparse.ArgumentParser(
        prog="BlenderTools CLI",
        description="Command Line Interface Tools",
        parents=[global_parser]
    )

    main_subparsers = parser.add_subparsers(dest="group", required=True)

    for group_dir in BASE_COMMANDS_DIR.iterdir():
        if not group_dir.is_dir() or group_dir.name.startswith("__"):
            continue

        group_name = group_dir.name

        # Check for main.py to allow folder to act as single command
        main_command_file = group_dir / "main.py"
        if main_command_file.exists():
            module = import_command_module(main_command_file)

            if not all(hasattr(module, attr) for attr in ["COMMAND_NAME", "HELP", "setup"]):
                raise ValueError(f"{main_command_file} must define COMMAND_NAME, HELP, and setup()")

            group_parser = main_subparsers.add_parser(group_name, help=module.HELP, parents=[global_parser])
            module.setup(group_parser)
            group_parser.set_defaults(handler=getattr(module, "handle", None))

        else:
            # Otherwise treat as a group of subcommands
            group_parser = main_subparsers.add_parser(group_name, help=f"{group_name} commands", parents=[global_parser])
            group_subparsers = group_parser.add_subparsers(dest="command", required=True)

            for file in group_dir.glob("*.py"):
                if file.name == "__init__.py":
                    continue

                module = import_command_module(file)

                if not hasattr(module, "COMMAND_NAME") or not hasattr(module, "HELP") or not hasattr(module, "setup"):
                    raise ValueError(f"{file} must define COMMAND_NAME, HELP, and setup()")

                subparser = group_subparsers.add_parser(module.COMMAND_NAME, help=module.HELP, parents=[global_parser])
                module.setup(subparser)
                subparser.set_defaults(handler=getattr(module, "handle", None))
                
    args = parser.parse_args()
    print(args.__dict__)
    return args