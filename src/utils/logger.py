import json
from datetime import datetime
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
        conf_file:     TextIO = open(config_file_path)
        json_data:     Dict   = json.load(conf_file)
        path:          str    = json_data["logfile_path"]
        name:          str    = json_data["logfile_name"]
        self.log_file: str    = path + f"{datetime.now()}_" + name
        self.opened:   bool   = False

    def write(self, message: str, severity: str) -> bool:
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
        log_to: TextIO = open(self.log_file, "a")
        to_log: str = (f"severity: {severity}\n"
                       f"message: {message}\n"
                       f"time: {datetime.now()}")
        log_to.write(to_log + "\n" + "---\n")
        print(to_log)
        log_to.close()
        self.opened = False
        return True