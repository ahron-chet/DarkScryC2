from ninja import Schema
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class FileModel(BaseModel):
    Name: str = Field(..., description="File name with extension")
    Icon: str = Field(..., description="Base64 encoded file icon")
    Size: int = Field(..., ge=0, description="Size of the file in bytes")
    LastWriteTimeUtc: datetime = Field(..., description="Last modified time in UTC")
    CreationTimeUtc: datetime = Field(..., description="File creation time in UTC")
    Path: str = Field(..., description="Full file path")

class DirectoriesModel(BaseModel):
    Items: List[str] = Field(..., description="List of directory paths")

class FileExplorerStreamResponde(BaseModel):
    Files: List[FileModel] = Field(..., description="List of files in the directory")
    Directories: DirectoriesModel = Field(..., description="Nested directories structure")
    RootPath: str = Field(..., description="Root path of the directory")


class GetFileBase64Responde(Schema):
    file_base64: str = Field(..., description="Base64 string of the requested file.")


class FileCollectionRequest(Schema):
    path: str

class UploadBase64FileRequest(FileCollectionRequest):
    file_base64: str = Field(..., description="Base64 string of the requested file.")
    file_name: str = Field(..., description="Base64 string of the requested file.")
