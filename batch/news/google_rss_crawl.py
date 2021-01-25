import sys
import time
from datetime import datetime

import schedule

sys.path.append('../..')
from fin_app.crawler.news.google import Topic, TopicRSSCrawler
from fin_app.database.nosql.dynamodb import DynamoDB
from fin_app.utils.config import AWSConfig, DataLocationConfig
from fin_app.utils.logger import Logger


TAG = 'twitter_trend_crawl'


class Callback(TopicRSSCrawler.Callback):

    def on_finished(self, data, args):
        Logger.d(TAG, f'on_finished : {args["topic"]}')

        Logger.d(TAG, '='*100)
        for d in data:
            d['published_date'] = datetime(*d['published_parsed'][:6]).strftime("%Y-%m-%d")
            del d['published_parsed']
            d['topic'] = args['topic']

        print(f'len(data) : {len(data)}')
        DynamoDB.put_items(
            AWSConfig.DYNAMODB_GOOGLE_RSS_NEWS_TABLE_NAME,
            data,
        )

    def on_failed(self, e, args):
        Logger.e(TAG, f'on_failed : {args["topic"]} : {e}')
        Logger.e(TAG, '='*100)


def main():

    topics = (
        Topic.BUSSINESS,
        Topic.POLICTICS,
        Topic.WORLD,
        Topic.NATION,
        Topic.TECHNOLOGY,
        Topic.SPORTS,
        Topic.ENTERTAINMENT,
    )

    def job():
        for topic in topics:
            trc = TopicRSSCrawler()
            trc.run(callback=Callback(), topic=topic)
            time.sleep(30)

    schedule.every(30).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
