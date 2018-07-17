"""
Logging-related utilities
"""

# IMPORTS ##############################################################################################################

# Standard Python modules
import logging
import sys

# Other Python modules

# Clauto Common Python modules
from clauto_common.patterns.singleton import Singleton
from clauto_common.exceptions import LogFileUnwriteableException

# CONSTANTS ############################################################################################################

# Log line format strings
format_strings = {
    "user": "[%(asctime)s.%(msecs)03d][%(clautod_levelname)s] %(message)s",
    "dev": "[%(asctime)s.%(msecs)03d][%(clautod_levelname)s][%(clautod_module)s:%(lineno)d] %(message)s",
    "nul": "[%(asctime)s.%(msecs)03d][???] %(message)s"
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

class Log(Singleton):
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

    def __init__(self, clauto_module="clauto-common", log_dir=None):
        """
        This function prepares a logger object to produce the clautod log
        :param log_dir: The path to the directory where the log file will go
        """

        # Singleton instantiation
        Singleton.__init__(self)
        if Singleton.is_initialized(self):
            if log_dir and log_dir != self.log_dir:
                self.debug("Logging is already initialized with dir <%s>. Not setting log dir to <%s>.",
                           self.log_dir,
                           log_dir
                           )
            if clauto_module != "clauto-common" and clauto_module != self.clauto_module:
                self.debug("Logging is already initialized with module <%s>. Not setting module to <%s>.",
                           self.clauto_module,
                           clauto_module
                           )

            return

        # If there's no log directory, log to stdout
        if not log_dir:
            self.log_dir = "STDOUT"
            self.handler = logging.StreamHandler(sys.stdout)

        # If the log directory is given, then log to a file in it
        else:
            # First, confirm the new log file is writable
            try:
                # Using w+ ensures that open() will create the file if it doesn't already exist
                open(log_dir + "/" + clauto_module + ".log", "w+").close()
            except IOError:
                raise LogFileUnwriteableException(log_dir + "/" + clauto_module + ".log")

            # Now that the log file is confirmed writable, start initializing
            self.log_dir = log_dir

            # Create a handler for the new log file
            self.handler = logging.StreamHandler(open(log_dir + "/" + clauto_module + ".log", "w+"))

        # Now we have a handler, so apply the custom formatter to it
        formatter = self.ClautodFormatter()
        self.handler.setFormatter(formatter)

        # Get the log object and add the handler with the custom formatter
        self.logger = logging.getLogger(clauto_module)
        self.logger.addHandler(self.handler)

        # Add the config and verbose log levels to the logging library's internal list
        logging.addLevelName(CUSTOM_LOGLEVEL_CONFIG, "CONFIG")
        logging.addLevelName(CUSTOM_LOGLEVEL_VERBOSE, "VERBOSE")

        # Add the functions to the Logger class
        logging.Logger.config = logger_dot_config
        logging.Logger.verbose = logger_dot_verbose

        # Expose the logger's functions
        # They can't just be wrapped, or else record.pathname would point to this file (See the custom formatter class)
        # The config and verbose functions are added dynamically by __init__()
        self.critical = self.logger.critical
        # noinspection PyUnresolvedReferences
        self.config = self.logger.config
        self.error = self.logger.error
        self.warning = self.logger.warning
        self.info = self.logger.info
        self.debug = self.logger.debug
        # noinspection PyUnresolvedReferences
        self.verbose = self.logger.verbose

        # The initial level is INF
        self.level_set("INF")

        # Initialization is finished
        self.clauto_module = clauto_module
        self.info("Logging initialized")

    # Some wrapper functions for easy access to logging

    def level_set(self, new_level):
        """
        Sets the log level
        :param new_level: The new log level. One of CRT, CFG, ERR, WRN, INF, DBG, VRB
        :return:
        """
        self.logger.setLevel(clautod_log_level_string_to_log_level[new_level])
