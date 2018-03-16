class Observable(object):

    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def remove_all_observers(self):
        self.observers = []

    def update_observable(self, arg):
        for observer in self.observers:
            observer.update_observer(arg)
