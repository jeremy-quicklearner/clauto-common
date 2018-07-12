"""
Utilities related to config files
"""

# IMPORTS ##############################################################################################################

# Standard Python modules

# Other Python modules
import configargparse

# Clauto Common Python modules
from ..exceptions import ConfigFileUnreadableException

# CONSTANTS ############################################################################################################

# FUNCTIONS ############################################################################################################

def config_read(filename):
    """
    Parse a config file
    :param filename: The filename of the config file
    :return: A dict containing every key/value pair in the config file
    """
    try:
        with open(filename, "r") as config_file:
            return configargparse.DefaultConfigFileParser().parse(config_file)
    except IOError:
        raise ConfigFileUnreadableException