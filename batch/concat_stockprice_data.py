import sys
sys.path.append('..')
from functools import reduce
import os

import pandas as pd

from fin_app.utils.config import DataLocationConfig


def main():
    years = range(1983, 2020)
    df_stocklist = pd.read_csv(
        DataLocationConfig.STOCKLIST_FILE
    )
    codes = df_stocklist['銘柄コード'].unique()

    for code in codes:
        df_list = []
        for year in years:
            try:
                filepath = os.path.join(
                    DataLocationConfig.STOCKPRICE_BASEDIR,
                    f'{year}/{code}.csv'
                )
                df_list.append(
                    pd.read_csv(filepath)
                )
            except Exception:
                pass

        if len(df_list) == 0:
            continue

        if len(df_list) == 1:
            df_concat = df_list[0]
        else:
            df_concat = reduce(
                lambda df1, df2: pd.concat([df1, df2], axis=0),
                df_list,
            )
        print(df_concat.head())
        print(df_concat.tail())
        filepath = os.path.join(
            DataLocationConfig.STOCKPRICE_CONCAT_BASEDIR,
            f'{code}.csv'
        )
        df_concat.to_csv(
            filepath,
            index=None
        )
        print(f'Saved concat data to {filepath}')
        print('='*80)


if __name__ == '__main__':
    main()
