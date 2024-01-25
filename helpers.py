# Import pandas
import pandas as pd
# Import boto3 to store csvs on AWS S3 bucket
import boto3
import botocore
import io
import os
# Import environment variables
from dotenv import load_dotenv

# AWS info
load_dotenv()
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    # aws_session_token=AWS_SESSION_TOKEN,
)

def save(df, name):
    with io.StringIO() as csv_buffer:
        df.to_csv(csv_buffer, index=False)

        response = s3_client.put_object(
            Bucket=AWS_S3_BUCKET, Key=name, Body=csv_buffer.getvalue()
        )

        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            print(f"Successful S3 put_object response. Status - {status}")
        else:
            print(f"Unsuccessful S3 put_object response. Status - {status}")
        
def load(name):
    response = s3_client.get_object(Bucket=AWS_S3_BUCKET, Key=name)

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"Successful S3 get_object response. Status - {status}")
        df = pd.read_csv(response.get("Body"))
    else:
        print(f"Unsuccessful S3 get_object response. Status - {status}")
        df = pd.DataFrame()    
    return df

def key_exists(name):
    try:
        s3_client.head_object(Bucket=AWS_S3_BUCKET, Key=name)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            # Something else has gone wrong.
            raise
    else:
        return True
    
def process_results(data):
  nested = []
  skip = ['challenges', 'textExtra', 'duetInfo', 'stickersOnItem', 'bitrateInfo', 'shareCover', 'volumeInfo', 'zoomCover', 'videoSuggestWordsList', 'effectStickers', 'subtitleInfos', 'warnInfo', 'poi']

  for id, value in data[0].items():
    if (type(value) is dict):
        nested.append(id)

  # Create blank dictionary
  flattened_data = {}

  # Loop through each video
  for idx, value in enumerate(data):
      flattened_data[idx] = {}
      # Loop through each value in each video
      for prop_idx, prop_value in value.items():
          # Check if contents
          if prop_idx == 'contents':
              flattened_data[idx]['desc'] = prop_value[0]['desc']
          # Check if skip
          elif prop_idx in skip:
              pass
          # Check if nested
          elif prop_idx in nested:
              # Loop through nested property
              for nested_idx, nested_value in prop_value.items():
                  if nested_idx not in skip:
                      flattened_data[idx][prop_idx + '_' + nested_idx] = nested_value
          # If not nested add to flattened dictionary
          else:
              flattened_data[idx][prop_idx] = prop_value
  
  return flattened_data

