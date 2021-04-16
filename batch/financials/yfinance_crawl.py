import sys
sys.path.append('../..')
import os
from typing import Dict

import pandas as pd

from fin_app.crawler.company_financials.yfinance import (
    FinancialsCrawler,
    BalanceSheetCrawler,
    CashflowCrawler,
)
from fin_app.utils.config import DataLocationConfig
from fin_app.utils.logger import Logger


TAG = 'yfinance financials crawl'


class FinancialsCallback(FinancialsCrawler.Callback):

    def on_finished(
        self,
        data: pd.DataFrame,
        args: Dict,
    ) -> None:

        filepath = os.path.join(
            DataLocationConfig.FINANCIALS_YFINANCE_BASEDIR,
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


class BalanceSheetCallback(BalanceSheetCrawler.Callback):

    def on_finished(
        self,
        data: pd.DataFrame,
        args: Dict,
    ) -> None:

        filepath = os.path.join(
            DataLocationConfig.BALANCE_SHEET_YFINANCE_BASEDIR,
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


class CashflowCallback(CashflowCrawler.Callback):

    def on_finished(
        self,
        data: pd.DataFrame,
        args: Dict,
    ) -> None:

        filepath = os.path.join(
            DataLocationConfig.CASHFLOW_YFINANCE_BASEDIR,
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

    fc = FinancialsCrawler()
    bsc = BalanceSheetCrawler()
    cfc = CashflowCrawler()
    for code in codes:
        fc.run(
            code=code,
            callback=FinancialsCallback()
        )
        bsc.run(
            code=code,
            callback=BalanceSheetCallback()
        )
        cfc.run(
            code=code,
            callback=CashflowCallback()
        )


if __name__ == '__main__':
    main()
