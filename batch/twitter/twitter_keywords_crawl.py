import sys
sys.path.append('../..')
from argparse import ArgumentParser
import random
from datetime import datetime

import pandas as pd

from fin_app.crawler.twitter.singleshot.tweepy_keyword_crawler import KeywordCrawler
from fin_app.database.nosql.dynamodb import DynamoDB
from fin_app.utils.config import AWSConfig, DataLocationConfig
from fin_app.utils.dynamodb import format_data


class Callback(KeywordCrawler.Callback):

    def on_finished(self, data, args):
        print('on_finished')
        print(args["keyword"])
        print(len(data))

        print('='*100)
        items = [format_data(item._json) for item in data]
        [item.update({'keyword': args["keyword"]}) for item in items]
        for item, d in zip(items, data):
            item['created_at'] = int(d.created_at.timestamp())
        DynamoDB.put_items(
            AWSConfig.DYNAMODB_TWITTER_TABLE_NAME,
            items,
        )

    def on_failed(self, e, args):
        print('on_failed')
        print(args["keyword"])
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
    stocklist = list(df_stocklist['銘柄名'])
    stocklist = random.sample(stocklist, len(stocklist))
    kc.run(
        keywords=stocklist,
        count=300,
        lang='ja',
        callback=Callback(),
        parallel=False,
    )


if __name__ == '__main__':
    main()
