from argparse import ArgumentParser
import logging
from pathlib import Path
from typing import Optional

from typing_extensions import Literal

from . import app
from .config import Config


ConfigAction = Literal["check", "create"]


parser = ArgumentParser(prog="microchat")
subparsers = parser.add_subparsers()

run_args = subparsers.add_parser("run", help="run MicroChat server")
run_args.add_argument(
    "--config", action="store", required=False,
    type=Path, default="./config.json",
    help="filename or path to config"
)

config_args = subparsers.add_parser("config", help="run config tools")
config_args.add_argument("action", choices=["check", "create"])
config_args.add_argument(
    "path", action="store", nargs='?',
    type=Path, default="./congig.json",
    help="filename or path to config"
)

args = parser.parse_args()

config_path: Optional[Path] = getattr(args, 'config', None)
config_action: Optional[ConfigAction] = getattr(args, 'action', None)

if config_path:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("main")
    logger.info(f"Use config file {config_path.absolute()}")
    if not config_path.exists():
        logger.error("Config file does not exists")
        exit(1)
    if not config_path.is_file():
        logger.error(f"{config_path.absolute()} is not a file")
        exit(1)
    with config_path.open() as config_file:
        raw_config = config_file.read()
    try:
        config = Config.load(config_file)
    except ValueError as e:
        logging.error(f"Config parsing error. {e}")
        exit()
    app.run(config)
elif config_action:
    pass
else:
    parser.print_help()
