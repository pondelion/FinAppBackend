import pandas_datareader.data as web

from ..base_crawler import BaseCrawler


class StooqCrawler(BaseCrawler):

    def run(
        self,
        code: int,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
    ) -> None:
        kwargs = {'code': code}

        try:
            df = web.DataReader(f'{code}.JP', 'stooq')
            callback.on_finished(df, kwargs)
        except Exception as e:
            callback.on_failed(e, kwargs)
