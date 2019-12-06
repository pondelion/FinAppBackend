from abc import ABCMeta, abstractmethod


class BaseCrawler:

    def __init__(self):
        """init"""
        pass

    @abstractmethod
    def crawl(self):
        """crawl"""
        pass
