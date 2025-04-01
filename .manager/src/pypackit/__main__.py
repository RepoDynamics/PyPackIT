import argparse

from loggerman import logger

from pypackit import script


def cli():
    logger.initialize(realtime_levels=list(range(7)))
    parser = argparse.ArgumentParser(description="Project Manager CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for script_name in script.__all__:
        script_module = getattr(script, script_name)
        script_module.cli_parser(subparsers)

    args = parser.parse_args()
    input_script_name = args.command.replace("-", "_")
    delattr(args, "command")
    input_script = getattr(script, input_script_name)
    input_script.run_cli(parser, args)
    return
