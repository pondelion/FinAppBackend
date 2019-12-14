import requests
from abc import ABCMeta, abstractmethod
from typing import Dict, List

import pandas as pd

from ..base_crawler import BaseCrawler
from ...utils.logger import Logger


class StockpriceCrawler(BaseCrawler):

    class Callback(metaclass=ABCMeta):

        @abstractmethod
        def on_finished(
            self,
            code: int,
            year: int,
            data: pd.DataFrame,
        ) -> None:
            """[summary]
            
            Args:
                code (int): [description]
                year (int): [description]
                data ([type]): [description]
            
            Raises:
                NotImplementedError: [description]
            """
            raise NotImplementedError

        @abstractmethod
        def on_failed(
            self,
            code: int,
            year: int,
            e: Exception,
        ) -> None:
            """[summary]
            
            Args:
                code (int): [description]
                year (int): [description]
                data ([type]): [description]
            
            Raises:
                NotImplementedError: [description]
            """
            raise NotImplementedError

    class DefaultCallback(Callback):
        def on_finished(
            self,
            code: int,
            year: int,
            data: pd.DataFrame,
        ) -> None:
            pass

        def on_failed(
            self,
            code: int,
            year: int,
            e: Exception,
        ) -> None:
            pass

    def __init__(self):
        self._URL = 'https://kabuoji3.com/stock/file.php'

    def run(
        self,
        code: int,
        year: int,
        callback: Callback = DefaultCallback(),
    ) -> None:
        """[summary]
        
        Args:
            code (int): [description]
            year (int): [description]
            callback (Callback, optional): [description]. Defaults to DefaultCallback().
        
        Raises:
            Exception: [description]
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
            }
            res = requests.post(
                self._URL,
                data={
                    'code': code,
                    'year': year
                },
                headers=headers,
            )
            if res.status_code != 200:
                raise Exception('Status code != 200')
        except Exception as e:
            Logger.e('StockpriceCrawler#crawl', f'Failed to post : {e}')
            callback.on_failed(
                code, year, e
            )
            return

        try:
            tmp_filepath = f'/tmp/stockprice_{code}_{year}.csv'
            with open(tmp_filepath, 'wb') as f:
                f.write(res.content)
            df_stockprice = pd.read_csv(
                tmp_filepath,
                encoding='SHIFT-JIS',
                skiprows=1,
            )
        except Exception as e:
            Logger.e('StockpriceCrawler#crawl', f'Failed to handle file : {e}')
            callback.on_failed(
                code, year, e
            )
            return

        if self._validate_date(df_stockprice) is False:
            callback.on_failed(
                code, year, Exception('Wrong data')
            )
            return

        callback.on_finished(
            code, year, df_stockprice
        )

    def _validate_date(
        self,
        df_stockprice: pd.DataFrame,
    ) -> bool:
        """[summary]
        
        Args:
            df_stockprice (pd.DataFrame): [description]
        
        Returns:
            bool: [description]
        """
        try:
            df_stockprice['高値']
        except Exception:
            return False

        return True
