import multiprocessing
from abc import ABCMeta, abstractmethod
from multiprocessing import Process
from typing import Dict, List
from datetime import datetime

from ...base_crawler import BaseCrawler
from ..api import TWEEPY_API


class UserCrawler(BaseCrawler):

    def run(
        self,
        screen_name: str,
        count_per_page: int = 200,
        n_pages: int = 20,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
    ) -> None:
        self._crawl(
            screen_name, count_per_page, n_pages, callback
        )

    def _crawl(
        self,
        screen_name: str,
        count_per_page: int,
        n_pages: int,
        callback: BaseCrawler.Callback,
    ):
        kwargs = {
            'screen_name': screen_name
        }
        pages = range(1, n_pages+1)

        for page in pages:
            kwargs['page'] = page
            try:
                tweets = TWEEPY_API.user_timeline(
                    screen_name=screen_name,
                    count=count_per_page,
                    page=page
                )
                callback.on_finished(tweets, kwargs)
            except Exception as e:
                callback.on_failed(e, kwargs)
