import boto3

from ..utils.config import AWSConfig

_aws_session = boto3.session.Session(
    region_name=AWSConfig.REGION_NAME,
    aws_access_key_id=AWSConfig.ACCESS_KEY_ID,
    aws_secret_access_key=AWSConfig.SECRET_ACCESS_KEY,
)

dynamodb = _aws_session.resource('dynamodb')
