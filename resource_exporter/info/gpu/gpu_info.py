import abc


class GPUInfo(metaclass=abc.ABCMeta):

    def __init__(self):
        pass

    @abc.abstractmethod
    def get(self):
        pass
