from datetime import datetime
from dateutil.relativedelta import relativedelta

import yfinance

from ..base_crawler import BaseCrawler


class YfinanceCrawler(BaseCrawler):

    def run(
        self,
        code: int,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
        period='max'
    ) -> None:
        kwargs = {'code': code}

        try:
            ticker = yfinance.Ticker(f'{code}.T')
            df = ticker.history(period=period)
            if len(df) < 10:
                raise Exception('data length too short.')
            callback.on_finished(df, kwargs)
        except Exception as e:
            callback.on_failed(e, kwargs)
