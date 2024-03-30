import boto3
from typing import Optional
from botocore.exceptions import ClientError

class S3Services:
    @staticmethod
    async def copy_s3_bucket_files(key: str, source_bucket: str, destination_bucket: str, aws_access_key: str, aws_secret_key: str, context) -> Optional[bool]:
        try:
            s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
            copy_source = {'Bucket': source_bucket, 'Key': key}
            s3_client.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=key)
            context.logger.log(f"File {key} successfully copied to bucket {destination_bucket}")
            return True
        except ClientError as e:
            context.logger.log(f"Error occurred while copying file {key}: {e}")
            return False

    @staticmethod
    async def delete_s3_bucket_files(key: str, source_bucket: str, destination_bucket: str, aws_access_key: str, aws_secret_key: str, context) -> Optional[bool]:
        try:
            s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
            response = s3_client.delete_object(Bucket=source_bucket, Key=key)
            if response['ResponseMetadata']['HTTPStatusCode'] == 204:
                context.logger.log(f"File {key} successfully deleted from bucket {source_bucket}")
                return True
            else:
                context.logger.log(f"File {key} could not be deleted from bucket {source_bucket}")
                return False
        except ClientError as e:
            context.logger.log(f"Error occurred while deleting file {key}: {e}")
            return False

