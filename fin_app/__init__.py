import os
from .utils.config import AWSConfig


os.environ["AWS_ACCESS_KEY_ID"] = AWSConfig.ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"] = AWSConfig.SECRET_ACCESS_KEY
