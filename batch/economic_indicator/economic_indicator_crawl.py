import sys
sys.path.append('../..')
import os
from typing import Dict

import pandas as pd

from fin_app.crawler.economic_indicators import (
    CPICrawler,
    GDPCrawler,
    PPICrawler,
    IndustrialProductionCrawler,
    RetailSalesCrawler
)
from fin_app.crawler.economic_indicators.fred import FredCrawler
from fin_app.utils.config import DataLocationConfig
from fin_app.utils.logger import Logger


TAG = 'economic_indicator_crawl'


class Callback(FredCrawler.Callback):

    def on_finished(
        self,
        data: pd.DataFrame,
        args: Dict,
    ) -> None:
        print(args['tag'])
        print(data.head())
        filepath = os.path.join(
            DataLocationConfig.ECONOMIC_INDICATOR_BASEDIR,
            'ja',
            f'{args["name"]}.csv'
        )
        data.to_csv(
            filepath,
            index=None,
        )
        Logger.i(TAG, f'Saved data to {filepath}')

    def on_failed(
        self,
        e: Exception,
        args: Dict,
    ) -> None:
        print(f'on_failed : {args["tag"]} : {e}')


def main():

    crawlers = (
        CPICrawler(),
        GDPCrawler(),
        PPICrawler(),
        IndustrialProductionCrawler(),
        RetailSalesCrawler()
    )

    for c in crawlers:
        c.run(
            start_dt='2005-01-01',
            callback=Callback()
        )


if __name__ == '__main__':
    main()
