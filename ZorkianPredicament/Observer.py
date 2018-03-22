
from abc import abstractmethod, ABCMeta


class Observer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, arg):
        pass
