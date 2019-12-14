import sys
sys.path.append('..')
import os
from typing import Dict

import pandas as pd

from fin_app.crawler import StockpriceCrawler
from fin_app.utils.config import DataLocationConfig


class Callback(StockpriceCrawler.Callback):

    def on_finished(
        self,
        data: pd.DataFrame,
        args: Dict,
    ) -> None:

        filepath = os.path.join(
            DataLocationConfig.STOCKPRICE_BASEDIR,
            f'{args["year"]}/{args["code"]}.csv'
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
        print(f'on_failed : {e}')


def main():
    df_stocklist = pd.read_csv(
        DataLocationConfig.STOCKLIST_FILE
    )

    print(df_stocklist['銘柄コード'].unique())

    years = range(1983, 2019)
    codes = df_stocklist['銘柄コード'].unique()

    for code in codes:
        for year in years:
            sc = StockpriceCrawler()
            sc.run(
                code=code,
                year=year,
                callback=Callback()
            )


if __name__ == '__main__':
    main()
