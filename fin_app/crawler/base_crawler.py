from abc import ABCMeta, abstractmethod


class BaseCrawler(metaclass=ABCMeta):

    def __init__(self):
        """init"""
        pass

    @abstractmethod
    def run(self):
        """single shot crawl"""
        raise NotImplementedError
