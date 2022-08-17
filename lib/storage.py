import boto3
import uuid
from dotenv import load_dotenv
import os

load_dotenv()


class MyS3Client:
    def __init__(self):
        boto3_s3 = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )
        self.s3_client = boto3_s3
        self.bucket_name = os.environ.get("AWS_STORAGE_BUCKET_NAME")
        self.bucket_region = os.environ.get("AWS_REGION")

    def s3_upload_img(self, file):
        file_id = str(uuid.uuid4())
        extra_args = {
            "ContentType": file.content_type,
        }

        self.s3_client.upload_fileobj(
            file, self.bucket_name, file_id, ExtraArgs=extra_args
        )

        return f"https://{self.bucket_name}.s3.{self.bucket_region}.amazonaws.com/{file_id}"

    def s3_delete_img(self, img_name):
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=img_name)
