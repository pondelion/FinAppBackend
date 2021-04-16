import sys
sys.path.append('../..')
from argparse import ArgumentParser
from datetime import datetime, date, timedelta

from fin_app.crawler import CompanyAnnouncementCrawler
from fin_app.database.nosql.dynamodb import DynamoDB
from fin_app.utils.config import AWSConfig
from fin_app.utils.logger import Logger


class Callback(CompanyAnnouncementCrawler.Callback):

    def on_finished(self, data, args):
        Logger.i('company_announcement_crawl : on_finished', f'{args["start_dt"]} : {args["end_dt"]}')
        Logger.i('company_announcement_crawl : on_finished', len(data))

        [d.update({'company_code': int(d['company_code'])}) for d in data]

        DynamoDB.put_items(
            AWSConfig.DYNAMODB_COMPANY_ANNOUNCEMENT_TABLE_NAME,
            data,
        )
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
    end_dt = date(2021, 4, 9)

    for i in range((end_dt - start_dt).days + 1):
        dt = end_dt - timedelta(i)
        cac.run(
            start_dt=dt,
            end_dt=dt,
            callback=Callback(),
        )


if __name__ == '__main__':
    main()
