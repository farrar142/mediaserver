
from typing import List
from django.http import HttpRequest
from ninja import Form, NinjaAPI, Schema, File
from ninja.files import UploadedFile
from django.contrib.auth.hashers import make_password, check_password
from medias.models import MyFiles, MyFileInfo

api = NinjaAPI(csrf=False)


class OriginForm(Schema):
    origin: str


@api.post('upload/file')
def single_file(request, form: OriginForm = Form(...), file: UploadedFile = File(None)):
    uploaded: MyFileInfo = MyFileInfo.get_or_create(file, form.origin)
    return {"url": uploaded.key}


@api.post('upload/files')
def multiple_files(request: HttpRequest, form: OriginForm = Form(...), files: List[UploadedFile] = File(...)):
    urls = []
    for file in files:
        _file: MyFileInfo = MyFileInfo.get_or_create(file, form.origin)
        urls.append(_file.key)
        print(_file.key)
    return {"urls": urls}
#


@api.get('download/file/{id}')
def download_file(request, id: str):
    return ""
