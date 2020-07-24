import sys
sys.path.append('../..')
import os
from typing import Dict

import pandas as pd

from fin_app.crawler import StooqCrawler
from fin_app.utils.config import DataLocationConfig
from fin_app.utils.logger import Logger


TAG = 'stooq_crawl'


class Callback(StooqCrawler.Callback):

    def on_finished(
        self,
        data: pd.DataFrame,
        args: Dict,
    ) -> None:

        filepath = os.path.join(
            DataLocationConfig.STOCKPRICE_BASEDIR,
            'stooq',
            f'{args["code"]}.csv'
        )
        data.to_csv(
            filepath,
            index=None,
        )
        print(f'Saved data to {filepath}')

    def on_failed(
        self,
        e: Exception,
        args: Dict,
    ) -> None:
        print(f'on_failed : {args["code"]} : {e}')


def main():
    df_stocklist = pd.read_csv(
        DataLocationConfig.STOCKLIST_FILE
    )

    print(df_stocklist['銘柄コード'].unique())

    codes = df_stocklist['銘柄コード'].unique()

    sc = StooqCrawler()
    for code in codes:
        if code < 2815:
            continue
        sc.run(
            code=code,
            callback=Callback()
        )


if __name__ == '__main__':
    main()
