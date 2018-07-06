# Parent class for Alex Martelli's "Borg" pattern (See: http://www.aleax.it/Python/5ep.html)
class Borg:
    _state = {}
    def __init__(self):
        self.__dict__ = self._state