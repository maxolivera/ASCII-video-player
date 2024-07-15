import os
import sys
import argparse
import logging
from PySide6.QtWidgets import QApplication

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
