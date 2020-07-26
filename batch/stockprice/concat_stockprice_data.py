import sys
sys.path.append('../..')
from functools import reduce
import os

import pandas as pd

from fin_app.utils.config import DataLocationConfig
from fin_app.utils.logger import Logger
from fin_app.data_processing.stockprice.stop_high_low import check_stop_high_low


CALC_STOP_HIGH_LOW = True


def main():
    years = range(1983, 2020+1)
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
                #print(f'failed to load data {filepath}')
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

        if CALC_STOP_HIGH_LOW:
            df_concat['日付'] = pd.to_datetime(df_concat['日付'])
            df_concat.set_index('日付', inplace=True)
            df_concat.sort_index(inplace=True)
            df_concat['last_close'] = df_concat['終値'].shift(1)
            df_concat['stop_high_low'] = df_concat.apply(
                lambda x: check_stop_high_low(
                    x['last_close'],
                    x['高値'],
                    x['安値']
                ),
                axis=1
            )
        # print(df_concat.head())
        # print(df_concat.tail())

        filepath = os.path.join(
            DataLocationConfig.STOCKPRICE_CONCAT_BASEDIR,
            f'{code}.csv'
        )
        df_concat.to_csv(
            filepath,
            #index=None
        )
        Logger.i('concat_stockprice_data', f'Saved concat data to {filepath}')
        print('='*80)


if __name__ == '__main__':
    main()
