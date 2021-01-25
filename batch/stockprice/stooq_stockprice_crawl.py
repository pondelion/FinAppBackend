import sys
sys.path.append('../..')
import os
import time
from typing import Dict

import pandas as pd

from fin_app.crawler import StooqCrawler
from fin_app.utils.config import DataLocationConfig
from fin_app.utils.logger import Logger


TAG = 'stooq_crawl'
g_fail_cnt = 0
g_last_success_code = 6926
g_reached_end = False
MAX_FAIL_CNT = 40


class Callback(StooqCrawler.Callback):

    def on_finished(
        self,
        data: pd.DataFrame,
        args: Dict,
    ) -> None:

        filepath = os.path.join(
            DataLocationConfig.STOCKPRICE_STOOQ_CONCAT_BASEDIR,
            f'{args["code"]}.csv'
        )
        data.to_csv(filepath)
        Logger.d(TAG, f'Saved data to {filepath}')
        global g_last_success_code
        global g_fail_cnt
        g_last_success_code = args["code"]
        g_fail_cnt = 0

    def on_failed(
        self,
        e: Exception,
        args: Dict,
    ) -> None:
        Logger.d(TAG, f'on_failed : {args["code"]} : {e}')
        global g_fail_cnt
        g_fail_cnt += 1


def crawl(crawler, codes, start_code):

    for code in codes:
        if code < start_code:
            continue
        crawler.run(
            code=code,
            callback=Callback()
        )
        time.sleep(20)
        if code == max(codes):
            global g_reached_end
            g_reached_end = True
        
        global g_fail_cnt
        if g_fail_cnt >= MAX_FAIL_CNT:
            Logger.d(TAG, 'stooq restriction detected, waiting until unrestriction.')
            while crawler.check_restriction() is False:
                time.sleep(60*60)
            g_fail_cnt = 0
            return


def main():
    df_stocklist = pd.read_csv(
        DataLocationConfig.STOCKLIST_FILE
    )

    Logger.d(TAG, df_stocklist['銘柄コード'].unique())

    codes = df_stocklist['銘柄コード'].unique()

    sc = StooqCrawler()

    while sc.check_restriction() is False:
        Logger.d(TAG, 'stooq restriction detected, waiting 1hour')
        time.sleep(60*60)

    global g_reached_end
    while g_reached_end == False:
        global g_last_success_code
        crawl(sc, codes, g_last_success_code+1)


if __name__ == '__main__':
    main()
