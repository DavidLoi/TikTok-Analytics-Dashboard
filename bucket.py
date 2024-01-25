import logging
import boto3
from botocore.exceptions import ClientError

AWS_ACCESS_KEY_ID = # Insert key
AWS_SECRET_ACCESS_KEY = # Insert key

s3_client = boto3.client('s3', region_name = 'us-east-2',
                    aws_access_key_id = AWS_ACCESS_KEY_ID,
                    aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

location = {'LocationConstraint': 'us-west-2'} 

s3_client.create_bucket(Bucket = 'tiktok', # Here is the name of the bucket you just created
                                  CreateBucketConfiguration = location)

file_name = 'tiktok.py'
bucket_name = 'tiktokanalytics'
object_name = file_name #You can set your own object name or keep it the same as the original file name on the local machine.

with open(file_name, 'rb') as f:
    s3_client.upload_fileobj(f, bucket_name, object_name)
