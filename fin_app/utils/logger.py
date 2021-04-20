import logging
from datetime import datetime
import os

import yaml


formatter = '%(levelname)s : %(asctime)s : %(message)s'
logging.basicConfig(format=formatter)

# DEFAULT_DEV_FILEPATH = os.path.join(
#     os.path.dirname(os.path.abspath(__file__)),
#     '..',
#     'config/dev.yml'
# )
# dev_conf = yaml.safe_load(open(DEFAULT_DEV_FILEPATH))
filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..',
    'log',
    f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
)
file_handler = logging.FileHandler(
    filename=filename
)
file_handler.setFormatter(logging.Formatter(formatter))


class Logger:
    logger = logging.getLogger('fin_app')
    if 'LAMBDA' not in os.environ:
        logger.addHandler(file_handler)

    @staticmethod
    def d(tag: str, message: str):
        """debug log"""
        Logger.logger.setLevel(logging.DEBUG)
        Logger.logger.debug('[%s] %s', tag, message)

    @staticmethod
    def i(tag: str, message: str):
        """infomation log"""
        Logger.logger.setLevel(logging.INFO)
        Logger.logger.info('[%s] %s', tag, message)

    @staticmethod
    def e(tag: str, message: str):
        """error log"""
        Logger.logger.setLevel(logging.ERROR)
        Logger.logger.error('[%s] %s', tag, message)

    @staticmethod
    def w(tag: str, message: str):
        """warning log"""
        Logger.logger.setLevel(logging.WARNING)
        Logger.logger.warn('[%s] %s', tag, message)
