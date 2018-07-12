# Exit codes and corresponding exceptions for Clauto modules

# EXIT CODES ###########################################################################################################

EXIT_OK                           =  0  # Everything is alright
EXIT_ERROR                        = -1  # Something went wrong and clautod doesn't know what it is
EXIT_ERROR_OS                     = -2  # The OS did something unexpected and clautod can't handle it
EXIT_ERROR_LOG_FILE_UNWRITEABLE   = -3  # The log file can't be written to
EXIT_ERROR_CONFIG_FILE_UNREADABLE = -4  # The config file can't be read

# EXCEPTION CLASSES ####################################################################################################


class LogFileUnwriteableException(Exception):
    pass


class ClautodAlreadyInstantiatedException(Exception):
    pass


class ConfigFileUnreadableException(Exception):
    pass


# MAP FROM EXCEPTION CLASSES TO EXIT CODES #############################################################################

exception_to_exit_code = {
    LogFileUnwriteableException: EXIT_ERROR_LOG_FILE_UNWRITEABLE,
    ClautodAlreadyInstantiatedException: EXIT_ERROR,
    ConfigFileUnreadableException: EXIT_ERROR_CONFIG_FILE_UNREADABLE,

    "default": EXIT_ERROR
}
