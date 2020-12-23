import sys
import time
from datetime import datetime

import schedule

sys.path.append('../..')
from fin_app.crawler import GoogleTrendsCrawler
from fin_app.database.nosql.dynamodb import DynamoDB
from fin_app.utils.config import AWSConfig, DataLocationConfig
from fin_app.utils.logger import Logger


TAG = 'google_trend_crawl'


class Callback(GoogleTrendsCrawler.Callback):

    def on_finished(self, data, args):

        json_data_list = [
            {
                'keyword': keyword,
                'date': args['datetime'].strftime('%Y-%m-%d'),
                'datetime': args['datetime'].strftime('%Y-%m-%d %H:%M:%S')
            }
            for keyword in data[0].tolist()
        ]

        Logger.d(TAG, f'on_finished : len(data) : {len(json_data_list)}')
        DynamoDB.put_items(
            AWSConfig.DYNAMODB_GOOGLE_TREND_NAME,
            json_data_list,
        )

    def on_failed(self, e, args):
        Logger.e(TAG, f'on_failed : {e}')


def main():

    def job():
        trc = GoogleTrendsCrawler()
        trc.run(callback=Callback())
        time.sleep(30)

    schedule.every(30).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
