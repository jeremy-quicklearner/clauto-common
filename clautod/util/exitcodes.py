# Exit codes for clautod process

OK                         =  0  # Everything is alright
ERROR                      = -1  # Something went wrong and clautod doesn't know what it is
OS_ERROR                   = -2  # The OS did something unexpected and clautod can't handle it
LOG_FILE_UNWRITEABLE_ERROR = -3  # The log file can't be written to
