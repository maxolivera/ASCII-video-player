import argparse
import logging
import sys
from PySide6.QtWidgets import QApplication
from src.gui.video_player import App


def main():
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser()
    _ = parser.add_argument(
        "-log",
        "--loglevel",
        default="warning",
        help="Provide logging level. Example: -log=info",
    )

    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel.upper())
    logging.info("Logging now setup.")

    print(logging.getLevelName(logger.getEffectiveLevel()))
    logging.info("Starting UI")
    app = QApplication([])

    window = App()

    sys.exit(app.exec())


main()
