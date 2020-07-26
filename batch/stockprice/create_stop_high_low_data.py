import sys
sys.path.append('../..')
import os

import pandas as pd

from fin_app.utils.config import DataLocationConfig
from fin_app.utils.logger import Logger
from fin_app.storage import S3
from fin_app.data_processing.stockprice.stop_high_low import check_stop_high_low


TAG = 'create_stop_high_low_data'


def main():
    df_stocklist = pd.read_csv(
        DataLocationConfig.STOCKLIST_FILE
    )

    Logger.d(TAG, df_stocklist['銘柄コード'].unique())

    codes = df_stocklist['銘柄コード'].unique()

    STOCKPRICE_FILEPATH_FMT = 's3://fin-app/stockprice_concat/{code}.csv'

    for code in codes[100:101]:
        code = 1382
        try:
            df = pd.read_csv(
                STOCKPRICE_FILEPATH_FMT.format(code=code)
            )
        except Exception as e:
            Logger.e(TAG, f'failed to load csv file from s3 : {e}')
            continue
        df['日付'] = pd.to_datetime(df['日付'])
        df = df.set_index('日付')
        df = df.rename(columns={
            '始値': 'open',
            '高値': 'high',
            '安値': 'low',
            '終値': 'close'
        })
        df.sort_index(inplace=True)

        df['last_close'] = df['close'].shift(1)
        df.dropna(inplace=True)

        print(df.tail())

        df['stop_high_low'] = df.apply(lambda x: check_stop_high_low(
            x['last_close'],
            x['high'],
            x['low']
        ), axis=1)
        print(df[df['stop_high_low']==1])


if __name__ == '__main__':
    main()
