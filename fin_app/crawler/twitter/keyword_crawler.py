from typing import List
from ..base_crawler import BaseCrawler


class KeywordCrawler(BaseCrawler):

    def __init__(
        self,
        keywords: List[str]=[]
    ):
        self._keywords = keywords

    def set_keywords(
        self,
        keywords: List[str]
    ) -> None:
        self._keywords = keywords

    def add_keywords(
        self,
        keywords: List[str]
    ) -> None:
        self._keywords += keywords
