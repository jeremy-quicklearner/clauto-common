"""
Logging-related utilities
"""

# IMPORTS ##############################################################################################################

# Standard Python modules
import re
import logging

# Other Python modules

# Clauto Common Python modules
from clauto_common.patterns.borg import Borg

# CONSTANTS ############################################################################################################

# Log line format strings
format_strings = {
    "user": "[%(asctime)s.%(msecs)d][%(clautod_levelname)s] %(message)s",
    "dev": "[%(asctime)s.%(msecs)d][%(clautod_levelname)s][%(clautod_module)s:%(lineno)d] %(message)s",
    "nul": "[%(asctime)s.%(msecs)d][???] %(message)s"
}

# Which format string to use for each level
log_level_to_format_string = {
    "CRT": "user",
    "CFG": "user",
    "ERR": "user",
    "WRN": "user",
    "INF": "user",
    "DBG": "dev",
    "VRB": "dev",
    "NUL": "nul"
}

"""
The magic numbers 9 and 41 fit into the logging library's internal hierarchy in which DEBUG is 10 and CRITICAL is 50:
CRITICAL = 50
<--------------CONFIG = 41
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
<--------------VERBOSE = 9
NOTSET = 0
"""
CUSTOM_LOGLEVEL_CONFIG = 41
CUSTOM_LOGLEVEL_VERBOSE = 9

# Associations between Python log levels and log level strings in clautod log format
log_level_to_clautod_log_level_string = {
    logging.CRITICAL:        "CRT",
    CUSTOM_LOGLEVEL_CONFIG:  "CFG",
    logging.ERROR:           "ERR",
    logging.WARNING:         "WRN",
    logging.INFO:            "INF",
    logging.DEBUG:           "DBG",
    CUSTOM_LOGLEVEL_VERBOSE: "VRB",
    logging.NOTSET:          "NUL"
}
clautod_log_level_string_to_log_level = {
    "CRT": logging.CRITICAL,
    "CFG": CUSTOM_LOGLEVEL_CONFIG,
    "ERR": logging.ERROR,
    "WRN": logging.WARNING,
    "INF": logging.INFO,
    "DBG": logging.DEBUG,
    "VRB": CUSTOM_LOGLEVEL_VERBOSE,
    "NUL": logging.NOTSET
}

# Extensions to the Python standard library's logger object


# This will be what gets called as "logger.config"
def logger_dot_config(self, message, *args, **kws):
    if self.isEnabledFor(CUSTOM_LOGLEVEL_CONFIG):
        self._log(CUSTOM_LOGLEVEL_CONFIG, message, args, **kws)


# This will be what gets called as "logger.verbose"
def logger_dot_verbose(self, message, *args, **kws):
    if self.isEnabledFor(CUSTOM_LOGLEVEL_VERBOSE):
        self._log(CUSTOM_LOGLEVEL_VERBOSE, message, args, **kws)


# CLASSES ##############################################################################################################

class NoLogDirException(Exception):
    pass


class LogFileUnwriteableException(Exception):
    pass


class Log(Borg):
    """
    This class wraps a logger object from Python's standard library, so that it produces the clautod log format and
    provides config and verbose log levels
    """

    # "PRIVATE" ########################################################################################################

    class ClautodFormatter(logging.Formatter):
        """
        Each line in the clautod log has a different format based on its log level, and some of those formats
        contain tags giving the position in source where the event happened. This is done using a custom
        Formatter subclass
        """

        def format(self, record):
            """
            Format a log line
            :param record: The log event object
            :return: The formatted log line (A string)
            """

            # Format the time
            self.datefmt = "%Y-%m-%d %H:%M:%S"

            # Pick which format string to use
            format_string = format_strings[
                log_level_to_format_string[
                    log_level_to_clautod_log_level_string[record.levelno]
                ]
            ]

            """
            Evaluate the custom format specifiers in the format string. This is a crude method of evaluation
            that prevents any future format string from containing the actual characters in any format specifier...
            but I doubt anyone will ever want those characters in there
            """
            format_string = format_string \
                .replace("%(clautod_levelname)s", log_level_to_clautod_log_level_string[record.levelno]) \
                .replace("%(clautod_module)s", record.pathname
                         .replace("/usr/share/clauto/", "")
                         .replace("/opt/venvs/clauto-common/lib/python3.5/site-packages/", "")
                         )

            # Backup the current format in case someone else is using the same logger
            original_format = self._style._fmt

            # Set the format
            self._style._fmt = format_string

            # Delegate the rest of the formatting to the superclass
            log_line = super().format(record)

            # Restore the original format
            self._style._fmt = original_format

            # The log line is formatted
            return log_line

    # "PUBLIC" #########################################################################################################

    def __init__(self, clauto_module=None, log_dir=None):
        """
        This function prepares a logger object to produce the clautod log
        :param log_dir: The path to the directory where the log file will go
        """

        Borg.__init__(self)

        # If the state is already initialized, just set the log directory
        if hasattr(self, "clauto_module"):
            if log_dir:
                self.log_dir_set(log_dir)
            return

        # The state isn't already initialized. A log directory must be supplied.
        if not log_dir:
            raise NoLogDirException

        # This is initialization
        self.clauto_module = clauto_module
        self.handler = None

        # Add the config and verbose log levels to the logging library's internal list
        logging.addLevelName(CUSTOM_LOGLEVEL_CONFIG, "CONFIG")
        logging.addLevelName(CUSTOM_LOGLEVEL_VERBOSE, "VERBOSE")

        # Add the functions to the Logger class
        logging.Logger.config = logger_dot_config
        logging.Logger.verbose = logger_dot_verbose

        # Obtain the logger from the Python logging library
        self.logger = logging.getLogger(clauto_module)

        # Set the log directory
        self.log_dir_set(log_dir)

        # Expose the logger's functions
        # They can't just be wrapped, or else record.pathname would point to this file
        self.critical = self.logger.critical
        self.config = self.logger.config
        self.error = self.logger.error
        self.warning = self.logger.warning
        self.info = self.logger.info
        self.debug = self.logger.debug
        self.verbose = self.logger.verbose


        self.debug("Logging initialized")

    def log_dir_set(self, new_log_dir):
        """
        Changes the directory where the log file goes
        :param new_log_dir: Path to the new log directory
        """

        # First, confirm the new log file is writable
        try:
            # Using w+ ensures that open() will create the file if it doesn't already exist
            open(new_log_dir + "/" + self.clauto_module + ".log", "w+").close()
        except IOError:
            raise LogFileUnwriteableException()

        # If this isn't the first time, the logger already has a handler applied. So remove it and close the stream
        if self.handler:
            self.logger.removeHandler(self.handler)
            self.handler.stream.close()

        # Create a handler for the new log file and apply a new instance of the custom formatter to it
        self.handler = logging.StreamHandler(open(new_log_dir + "/" + self.clauto_module + ".log", "w+"))
        formatter = self.ClautodFormatter()
        self.handler.setFormatter(formatter)

        # Get the log object and add the handler with the custom formatter
        self.logger.addHandler(self.handler)

    # Some wrapper functions for easy access to logging

    def level_set(self, new_level):
        """
        Sets the log level
        :param new_level: The new log level. One of CRT, CFG, ERR, WRN, INF, DBG, VRB
        :return:
        """
        self.logger.setLevel(clautod_log_level_string_to_log_level[new_level])