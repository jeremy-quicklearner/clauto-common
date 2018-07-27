"""
Validation-related utilities
"""

# TODO: Write validation function for each config file setting

# IMPORTS ##############################################################################################################

# Standard Python modules

# Other Python modules

# Clauto Common Python modules
from clauto_common.patterns.singleton import Singleton
from clauto_common.patterns.wildcard import WILDCARD
from clauto_common.util.log import Log
from clauto_common.access_control import PRIVILEGE_LEVEL_PUBLIC
from clauto_common.access_control import PRIVILEGE_LEVEL_ADMIN
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
        Singleton.__init__(self)
        if Singleton.is_initialized(self):
            return

        self.log = Log("clautod")

    # noinspection PyMethodMayBeStatic
    def validate_params(self, params, required_param_names=[], optional_param_names=[]):
        """
        Will throw ValidationError if a required param is missing, and will convert missing optional params to WILDCARDs
        Any param that isn't in either list will be left behind
        :param required_param_names: Array of required parameter names
        :param optional_param_names: Array of optional parameter names
        :return: Sanitized params dict
        """

        sanitized_params = {}
        for required_param in required_param_names:
            if required_param not in params:
                self.log.verbose("Missing parameter: <%s>", required_param)
                raise ValidationException("Missing parameter: <%s>" % required_param)
            sanitized_params[required_param] = params[required_param]
        for optional_param in optional_param_names:
            if optional_param not in params:
                self.log.verbose("Filling in param <%s> with wildcard", optional_param)
                sanitized_params[optional_param] = WILDCARD
            else:
                sanitized_params[optional_param] = params[optional_param]
        return sanitized_params


    # noinspection PyMethodMayBeStatic
    def validate_string(
        self,
        candidate,
        can_be_none=False,
        can_be_wildcard=False,
        can_be_empty=False,
        can_contain_newline=True
    ):
        if candidate is None:
            if not can_be_none:
                raise NoneException()
            else:
                return None
        if candidate is WILDCARD:
            if not can_be_wildcard:
                raise ValidationException("Wildcard not allowed")
            else:
                return WILDCARD
        if not isinstance(candidate, str):
            self.log.debug("Expected type <str> but candidate is of type <%s>" % type(candidate))
            raise TypeError
        if (candidate == "") and (not can_be_empty):
            raise ValidationException()
        if ("\n" in candidate) and (not can_contain_newline):
            raise ValidationException()
        return candidate

    # noinspection PyMethodMayBeStatic
    def validate_int(self, candidate, can_be_none=False, can_be_wildcard=False,min_value=None, max_value=None):
        if candidate is None:
            if not can_be_none:
                raise NoneException()
            else:
                return None
        if candidate is WILDCARD:
            if not can_be_wildcard:
                raise ValidationException("Wildcard not allowed")
            else:
                return WILDCARD
        if not (isinstance(candidate, int) or isinstance(candidate, str)):
            self.log.debug("Expected type <int or str> but candidate is of type <%s>" % type(candidate))
            raise TypeError
        try:
            int_candidate = int(candidate)
        except ValueError:
            raise ValidationException()
        if min_value and int_candidate < min_value:
            raise ValidationException()
        if max_value and int_candidate > max_value:
            raise ValidationException()
        return int_candidate

    def validate_username(self, username, can_be_none=False, can_be_wildcard=False):
        try:
            self.validate_string(username, can_be_none, can_be_wildcard, False, False)
        except NoneException:
            raise NoneException("username")
        except TypeError:
            raise TypeError("username")
        except ValidationException:
            raise ValidationException("username <%s>" % username)

        self.log.verbose("Validated username <%s>", username)
        return username

    def validate_password(self, password, can_be_none=False, can_be_wildcard=False):
        try:
            self.validate_string(password, can_be_none, can_be_wildcard, False, False)
        except NoneException:
            raise NoneException("password")
        except TypeError:
            raise TypeError("password")
        except ValidationException:
            raise ValidationException("password")
        self.log.verbose("Validated a password")
        return password

    def validate_privilege_level(self, privilege_level, can_be_none=False, can_be_wildcard=False):
        try:
            privilege_level = self.validate_int(
                privilege_level,
                can_be_none,
                can_be_wildcard,
                PRIVILEGE_LEVEL_PUBLIC,
                PRIVILEGE_LEVEL_ADMIN
            )
        except NoneException:
            raise NoneException("privilege_level")
        except TypeError:
            raise TypeError("privilege_level")
        except ValidationException:
            raise ValidationException("privilege_level <%s>" % privilege_level)
        self.log.verbose("Validated privilege level <%s>" % privilege_level)
        return privilege_level
