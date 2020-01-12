import sys
sys.path.append('../..')
from datetime import datetime
import time

import schedule

from fin_app.crawler.twitter.singleshot.trend_crawler import TrendCrawler
from fin_app.database.nosql.dynamodb import DynamoDB
from fin_app.utils.config import AWSConfig, DataLocationConfig
from fin_app.utils.logger import Logger


TAG = 'twitter_trend_crawl'


class Callback(TrendCrawler.Callback):

    def on_finished(self, data, args):
        Logger.d(TAG, 'on_finished')

        Logger.d(TAG, '='*100)
        for d in data:
            d['datetime_keyword'] = d['datetime'].strftime('%Y%m%d_%H%M%S') + '_' + d['keyword']
            d['datetime'] = int(d['datetime'].timestamp())
            d['date'] = d['date'].strftime("%Y-%m-%d")

        DynamoDB.put_items(
            AWSConfig.DYNAMODB_TWITTER_TREND_TABLE_NAME,
            data,
        )

    def on_failed(self, e, args):
        Logger.e(TAG, f'on_failed : {e}')
        Logger.e(TAG, '='*100)


def main():
    tc = TrendCrawler()

    schedule.every(1).minutes.do(
        lambda: tc.run(callback=Callback())
    )

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
