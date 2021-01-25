import sys
sys.path.append('../..')
import os
import time

import pandas as pd
import numpy as np
import requests

from fin_app.utils.config import DataLocationConfig
from fin_app.utils.logger import Logger
from fin_app.storage import S3


def download_pdf_to_S3(
    pdf_url: str,
    filer_name: str,
    sub_datetime: str,
    doc_description: str,
) -> str:
    s3_dest_filepath = os.path.join(
        DataLocationConfig.EDINET_SECURITIES_REPORT_PDF_DIR,
        filer_name,
        # f'{pd.to_datetime(sub_datetime).strftime("%Y%m%d_%H%M")}.pdf'
        f'{doc_description}_{pd.to_datetime(sub_datetime).strftime("%Y%m%d")}.pdf'
    )
    local_tmp_filepath = os.path.join(
        '/tmp',
        'securities_report.pdf'
    )
    res = requests.get(pdf_url)
    with open(local_tmp_filepath, 'wb') as f:
        f.write(res.content)

    S3.save_file(
        local_filepath=local_tmp_filepath,
        s3_filepath=s3_dest_filepath,
    )
    print(f'saved to {s3_dest_filepath}')
    time.sleep(0.1)
    return s3_dest_filepath


def main():
    start_dt = '2016-01-24'
    end_dt = '2020-12-23'

    for dt in pd.date_range(start_dt, end_dt)[::-1]:
        print(dt)
        docinfo_filepath = os.path.join(
            DataLocationConfig.EDINET_SECURITIES_REPORT_DOCINFO_DIR,
            f'{dt.strftime("%Y_%m_%d")}.csv'
        )
        try:
            print(docinfo_filepath)
            df_docinfo = pd.read_csv(docinfo_filepath)
            print(len(df_docinfo))
            if len(df_docinfo) == 0:
                continue
            if 's3_url' not in df_docinfo.columns:
                df_docinfo['s3_url'] = np.nan
            # filt = df_docinfo['doc_descriptions'].str.contains('有価証券報告書', na=False)
            filt = df_docinfo['doc_descriptions'].str.contains('四半期', na=False)
            filt = filt & (~df_docinfo['doc_descriptions'].str.contains('内国', na=False))
            filt = filt & (~df_docinfo['doc_descriptions'].str.contains('外国', na=False))
            filt = filt & (~df_docinfo['s3_url'].map(lambda x: str(x).startswith('s3')))
            if filt.sum() == 0:
                continue
            df_docinfo.loc[filt, 's3_url'] = df_docinfo.loc[filt].apply(
                lambda x: download_pdf_to_S3(
                    x['pdf_urls'],
                    x['filer_names'],
                    x['submit_datetimes'],
                    x['doc_descriptions']
                ),
                axis=1
            )
            df_docinfo.to_csv(docinfo_filepath, index=False)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()