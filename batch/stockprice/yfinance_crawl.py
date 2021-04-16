import sys
sys.path.append('../..')
import os
from typing import Dict

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
            DataLocationConfig.STOCKPRICE_YFINANCE_CONCAT_BASEDIR,
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


def main():
    df_stocklist = pd.read_csv(
        DataLocationConfig.STOCKLIST_FILE
    )

    print(df_stocklist['銘柄コード'].unique())

    codes = df_stocklist['銘柄コード'].unique()

    yfc = YfinanceCrawler()
    for code in codes:
        yfc.run(
            code=code,
            period='max',
            callback=Callback()
        )


if __name__ == '__main__':
    main()
