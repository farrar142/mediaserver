import os
from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
import hashlib
import uuid
import boto3
import dotenv
from base.MyS3Client import file_upload

if getattr(settings, "USE_TZ", False):
    from django.utils.timezone import localtime as now
else:
    from django.utils.timezone import now

dotenv.load_dotenv()


def save_directory(origin, user, file):
    _now = now()
    year = _now.year
    month = _now.month
    day = _now.day
    # return "media/{0}/{1}/{2}/{3}/{4}".format(origin, year, month, day, file.name)
    return f"{os.getenv('MEDIA_PATH','media')}/{origin}/{user}/{str(uuid.uuid1())}"


class MyFiles(models.Model):
    title = models.TextField(default='')
    # file = models.FileField(upload_to=save_directory, null=True)
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    file_path = models.CharField('파일경로', max_length=256)
    file_url = models.CharField("파일URL", max_length=256)
    origin = models.CharField("출처", max_length=100, default="default")
    is_valid = models.BooleanField("인증 완료됨", default=False)
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('BOTO3_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv("BOTO3_ACCESS_KEY_PASSWORD")
    )

    @property
    def get_url(self):
        return self.file_path

    @classmethod
    def create(cls, file, origin, user):
        file_path = save_directory(origin, user, file)
        file_url = file_upload.upload(file, file_path)
        print(file_url)

        uploaded: MyFiles = MyFiles.objects.create(
            origin=origin,
            title=file.name, file_path=file_path, file_url=file_url)
        return uploaded

    def delete(self, using=None, keep_parents=False):
        file_upload.delete_by_path(self.file_path)
        return super().delete(using=None, keep_parents=False)


class MyFileInfo(models.Model):
    name = models.CharField("파일이름", max_length=500)
    size = models.IntegerField("파일사이즈")
    key = models.CharField("파일 키", max_length=128)
    file = models.ForeignKey(MyFiles, on_delete=models.CASCADE)

    @classmethod
    def part_hash(cls, key):
        data = key.encode()
        hash_object = hashlib.sha256()
        hash_object.update(data)
        hash_address = hash_object.hexdigest()
        return hash_address

    @classmethod
    def make_hash(cls, file):
        name_hash = cls.part_hash(file.name)
        size_hash = cls.part_hash(str(file.size))
        return name_hash+size_hash

    @classmethod
    def get_or_create(cls, file, origin="default", user="none"):
        fileInfo: MyFileInfo = cls.create(file, origin, user)
        return fileInfo.file
        #     return fileInfo.file
        # key = cls.make_hash(file)
        # print(key)
        # res = cls.objects.filter(key=key)
        # if res.exists():
        #     fileInfo: MyFileInfo = res.first()
        #     return fileInfo.file
        # else:
        #     fileInfo: MyFileInfo = cls.create(file, origin, user)
        #     return fileInfo.file

    @classmethod
    def create(cls, _file, origin, user):
        key = cls.make_hash(_file)
        file: MyFiles = MyFiles.create(_file, origin, user)
        info: MyFileInfo = cls.objects.create(
            file=file,
            name=_file.name, size=_file.size, key=key)
        return info
