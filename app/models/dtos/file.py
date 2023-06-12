from fastapi import UploadFile

class FileDTO(UploadFile):
  file: UploadFile