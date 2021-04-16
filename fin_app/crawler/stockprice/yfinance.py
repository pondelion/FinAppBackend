from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from typing import Optional

import yfinance

from ..base_crawler import BaseCrawler


class YfinanceCrawler(BaseCrawler):

    def run(
        self,
        code: int,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
        period='max',
        start_dt: Optional[date] = None,
        end_dt: Optional[date] = None,
        min_data_length: int = 10
    ) -> None:
        kwargs = {'code': code}

        try:
            ticker = yfinance.Ticker(f'{code}.T')
            history_kwargs = {}
            if start_dt is not None:
                history_kwargs['start'] = kwargs['start_dt'] = start_dt
            if end_dt is not None:
                history_kwargs['end'] =  kwargs['end_dt'] = end_dt + timedelta(days=1)
            if start_dt is None and end_dt is None:
                history_kwargs['period'] = period
            df = ticker.history(**history_kwargs)
            if len(df) < min_data_length:
                raise Exception('data length too short.')
            callback.on_finished(df, kwargs)
        except Exception as e:
            callback.on_failed(e, kwargs)
