import os

from .utils.config import AWSConfig
from .utils.logger import Logger

try:
    os.environ["AWS_ACCESS_KEY_ID"] = AWSConfig.ACCESS_KEY_ID
except Exception as e:
    Logger.e('__init__', f'Failed to load config [AWSConfig.ACCESS_KEY_ID] : {e}')
try:
    os.environ["AWS_SECRET_ACCESS_KEY"] = AWSConfig.SECRET_ACCESS_KEY
except Exception as e:
    Logger.e('__init__', f'Failed to load config [AWSConfig.SECRET_ACCESS_KEY] : {e}')
