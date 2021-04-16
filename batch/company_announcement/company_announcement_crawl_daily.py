import sys
sys.path.append('../..')
from argparse import ArgumentParser
from datetime import datetime, date, timedelta
import os
import time

import requests
import schedule

from fin_app.crawler import CompanyAnnouncementCrawler
from fin_app.database.nosql.dynamodb import DynamoDB
from fin_app.utils.config import AWSConfig
from fin_app.utils.config import DataLocationConfig
from fin_app.utils.logger import Logger
from fin_app.storage import S3


g_data = []


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
    return s3_dest_filepath


class Callback14(CompanyAnnouncementCrawler.Callback):

    def on_finished(self, data, args):
        Logger.i('company_announcement_crawl : on_finished', f'{args["start_dt"]} : {args["end_dt"]}')
        Logger.i('company_announcement_crawl : on_finished', len(data))

        [d.update({'company_code': int(d['company_code'])}) for d in data]

        DynamoDB.put_items(
            AWSConfig.DYNAMODB_COMPANY_ANNOUNCEMENT_TABLE_NAME,
            data,
        )
        [download_pdf_to_S3(d['document_url'], d['pubdate'].split(' ')[0].replace('-', '')) for d in data]
        global g_data
        g_data = data
        print('='*100)

    def on_failed(self, e, args):
        Logger.i('company_announcement_crawl : on_failed', f'{args["start_dt"]} : {args["end_dt"]}')
        Logger.i('company_announcement_crawl : on_failed', e)
        print('='*100)


class Callback00(CompanyAnnouncementCrawler.Callback):

    def on_finished(self, data, args):
        Logger.i('company_announcement_crawl : on_finished', f'{args["start_dt"]} : {args["end_dt"]}')
        Logger.i('company_announcement_crawl : on_finished', len(data))

        [d.update({'company_code': int(d['company_code'])}) for d in data]

        global g_data
        ids = [d['id'] for d in g_data]
        filtered_data = list(filter(lambda x: x['id'] not in ids, data))

        Logger.i('company_announcement_crawl : on_finished, filtered_data len => ', len(filtered_data))
        DynamoDB.put_items(
            AWSConfig.DYNAMODB_COMPANY_ANNOUNCEMENT_TABLE_NAME,
            filtered_data,
        )
        [download_pdf_to_S3(d['document_url'], d['pubdate'].split(' ')[0].replace('-', '')) for d in filtered_data]
        
        g_data = []
        print('='*100)

    def on_failed(self, e, args):
        Logger.i('company_announcement_crawl : on_failed', f'{args["start_dt"]} : {args["end_dt"]}')
        Logger.i('company_announcement_crawl : on_failed', e)
        print('='*100)


def job00():
    cac = CompanyAnnouncementCrawler()
    dt = date.today() - timedelta(days=1)
    cac.run(
        start_dt=dt,
        end_dt=dt,
        callback=Callback00(),
    )


def job14():
    cac = CompanyAnnouncementCrawler()
    dt = date.today()
    cac.run(
        start_dt=dt,
        end_dt=dt,
        callback=Callback14(),
    )


def main():
    schedule.every().day.at('00:01').do(job00)
    schedule.every().day.at('14:00').do(job14)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
