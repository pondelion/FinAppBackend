import sys
sys.path.append('../..')
import os
import time
from typing import Dict

import pandas as pd

from fin_app.crawler import EdinetDocInfoCrawler
from fin_app.utils.config import DataLocationConfig
from fin_app.utils.logger import Logger


class Callback(EdinetDocInfoCrawler.Callback):

    def on_finished(
        self,
        data: pd.DataFrame,
        args: Dict,
    ) -> None:
        Logger.d('edinet_docinfo_crawl', f'{args["date"]} : {len(data)}')
        # print(data)
        filepath = os.path.join(
            DataLocationConfig.EDINET_SECURITIES_REPORT_DOCINFO_DIR,
            f'{args["date"].replace("-", "_")}.csv'
        )
        data.to_csv(filepath, index=False)
        
    def on_failed(
        self,
        e: Exception,
        args: Dict,
    ) -> None:
        Logger.d('edinet_docinfo_crawl', f'{args["date"]} : {e}')


def main():

    sc = EdinetDocInfoCrawler()

    sc.run(
        callback=Callback(),
        # start=pd.to_datetime('2021-01-20'),
        # end=pd.to_datetime('2021-01-23'),
    )


if __name__ == '__main__':
    main()
