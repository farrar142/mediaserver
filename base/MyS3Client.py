import os
import boto3
import uuid
import dotenv

dotenv.load_dotenv()
AWS_ACCESS_KEY = os.getenv('BOTO3_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv("BOTO3_ACCESS_KEY_PASSWORD")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
def sanitizer(url:str):
    if url.startswith('/'):
        return url[1:]
    else:
        return url

class MyS3Client:
    def __init__(self, access_key, secret_key, bucket_name):
        print(secret_key, access_key)
        boto3_s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        self.s3_client = boto3_s3
        self.bucket_name = bucket_name

    def upload(self, file, file_path):
        extra_args = {'ContentType': file.content_type}
        self.s3_client.upload_fileobj(
            file,
            self.bucket_name,
            file_path,
            # ExtraArgs=extra_args
        )
        return f'https://{self.bucket_name}.s3.ap-northeast-2.amazonaws.com/{file_path}'

    def upload_by_path(self, file):
        self.s3_client.upload_file(
            file,
            self.bucket_name,
            f"my/{file}",
            # ExtraArgs=extra_args
        )
        
    def delete_by_path(self,path):
        self.s3_client.delete_object(Bucket=self.bucket_name,Key=sanitizer(path))
        print("delete file at ",path)
        return True
        


# MyS3Client instance
s3_client = MyS3Client(AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET_NAME)


class FileUpload:
    def __init__(self, client):
        self.client: MyS3Client = client

    def upload(self, file, file_path):
        return self.client.upload(file, file_path)

    def upload_by_path(self, file):
        return self.client.upload_by_path(file)
    
    def delete_by_path(self,path):
        return self.client.delete_by_path(path)


file_upload = FileUpload(s3_client)
