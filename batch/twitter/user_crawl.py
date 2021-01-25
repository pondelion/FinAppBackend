import os
import sys
sys.path.append('../..')
from datetime import datetime
import time

import urllib
import schedule

from fin_app.crawler.twitter.singleshot.tweepy_user_crawler import UserCrawler
from fin_app.database.nosql.dynamodb import DynamoDB
from fin_app.storage.s3 import S3
from fin_app.utils.config import AWSConfig, DataLocationConfig
from fin_app.utils.dynamodb import format_data
from fin_app.utils.logger import Logger


TAG = 'twitter_user_crawl'


class Callback(UserCrawler.Callback):

    def on_finished(self, data, args):
        Logger.d(TAG, 'on_finished')
        print(args)
        print(f'len(data) : {len(data)}')

        items = [format_data(item._json) for item in data]
        [item.update({'screen_name': args["screen_name"]}) for item in items]
        for item, d in zip(items, data):
            item['created_at'] = int(d.created_at.timestamp())
            item['id'] = d.id
            if 'media' in item['entities']:
                try:
                    s3_media_urls = []
                    medias = item['entities']['media']
                    for media in medias:
                        media_url = media['media_url']
                        filename = media_url.split("/")[-1]
                        local_tmp_filepath = f'/tmp/{filename}'
                        urllib.request.urlretrieve(
                            media_url,
                            local_tmp_filepath
                        )
                        s3_filepath = os.path.join(
                            DataLocationConfig.TWITTER_MEDIAFILE_DIR,
                            args["screen_name"],
                            filename
                        )
                        S3.save_file(local_tmp_filepath, s3_filepath, 'i-app')
                        os.remove(local_tmp_filepath)
                        Logger.d(TAG, f'Uploaded media file to {s3_filepath}')
                        s3_media_urls.append(s3_filepath)
                    item['s3_media_urls'] = s3_media_urls
                except Exception as e:
                    print(e)

        DynamoDB.put_items(
            AWSConfig.DYNAMODB_TWITTER_USER_TWEET_TABLE_NAME,
            items,
        )

    def on_failed(self, e, args):
        Logger.e(TAG, f'on_failed : {e} : {args}')


def main():
    uc = UserCrawler()

    uc.run(
        screen_name='realDonaldTrump',
        count_per_page=200,
        n_pages=20,
        callback=Callback()
    )

    # schedule.every(2).minutes.do(
    #     lambda: uc.run(
    #         screen_name='realDonaldTrump',
    #         count_per_page=200,
    #         n_pages=3,
    #         callback=Callback()
    #     )
    # )

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


if __name__ == '__main__':
    main()
