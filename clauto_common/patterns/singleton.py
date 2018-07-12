# Boilerplate code for Singleton design pattern.
# There are multiple instances of each Singleton
# subclass, but they all share the same state
# (not across different subclasses)


class Singleton:
    """
    Superclass for Singletons. To make a singleton,
    extend this class and call Singleton.__init__(self, __class) from your subclass's __init__()
    """

    # States of all the subclasses
    _states = {}

    def __init__(self, subclass):
        """
        Constructor for Singleton superclass
        :param subclass: The name of the subclass being instantiated
        """

        # If this is the subclass' first instantiation, register its state
        if subclass not in Singleton._states:
            Singleton._states[subclass] = {}

        # The new instance's state must be shared with other instances
        self.__dict__ = self._states[subclass]

    @staticmethod
    def is_initialized(subclass):
        """
        Returns true if a Singleton subclass has already been initialized
        :param subclass: The subclass to check
        :return: Whether the subclass has been initialized already
        """

        # If the class' state has been registered and isn't empty, then its
        # constructor must have filled in its state previously
        return (subclass in Singleton._states) and (Singleton._states[subclass])
