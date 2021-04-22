import os
from typing import Dict
from datetime import datetime, timedelta, date

import pandas as pd

from fin_app.crawler.stockprice import YfinanceCrawler
from fin_app.utils.config import DataLocationConfig
from fin_app.utils.logger import Logger
from fin_app.storage.s3 import S3


TAG = 'yfinance stockprice crawl'
START_CODE = os.environ.get('START_CODE', None)
END_CODE = os.environ.get('END_CODE', None)
CODE_SUFFIX = f'_{START_CODE}_{END_CODE}' if START_CODE is not None and END_CODE is not None else ''


class Callback(YfinanceCrawler.Callback):

    def on_finished(
        self,
        data: pd.DataFrame,
        args: Dict,
    ) -> None:
        local_dir = os.path.join(
            '/tmp',
            'stock'
        )
        os.makedirs(local_dir, exist_ok=True)
        local_stock_file = os.path.join(
            local_dir,
            f'{args["start_dt"].strftime("%Y%m%d")}{CODE_SUFFIX}.csv'
        )
        data.to_csv(local_stock_file)
        s3_filepath = os.path.join(
            DataLocationConfig.STOCKPRICE_YFINANCE_DAILY_BASEDIR,
            f'{args["start_dt"].strftime("%Y%m%d")}/{CODE_SUFFIX}.csv'
        )
        S3.save_file(
            local_stock_file,
            s3_filepath,
        )
        Logger.i(TAG, f'on_fnished : {args["code"]} : {len(data)}')

    def on_failed(
        self,
        e: Exception,
        args: Dict,
    ) -> None:
        Logger.e(TAG, f'on_failed : {args["code"]} : {e}')


def _crawl():

    LOCAL_STOCKLIST_FILE = '/tmp/stocklist.csv'
    S3.download_file(
        DataLocationConfig.STOCKLIST_FILE,
        LOCAL_STOCKLIST_FILE,
    )
    df_stocklist = pd.read_csv(LOCAL_STOCKLIST_FILE)
    if START_CODE is not None and END_CODE is not None:
        df_stocklist = df_stocklist[
            (df_stocklist['銘柄コード'] >= int(START_CODE)) & (df_stocklist['銘柄コード'] <= int(END_CODE))
        ]

    codes = df_stocklist['銘柄コード'].unique().tolist()

    yfc = YfinanceCrawler()
    start_dt = end_dt = date.today() - timedelta(days=1)

    yfc.run(
        code=codes,
        start_dt=start_dt,
        end_dt=end_dt,
        min_data_length=1,
        callback=Callback()
    )


def crawl(event, context):
    _crawl()
