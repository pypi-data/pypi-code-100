import logging
from datetime import datetime
from os import getenv, system
from dotenv import load_dotenv
from pathlib import Path


class Logger:
    def __init__(self):
        # Load envs
        load_dotenv()

        self.log_folder = Path(getenv("TT_LOG_FOLDER", "."))

        FORMAT = "%(asctime)-10s | %(levelname)s | %(message)s"

        self.log_file = self.log_folder / f"{(datetime.today()).strftime('%Y%m%d')}.log"
        logging.basicConfig(filename=self.log_file, format=FORMAT, level=logging.INFO)

    def get_logs(self, last_log: bool, output: bool) -> None:
        if last_log:
            list_of_files = Path.glob(self.log_folder / "*.log")
            list_of_files_not_empty = list(
                filter(lambda x: Path.getsize(x) > 0, list_of_files)
            )  # Remove all empty files

            if list_of_files_not_empty == []:
                print("No logs yet")
                return None

            latest_file = max(
                list_of_files_not_empty, key=Path.getctime
            )  # List the last log by creation date

            if output:
                with open(latest_file, "r") as file:
                    print(file.read())  # Output to stdout
            else:
                system(f"open {latest_file}")  # Open directory

            if dir:
                with open(latest_file, "rw") as file:
                    print(file.read())
        else:
            system(f"open {self.log_folder}")

    def info(self, data):
        logging.info(data)

    def warning(self, data):
        logging.warn(data)

    def error(self, data):
        logging.error(data)
