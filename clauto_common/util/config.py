"""
Utilities related to config files
"""

# IMPORTS ##############################################################################################################

# Standard Python modules

# Other Python modules
import configargparse

# Clauto Common Python modules
from ..exceptions import ConfigFileUnreadableException
from ..exceptions import ConfigKeyException


# CONSTANTS ############################################################################################################

# CLASSES ##############################################################################################################

class ClautoConfig:

    def __init__(self, wrapped_dict):
        self.wrapped_dict = wrapped_dict

    def __getitem__(self, key):
        try:
            return self.wrapped_dict[key]
        except KeyError:
            raise ConfigKeyException(key)

    def items(self):
        return self.wrapped_dict.items()


# FUNCTIONS ############################################################################################################

def config_read(filename):
    """
    Parse a config file
    :param filename: The filename of the config file
    :return: An instance of a dict subclass containing every key/value pair in
    the config file, which throws a ConfigKeyException if one tries to get the
    value for a missing key
    """
    try:
        with open(filename, "r") as config_file:
            return ClautoConfig(configargparse.DefaultConfigFileParser().parse(config_file))
    except IOError:
        raise ConfigFileUnreadableException
