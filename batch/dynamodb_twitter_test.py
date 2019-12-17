import sys
sys.path.append('..')
from datetime import datetime as dt

from fin_app.database.nosql.dynamodb import DynamoDB


def main():
    res = DynamoDB.partitionkey_query(
        table_name='finapp_twitter_tweet',
        partition_key_name='keyword',
        partition_key='ロジザード',
    )
    print([dt.fromtimestamp(r['created_at']) for r in res])


if __name__ == '__main__':
    main()
