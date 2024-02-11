import abc


class MainBoardInfo(metaclass=abc.ABCMeta):

    def __init__(self):
        pass

    @abc.abstractmethod
    def get(self):
        pass
