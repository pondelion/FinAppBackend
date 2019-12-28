from abc import ABCMeta, abstractmethod


class BaseStorage(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def upload_file():
        raise NotImplementedError
