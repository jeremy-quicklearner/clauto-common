# Exit codes and corresponding exceptions for Clauto modules

# EXIT CODES ###########################################################################################################

EXIT_OK                              =  0  # Everything is alright
EXIT_ERROR                           =  1  # Something went wrong and clautod doesn't know what it is
EXIT_ERROR_OS                        =  2  # The OS did something unexpected and clautod can't handle it
EXIT_ERROR_LOG_FILE_UNWRITEABLE      =  3  # The log file can't be written to
EXIT_ERROR_CONFIG_FILE_UNREADABLE    =  4  # The config file can't be read
EXIT_ERROR_CONFIG_SETTING_MISSING    =  5  # A setting is missing from the config file

# EXCEPTION CLASSES ####################################################################################################


class LogFileUnwriteableException(Exception):
    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        Exception.__init__(self, *args, **kwargs)


class ClautodAlreadyInstantiatedException(Exception):
    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        Exception.__init__(self, *args, **kwargs)


class EmptyConfigInstantiationException(Exception):
    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        Exception.__init__(self, *args, **kwargs)


class ConfigFileUnreadableException(Exception):
    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        Exception.__init__(self, *args, **kwargs)


class ConfigKeyException(Exception):
    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        Exception.__init__(self, *args, **kwargs)


class NoneException(Exception):
    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        Exception.__init__(self, *args, **kwargs)


class ValidationException(Exception):
    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        Exception.__init__(self, *args, **kwargs)


class DatabaseStateException(Exception):
    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        Exception.__init__(self, *args, **kwargs)

class MissingSubjectException(Exception):
    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        Exception.__init__(self, *args, **kwargs)

class InvalidCredentialsException(Exception):
    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        Exception.__init__(self, *args, **kwargs)


# MAP FROM EXCEPTION CLASSES TO EXIT CODES #############################################################################

exception_to_exit_code = {
    LogFileUnwriteableException:         EXIT_ERROR_LOG_FILE_UNWRITEABLE,
    ClautodAlreadyInstantiatedException: EXIT_ERROR,
    EmptyConfigInstantiationException:   EXIT_ERROR,
    ConfigFileUnreadableException:       EXIT_ERROR_CONFIG_FILE_UNREADABLE,
    ConfigKeyException:                  EXIT_ERROR_CONFIG_SETTING_MISSING,
    NoneException:                       EXIT_ERROR,
    ValidationException:                 EXIT_ERROR,
    DatabaseStateException:              EXIT_ERROR,
    MissingSubjectException:             EXIT_ERROR,
    InvalidCredentialsException:         EXIT_ERROR,

    "default":                           EXIT_ERROR
}
