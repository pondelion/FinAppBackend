import sys
sys.path.append('../..')
from argparse import ArgumentParser
from datetime import datetime, date, timedelta
import os
import time

import requests

from fin_app.crawler import CompanyAnnouncementCrawler
from fin_app.database.nosql.dynamodb import DynamoDB
from fin_app.utils.config import AWSConfig
from fin_app.utils.config import DataLocationConfig
from fin_app.utils.logger import Logger
from fin_app.storage import S3


def download_pdf_to_S3(
    pdf_url: str,
    pubdate: str,
) -> str:
    s3_dest_filepath = os.path.join(
        DataLocationConfig.COMPANY_ANNOUNCEMENT_PDF_DIR,
        pubdate,
        pdf_url.split('/')[-1],
    )
    local_tmp_filepath = os.path.join(
        '/tmp',
        'securities_report.pdf'
    )
    res = requests.get(pdf_url)
    if res.status_code != 200:
        print(f'status_code = {res.status_code} : {pdf_url}, skip downloading.')
        return None
    with open(local_tmp_filepath, 'wb') as f:
        f.write(res.content)

    S3.save_file(
        local_filepath=local_tmp_filepath,
        s3_filepath=s3_dest_filepath,
    )
    print(f'saved to {s3_dest_filepath}')
    time.sleep(0.1)
    return s3_dest_filepath


class Callback(CompanyAnnouncementCrawler.Callback):

    def on_finished(self, data, args):
        Logger.i('company_announcement_crawl : on_finished', f'{args["start_dt"]} : {args["end_dt"]}')
        Logger.i('company_announcement_crawl : on_finished', len(data))

        [download_pdf_to_S3(d['document_url'], d['pubdate'].split(' ')[0].replace('-', '')) for d in data]
        print('='*100)

    def on_failed(self, e, args):
        Logger.i('company_announcement_crawl : on_failed', f'{args["start_dt"]} : {args["end_dt"]}')
        Logger.i('company_announcement_crawl : on_failed', e)
        print('='*100)


def main():

    cac = CompanyAnnouncementCrawler()

    # start_dt = date(2010, 2, 3)
    # end_dt = date(2019, 12, 17)
    start_dt = date(2019, 12, 18)
    end_dt = date(2021, 4, 10)

    for i in range((end_dt - start_dt).days + 1):
        dt = end_dt - timedelta(i)
        cac.run(
            start_dt=dt,
            end_dt=dt,
            callback=Callback(),
        )


if __name__ == '__main__':
    main()
