from .base_storage import BaseStorage
from ..aws.resource_provider import S3 as S3_resouce
from ..utils.config import AWSConfig


class S3(BaseStorage):

    @staticmethod
    def upload_file(
        local_filepath: str,
        s3_filepath: str,
        bucket_name: str = AWSConfig.S3_BUCKET_NAME,
    ):
        bucket = S3_resouce.Bucket(bucket_name)

        bucket.upload_file(
            local_filepath,
            s3_filepath
        )
