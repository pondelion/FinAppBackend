from abc import ABCMeta, abstractmethod


class BaseCrawler:

    def __init__(self):
        """init"""
        pass

    @abstractmethod
    def run(self):
        """single shot crawl"""
        raise NotImplementedError

    @abstractmethod
    def schedule(
        self,

    ):
        """scheduled crawl"""
        raise NotImplementedError
