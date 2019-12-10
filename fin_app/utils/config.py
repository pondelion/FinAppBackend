import os

import yaml

from .logger import Logger

DEFAULT_AWS_FILEPATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..',
    'config/aws.yml'
)
DEFAULT_TWITTER_FILEPATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..',
    'config/twitter.yml'
)


def _load_aws_config(filepath: str = DEFAULT_AWS_FILEPATH):
    return yaml.safe_load(open(filepath))


def _load_twitter_config(filepath: str = DEFAULT_TWITTER_FILEPATH):
    return yaml.safe_load(open(filepath))


class _AWSConfig(type):
    config = _load_aws_config()

    def __getattr__(cls, key: str):
        try:
            return cls.config[key]
        except Exception as e:
            Logger.e(__class__, f'No config value found for {key}')
            raise e


class _TwitterConfig(type):
    config = _load_twitter_config()

    def __getattr__(cls, key: str):
        try:
            return cls.config[key]
        except Exception as e:
            Logger.e(__class__, f'No config value found for {key}')
            raise e


class AWSConfig(metaclass=_AWSConfig):
    pass


class TwitterConfig(metaclass=_TwitterConfig):
    pass


TABLE_NAME_MAPPING = {
    'dynamodb': {
        'twitter': 'finapp_twitter_tweet'
    }
}