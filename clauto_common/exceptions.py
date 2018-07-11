# Exit codes and corresponding exceptions for Clauto modules

# EXIT CODES ###########################################################################################################

EXIT_OK                         =  0  # Everything is alright
EXIT_ERROR                      = -1  # Something went wrong and clautod doesn't know what it is
EXIT_ERROR_OS                   = -2  # The OS did something unexpected and clautod can't handle it
EXIT_ERROR_LOG_FILE_UNWRITEABLE = -3  # The log file can't be written to

# EXCEPTION CLASSES ####################################################################################################


class LogFileUnwriteableException(Exception):
    pass


class ClautodAlreadyInstantiatedException(Exception):
    pass


# MAP FROM EXCEPTION CLASSES TO EXIT CODES #############################################################################

exception_to_exit_code = {
    LogFileUnwriteableException: EXIT_ERROR_LOG_FILE_UNWRITEABLE,
    ClautodAlreadyInstantiatedException: EXIT_ERROR,

    "default": EXIT_ERROR
}
