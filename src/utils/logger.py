"""
This module makes Logger objects available for use when imported.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, TextIO


class Logger:
    """
    A simple logging utility serving as a way to persist logs between runs

    Data members:
    log_file (TextIO): The log file to write the log data to
                       Full path is configured in conf/logger_config.json
                       The log file's name contains the initialization time,
                       along with the configured name
    """

    def __init__(self, config_file_path: str) -> None:
        Path("./logs").mkdir(parents=True, exist_ok=True)
        with open(config_file_path, encoding="utf-8") as conf_file:
            json_data: Dict = json.load(conf_file)
        path:          str = json_data["logfile_path"]
        name:          str = json_data["logfile_name"]
        self.log_file: str = path + f"{datetime.now()}_" + name
        self.opened:   bool = False

    def write(self, component: str, message: str, severity: str) -> bool:
        """
        Opens and writes to the log file based on the message and severity

        Parameters:
        message  (str): The message to log to the file
        severity (str): The severity of the message to write to the file

        Returns:
        bool: Whether the writing to the file was successful or not
        """
        if self.opened:
            return False
        self.opened = True
        log_to: TextIO = open(self.log_file, "a", encoding="utf-8")
        to_log: str = (f"Component: {component}\n"
                       f"Severity: {severity}\n"
                       f"Message: {message}\n"
                       f"Time: {datetime.now()}")
        log_to.write(to_log + "\n" + "---\n")
        print(to_log)
        log_to.close()
        self.opened = False
        return True
