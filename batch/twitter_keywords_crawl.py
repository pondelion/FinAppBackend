import sys
sys.path.append('..')
from argparse import ArgumentParser

import pandas as pd

from fin_app.crawler.twitter.singleshot.keyword_crawler import KeywordCrawler
from fin_app.database.nosql.dynamodb import DynamoDB
from fin_app.utils.config import AWSConfig, DataLocationConfig
from fin_app.utils.dynamodb import format_data


class Callback(KeywordCrawler.Callback):

    def on_finished(self, keyword, data):
        print('on_finished')
        print(keyword)
        print(len(data))
        print('='*100)
        items = [format_data(item._json) for item in data]
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
    df_stocklist = pd.read_csv(
        DataLocationConfig.STOCKLIST_FILE
    )
    df_stocklist['銘柄名'] = df_stocklist['銘柄名'].map(lambda x: x.replace('(株)', ''))
    print(df_stocklist.head())
    print(len(df_stocklist))
    kc = KeywordCrawler()
    kc.run(
        keywords=list(df_stocklist['銘柄名']),
        count=300,
        callback=Callback(),
        parallel=False,
    )


if __name__ == '__main__':
    main()
