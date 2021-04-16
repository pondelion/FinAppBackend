import os
from typing import Dict
from datetime import datetime, timedelta, date

import pandas as pd

from fin_app.crawler.stockprice import YfinanceCrawler
from fin_app.utils.config import DataLocationConfig
from fin_app.utils.logger import Logger


TAG = 'yfinance stockprice crawl'


class Callback(YfinanceCrawler.Callback):

    def on_finished(
        self,
        data: pd.DataFrame,
        args: Dict,
    ) -> None:

        filepath = os.path.join(
            DataLocationConfig.STOCKPRICE_YFINANCE_DAILY_BASEDIR,
            args['start_dt'].strftime('%Y%m%d'),
            f'{args["code"]}.csv'
        )
        data.to_csv(filepath)
        Logger.i(TAG, f'Saved data to {filepath}')

    def on_failed(
        self,
        e: Exception,
        args: Dict,
    ) -> None:
        Logger.e(TAG, f'on_failed : {args["code"]} : {e}')


def _crawl():
    df_stocklist = pd.read_csv(
        DataLocationConfig.STOCKLIST_FILE
    )

    codes = df_stocklist['銘柄コード'].unique()

    yfc = YfinanceCrawler()
    start_dt = end_dt = date.today() - timedelta(days=1)
    for code in codes:
        yfc.run(
            code=code,
            start_dt=start_dt,
            end_dt=end_dt,
            min_data_length=1,
            callback=Callback()
        )


def crawl(event, context):
    _crawl()