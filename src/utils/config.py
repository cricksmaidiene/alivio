from pyprojroot import here

S3_BUCKET: str = "alivio"
BASE_DIR: str = str(here())
LOCAL_DATA_DIR: str = BASE_DIR + "/data"
S3_DATA_DIR: str = f"s3://{S3_BUCKET}/datasets"