import sys
sys.path.append('../..')
import os
from datetime import datetime, timedelta

import pandas as pd

from fin_app.utils.config import DataLocationConfig
from fin_app.utils.logger import Logger
from fin_app.data_processing.stockprice.candle_chart import creaet_candle_chart
from fin_app.storage import S3


TAG = 'create_candle_dataset'


def main():
    df_stocklist = pd.read_csv(
        DataLocationConfig.STOCKLIST_FILE
    )

    Logger.d(TAG, df_stocklist['銘柄コード'].unique())

    codes = df_stocklist['銘柄コード'].unique()

    STOCKPRICE_FILEPATH_FMT = 's3://fin-app/stockprice_concat/{code}.csv'

    STRIDE_DAYS = 30
    WINDOW_DAYS = 30*4
    STRIDE_D_TD = timedelta(days=STRIDE_DAYS)
    WINDOW_D_TD = timedelta(days=WINDOW_DAYS)

    WIDTH = 0.5

    S3_CANDLECHART_FILEPATH_FMT = os.path.join(
        DataLocationConfig.STOCKPRICE_CANDLECHART_BASEDIR.replace('s3://fin-app/', ''),
        f'DAILY_WINDOW-{WINDOW_DAYS}d_STRIDE-{STRIDE_DAYS}d_WIDTH-{WIDTH}',
        '{code}',
        '{start_dt}_{end_dt}.png'
    )
    LOCAL_CANDLECHART_FILEPATH_FMT = os.path.join(
        '/tmp',
        f'WINDOW-{WINDOW_DAYS}d_STRIDE-{STRIDE_DAYS}d',
        '{code}',
        '{start_dt}_{end_dt}.png'
    )

    for code in codes[2:]:
        # if code < 1515:
        #     continue
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
        MIN_DT = df.index.min()
        MAX_DT = df.index.max()

        start_dt = MIN_DT
        end_dt = MIN_DT + WINDOW_D_TD

        try:
            while end_dt <= MAX_DT:
                start_dt_str = start_dt.strftime('%Y-%m-%d')
                end_dt_str = end_dt.strftime('%Y-%m-%d')

                df_sliced = df[start_dt_str:end_dt_str]

                s3_filepath = S3_CANDLECHART_FILEPATH_FMT.format(
                    code=code,
                    start_dt=start_dt_str,
                    end_dt=end_dt_str,
                )
                local_filepath = LOCAL_CANDLECHART_FILEPATH_FMT.format(
                    code=code,
                    start_dt=start_dt_str,
                    end_dt=end_dt_str
                )
                if not os.path.exists(os.path.dirname(local_filepath)):
                    os.makedirs(os.path.dirname(local_filepath))

                local_filepath = creaet_candle_chart(
                    opens=df_sliced.open,
                    closes=df_sliced.close,
                    highs=df_sliced.high,
                    lows=df_sliced.low,
                    width=WIDTH,
                    filepath=local_filepath
                )

                S3.save_file(
                    local_filepath=local_filepath,
                    s3_filepath=s3_filepath,
                )

                Logger.i(TAG, f'Saved candle chart image to {s3_filepath}')

                os.remove(local_filepath)

                start_dt += STRIDE_D_TD
                end_dt += STRIDE_D_TD
        except Exception as e:
            Logger.e(TAG, f'{e}')
            continue


if __name__ == '__main__':
    main()
