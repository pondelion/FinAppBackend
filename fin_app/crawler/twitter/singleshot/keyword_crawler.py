import multiprocessing
from abc import ABCMeta, abstractmethod
from multiprocessing import Process
from typing import Dict, List

from ...base_crawler import BaseCrawler
from ..api import API


class KeywordCrawler(BaseCrawler):

    class Callback(metaclass=ABCMeta):

        @abstractmethod
        def on_finished(
            self,
            keyword: str,
            data: List[Dict],
        ) -> None:
            """[summary]
            
            Args:
                keyword (str): [description]
                data (List[Dict]): [description]
            
            Raises:
                NotImplementedError: [description]
            """
            raise NotImplementedError

        @abstractmethod
        def on_failed(
            self,
            keyword: str,
            e: Exception,
        ) -> None:
            """[summary]
            
            Args:
                keyword (str): [description]
            
            Raises:
                NotImplementedError: [description]
            """
            raise NotImplementedError

    class DefaultCallback(Callback):
        def on_finished(
            self,
            keyword: str,
            data: List[Dict],
        ) -> None:
            pass

        def on_failed(
            self,
            keyword: str,
            e: Exception,
        ) -> None:
            pass

    def __init__(
        self,
        keywords: List[str] = [],
        count: int = 200,
    ):
        """[summary]
        
        Args:
            keywords (List[str], optional): [description]. Defaults to [].
            count (int, optional): [description]. Defaults to 200.
        """
        self._keywords = keywords
        self._CPU_COUNT = multiprocessing.cpu_count()
        self._count = count

    def set_keywords(
        self,
        keywords: List[str]
    ) -> None:
        """[summary]
        
        Args:
            keywords (List[str]): [description]
        """
        self._keywords = keywords

    def add_keywords(
        self,
        keywords: List[str]
    ) -> None:
        """[summary]
        
        Args:
            keywords (List[str]): [description]
        """
        self._keywords += keywords

    def run(
        self,
        keywords: List[str] = [],
        count: int = None,
        callback: Callback = DefaultCallback()
    ) -> None:
        """[summary]
        
        Args:
            keywords (List[str], optional): [description]. Defaults to [].
            count (int, optional): [description]. Defaults to None.
            callback (Callback, optional): [description]. Defaults to None.
        """
        self._add_keywords(keywords)
        if count is not None:
            self._count = count
        sub_keywords = [
            self._keywords[i::self._CPU_COUNT] for i in range(self._CPU_COUNT)
        ]
        processes = [
            Process(self._crawl, (keywords, self._count, callback)) for keywords in sub_keywords
        ]
        [p.start() for p, keywords in zip(processes, sub_keywords) if len(keywords) != 0]
        [p.join() for p, keywords in zip(processes, sub_keywords) if len(keywords) != 0]

    def _crawl(
        self,
        keywords: List[str],
        count: int,
        callback: Callback,
    ) -> None:
        """[summary]
        
        Args:
            keywords (List[str]): [description]
        """
        for keyword in keywords:
            try:
                results = API.search(
                    q=keyword,
                    count=count
                )
                callback.on_finished(keyword, results)
            except Exception as e:
                callback.on_failed(keyword, e)
