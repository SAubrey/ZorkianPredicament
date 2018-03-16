
from abc import abstractmethod, ABCMeta


class Observer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update_observer(self, arg):
        pass
