import sys
sys.path.append('../..')
import os
from datetime import datetime, timedelta

import pandas as pd
from tqdm import tqdm

from fin_app.utils.config import DataLocationConfig
from fin_app.utils.logger import Logger
from fin_app.data_processing.stockprice.candle_chart import creaet_candle_chart
from fin_app.storage import S3


TAG = 'create_candle_metadata'


def main():

    df_stocklist = pd.read_csv(
        DataLocationConfig.STOCKLIST_FILE
    )

    Logger.d(TAG, df_stocklist['銘柄コード'].unique())

    codes = df_stocklist['銘柄コード'].unique()

    STOCKPRICE_FILEPATH_FMT = 's3://fin-app/stockprice_concat/{code}.csv'

    METADATA_LOCAL_FILEPATH = '/tmp/DAILY_WINDOW-120d_STRIDE-30d_WIDTH-0.5_stockprice_metadata.csv'
    METADATA_S3_FILEPATH = os.path.join(
        DataLocationConfig.STOCKPRICE_CANDLECHART_BASEDIR.replace('s3://fin-app/', ''),
        f'metadata/DAILY_WINDOW-120d_STRIDE-30d_WIDTH-0.5/stockprice_metadata.csv'
    )

    s3_filepath_list = []
    start_dt_str_list = []
    end_dt_str_list = []
    code_list = []
    change_rate_list = []
    for code in tqdm(codes[:]):
        Logger.i(TAG, code)
        files = S3.get_filelist(
            basedir=os.path.join(
                DataLocationConfig.STOCKPRICE_CANDLECHART_BASEDIR.replace('s3://fin-app/', ''),
                # 'DAILY_WINDOW-120d_STRIDE-30d_WIDTH-0.5/1301'
                f'DAILY_WINDOW-120d_STRIDE-30d_WIDTH-0.5/{code}'
            )
        )
        start_dt_str = [file.split('/')[-1].replace('.png', '').split('_')[0] for file in files]
        end_dt_str = [file.split('/')[-1].replace('.png', '').split('_')[1] for file in files]

        s3_filepath_list += files
        start_dt_str_list += start_dt_str
        end_dt_str_list += end_dt_str
        code_list += [code]*len(files)

        Logger.i(TAG, f'len(files) : {len(files)}')
        Logger.i(TAG, f'len(s3_filepath_list) : {len(s3_filepath_list)}')

        try:
            df = pd.read_csv(
                STOCKPRICE_FILEPATH_FMT.format(code=code)
            )
        except Exception as e:
            Logger.e(TAG, f'failed to load csv file from s3 : {e}')
            change_rate_list += [None]*len(files)
            continue

        df['日付'] = pd.to_datetime(df['日付'])
        df = df.set_index('日付')
        df = df.rename(columns={
            '始値': 'open',
            '高値': 'high',
            '安値': 'low',
            '終値': 'close'
        })
        MAX_DT = df.index.max()

        for sds, eds in zip(start_dt_str, end_dt_str):
            if len(df[sds:eds]) == 0:
                change_rate_list.append(None)
                continue

            edt = datetime.strptime(eds, '%Y-%m-%d')
            for i in range(119):
                try:
                    df.loc[edt]
                    break
                except Exception:
                    edt -= timedelta(days=1)
                    continue
                #raise Exception('')
            change_rate_start_dt = edt + timedelta(days=1)
            change_rate_end_dt = change_rate_start_dt + timedelta(days=30)
            if change_rate_end_dt > MAX_DT or len(df[change_rate_start_dt:change_rate_end_dt]) == 0:
                change_rate_list.append(None)
                continue

            change_rate = \
                (df[change_rate_start_dt:change_rate_end_dt]['close'] - df.loc[edt]['close']).mean() /  \
                df.loc[edt]['close']
            change_rate_list.append(change_rate)

        if code % 10 == 0:
            df_meta = pd.DataFrame({
                's3_filepath': s3_filepath_list,
                'code': code_list,
                'start_dt': start_dt_str_list,
                'end_dt': end_dt_str_list,
                'change_rate_30d': change_rate_list,
            })
            df_meta.to_csv(
                METADATA_LOCAL_FILEPATH,
                index=None
            )
            Logger.i(TAG, f'len(df_meta) : {len(df_meta)}')

    df_meta = pd.DataFrame({
        's3_filepath': s3_filepath_list,
        'code': code_list,
        'start_dt': start_dt_str_list,
        'end_dt': end_dt_str_list,
        'change_rate_30d': change_rate_list,
    })
    df_meta.to_csv(
        METADATA_LOCAL_FILEPATH,
        index=None
    )

    S3.save_file(
        local_filepath=METADATA_LOCAL_FILEPATH,
        s3_filepath=METADATA_S3_FILEPATH,
    )


if __name__ == '__main__':
    main()
