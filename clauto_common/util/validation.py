"""
Validation-related utilities
"""

# TODO: Write validation function for each config file setting

# IMPORTS ##############################################################################################################

# Standard Python modules

# Other Python modules

# Clauto Common Python modules
from clauto_common.patterns.singleton import Singleton
from clauto_common.util.log import Log
from clauto_common.exceptions import NoneException
from clauto_common.exceptions import ValidationException


# CONSTANTS ############################################################################################################

# CLASSES ##############################################################################################################

class Validator(Singleton):
    """
    This class contains lots of methods to validate parameters throughout Clauto
    """

    def __init__(self):
        # Singleton instantiation
        Singleton.__init__(self, __class__)
        if Singleton.is_initialized(__class__):
            return

        self.log = Log("clautod")

    # noinspection PyMethodMayBeStatic
    def validate_string(self, candidate, can_be_none=False, can_be_empty=False, can_contain_newline=True):
        if (candidate is None) and (not can_be_none):
            raise NoneException()
        if not isinstance(candidate, str):
            raise TypeError
        if (candidate == "") and (not can_be_empty):
            raise ValidationException()
        if ("\n" in candidate) and (not can_contain_newline):
            raise ValidationException()
        return candidate

    def validate_username(self, username, can_be_none=False):
        self.validate_string(username, can_be_none, False, False)
        self.log.verbose("Validated username <%s>", username)
        return username

    def validate_password(self, password, can_be_none=False):
        self.validate_string(password, can_be_none, False, False)
        self.log.verbose("Validated a password")
        return password
