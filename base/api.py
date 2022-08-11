
import json
import os
from typing import List
from django.http import FileResponse, HttpRequest, HttpResponse
from ninja import Form, NinjaAPI, Schema, File
from ninja.files import UploadedFile
from django.core.files.storage import FileSystemStorage
from ninja.renderers import BaseRenderer
from django.contrib.auth.hashers import make_password, check_password
from medias.models import MyFiles, MyFileInfo
import mimetypes


class MyRenderer(BaseRenderer):
    # media_type = "image/png"

    def render(self, request, data, *, response_status):
        if data.get("file") and data.get("title"):
            file = data.get("file")
            title = data.get("title")
            file_type = file.split('.')[-1]
            file_path = os.getcwd()
            # fs = FileSystemStorage(file_path)
            mime_type = mimetypes.guess_type(title)
            print("mimetype", mime_type)
            if mime_type[0]:
                self.media_type = mime_type[0]
                print("my_mimeType", self.media_type)
            else:
                self.media_type = f"application/{file_type}+xml"
                print("my_mimeType", self.media_type)

            # return FileResponse(open(file[1:], 'rb'), content_type=file_type)
            return open(file[1:], 'rb')
        if data:
            return json.dumps({"title": data.get("title"), "image": data.get("file"), "type": data.get("file").split('.')[-1]})
        else:
            return json.dumps([])


api = NinjaAPI(csrf=False, title="api", urls_namespace="api")
download = NinjaAPI(csrf=False, renderer=MyRenderer(),
                    title="download", urls_namespace="download")


class OriginForm(Schema):
    origin: str
    user: str


@api.post('upload/file')
def single_file(request, form: OriginForm = Form(...), file: UploadedFile = File(None)):
    uploaded: MyFiles = MyFileInfo.get_or_create(file, form.origin, form.user)
    return {
        "file": 
            {
                "url":uploaded.get_url,
                "id":uploaded.pk
            }
    }


@api.post('upload/files')
def multiple_files(request: HttpRequest, form: OriginForm = Form(...), files: List[UploadedFile] = File(...)):
    urls = []
    for file in files:
        _file: MyFiles = MyFileInfo.get_or_create(file, form.origin, form.user)
        urls.append(
            {
                "url":_file.get_url,
                "id":_file.pk
            }
        )
        print("fileKey", _file.get_url)
    return {"files": urls}
#
@api.post('valid/file/{id}')
def valid_file(request:HttpRequest,id:int):
    files = MyFiles.objects.filter(pk=id)
    if files.exists():
        files.update(is_valid=True)
    return {"result":True}
    
@api.get("files")
def get_files(request):
    return list(MyFiles.objects.all().values())

@api.get('fileInfos')
def get_file_info(request):
    return list(MyFileInfo.objects.all().values())

@api.delete("file/{id}")
def remove_file(request,id:int):
    files = MyFiles.objects.filter(pk=id)
    for file in files:
        file.delete()
    return

@api.delete("files")
def remove_all_files(request):
    files = MyFiles.objects.all()
    for file in files:
        file.delete()

class FileOut(Schema):
    title: str
    file: str


@download.get('file/{id}', response=FileOut)
def download_file(request, id: str):
    fileInfo: MyFileInfo = MyFileInfo.objects.get(key=id)
    print("fileInfo", fileInfo.file.file)
    return fileInfo.file
