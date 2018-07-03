"""
Logging-related utilities
"""

# IMPORTS ##############################################################################################################

# Standard Python modules
import logging

# Other Python modules

# Clauto modules
from util import exitcodes

# CONSTANTS ############################################################################################################

# Log file name
LOG_FILENAME = "clautod.log"

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

# Python logger object
LOGGER = logging.getLogger("clautod")

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


# STATE ################################################################################################################

# Whether the logging is initialized or not
is_initialized = False

# Handler object enabling logging to the current log file
handler = None

# HELPERS ##############################################################################################################


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
            .replace("%(clautod_module)s", record.pathname.replace("/usr/share/clauto/clautod/", ""))

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

# "EXPOSED" ############################################################################################################


def init(log_dir):
    """
    This function prepares a logger object to produce the clautod log
    :param log_dir: The path to the directory where the log file will go
    """

    # Set the log file
    log_dir_set(log_dir)

    # Add the config and verbose log levels to the logging library's internal list
    logging.addLevelName(CUSTOM_LOGLEVEL_CONFIG, "CONFIG")
    logging.addLevelName(CUSTOM_LOGLEVEL_VERBOSE, "VERBOSE")

    # This will be what gets called as "logger.config"
    def logger_dot_config(self, message, *args, **kws):
        if self.isEnabledFor(CUSTOM_LOGLEVEL_CONFIG):
            self._log(CUSTOM_LOGLEVEL_CONFIG, message, args, **kws)

    # This will be what gets called as "logger.verbose"
    def logger_dot_verbose(self, message, *args, **kws):
        if self.isEnabledFor(CUSTOM_LOGLEVEL_VERBOSE):
            self._log(CUSTOM_LOGLEVEL_VERBOSE, message, args, **kws)

    # Add the functions to the Logger class
    logging.Logger.verbose = logger_dot_verbose
    logging.Logger.config = logger_dot_config

    # The logging is now initialized
    global is_initialized
    is_initialized = True

    debug("Logging initialized")


def log_dir_set(new_log_dir):
    """
    Changes the directory where the log file goes
    :param new_log_dir: Path to the new log directory
    """

    # First, confirm the new log file is writable
    try:
        # Using w+ ensures that open() will create the file if it doesn't already exist
        open(new_log_dir + "/" + LOG_FILENAME, "w+").close()
    except IOError:
        exit(exitcodes.LOG_FILE_UNWRITEABLE_ERROR)

    # If logging is initialized, the logger already has a handler applied. So remove it and close the stream
    global handler
    if is_initialized:
        LOGGER.removeHandler(handler)
        handler.stream.close()

    # Create a handler for the new log file and apply a new instance of the custom formatter to it
    handler = logging.StreamHandler(open(new_log_dir + "/" + LOG_FILENAME, "w+"))
    handler.setFormatter(ClautodFormatter())

    # Get the log object and add the handler with the custom formatter
    LOGGER.addHandler(handler)


def cleanup():
    """
    Actions to be performed when clautod is terminated
    """

    # If logging is initialized, the logger has a custom formatter applied. So remove it
    global handler
    if is_initialized:
        LOGGER.removeHandler(handler)

# Some wrapper functions for easy access to logging


def level_set(new_level):
    """
    Sets the log level
    :param new_level: The new log level. One of CRT, CFG, ERR, WRN, INF, DBG, VRB
    :return:
    """
    LOGGER.setLevel(clautod_log_level_string_to_log_level[new_level])


def critical(msg, *args, **kwargs):
    LOGGER.critical(msg, *args, **kwargs)


def config(msg, *args, **kwargs):
    # This function is added dynamically to the Logger class by init()
    LOGGER.config(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    LOGGER.error(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    LOGGER.warning(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    LOGGER.info(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    LOGGER.debug(msg, *args, **kwargs)


def verbose(msg, *args, **kwargs):
    # This function is added dynamically to the Logger class by init()
    LOGGER.verbose(msg, *args, **kwargs)
