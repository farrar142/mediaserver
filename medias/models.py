from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
import hashlib
import uuid
if getattr(settings, "USE_TZ", False):
    from django.utils.timezone import localtime as now
else:
    from django.utils.timezone import now


def save_directory(instance, filename):
    _now = now()
    year = _now.year
    month = _now.month
    day = _now.day
    return "{0}/{1}/{2}/{3}/{4}".format(instance.origin, year, month, day, filename)


class MyFiles(models.Model):
    title = models.TextField(default='')
    file = models.FileField(upload_to=save_directory, null=True)
    origin = models.CharField("출처", max_length=100, default="default")

    @property
    def get_url(self):
        return self.file.url

    @classmethod
    def create(cls, file, origin):
        uploaded: MyFiles = MyFiles.objects.create(
            origin=origin,
            title=file.name, file=file)
        return uploaded


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
    def get_or_create(cls, file, origin="default"):
        key = cls.make_hash(file)
        print(key)
        res = cls.objects.filter(key=key)
        if res.exists():
            fileInfo: MyFileInfo = res.first()
            return fileInfo.file
        else:
            fileInfo: MyFileInfo = cls.create(file, origin)
            return fileInfo.file

    @classmethod
    def create(cls, _file, origin):
        key = cls.make_hash(_file)
        file: MyFiles = MyFiles.create(_file, origin)
        info: MyFileInfo = cls.objects.create(
            file=file,
            name=_file.name, size=_file.size, key=key)
        return info
