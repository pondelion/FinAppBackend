import sys
sys.path.append('..')
from argparse import ArgumentParser

from fin_app.crawler.twitter.singleshot.keyword_crawler import KeywordCrawler
from fin_app.database.nosql.dynamodb import DynamoDB
from fin_app.utils.config import AWSConfig
from fin_app.utils.dynamodb import empty2null


class Callback(KeywordCrawler.Callback):

    def on_finished(self, keyword, data):
        print('on_finished')
        print(keyword)
        print(len(data))
        # print(data[1].text)
        print('='*100)
        items = [empty2null(item._json) for item in data]
        [item.update({'keyword': keyword}) for item in items]
        for item, d in zip(items, data):
            item['created_at'] = int(d.created_at.timestamp())
        DynamoDB.put_items(
            AWSConfig.DYNAMODB_TWITTER_TEST_TABLE_NAME,
            items,
        )

    def on_failed(self, keyword, e):
        print('on_failed')
        print(keyword)
        print(e)
        print('='*100)


def main():
    kc = KeywordCrawler()
    kc.run(
        keywords=['test', '寒い'],
        count=2,
        callback=Callback()
    )


if __name__ == '__main__':
    main()
