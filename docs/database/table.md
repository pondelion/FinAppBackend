
- twitter user master

| Attribute Name | Data Type | Data Length | Not NULL | PK/FK | Description |
| -------- | -------- | -------- | -------- | -------- | -------- |
| user_id |      |      | o | PK | |
| screen_name | string | | o | | |
| follower_count | unsigned int |  | o | | | 
| follow_count | unsigned int |  | o | | |
| joined_at | datetime | - | o | | Twitter加入日 |
| last_updated_at | datetime | - | | | DBレコードが最後に更新された日時 |


- twitter tweet

| Attribute Name | Data Type | Data Length | Not Null | PK/FK | Description |
| -------- | -------- | -------- | -------- | -------- | -------- |
| tweet_id |      |      | o | PK |
| user_id |      |      | o | FK | ユーザーID |
| tweeted_at | datetime |      | o || ツイート日時 |
| filepath | string | | o || ツイートテキストデータが格納されているファイルパス |
