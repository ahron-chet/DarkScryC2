from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class FileModel(BaseModel):
    """Metadata about a file on the agent."""

    name: str = Field(..., description="File name with extension")
    icon: str = Field(..., description="Base64 encoded file icon")
    size: int = Field(..., ge=0, description="Size of the file in bytes")
    last_write_time_utc: datetime = Field(..., description="Last modified time in UTC")
    creation_time_utc: datetime = Field(..., description="File creation time in UTC")
    path: str = Field(..., description="Full file path")


class DirectoriesModel(BaseModel):
    """Directory listing."""

    items: List[str] = Field(..., description="List of directory paths")


class FileExplorerStreamResponse(BaseModel):
    """Response for directory snapshot requests."""

    files: List[FileModel] = Field(..., description="List of files in the directory")
    directories: DirectoriesModel = Field(
        ..., description="Nested directories structure"
    )
    root_path: str = Field(..., description="Root path of the directory")


class FileCollectionRequest(BaseModel):
    """Path request payload."""

    path: str = Field(..., description="Path on the agent's filesystem")


class UploadBase64FileRequest(FileCollectionRequest):
    """Upload base64 encoded file to the agent."""

    file_base64: str = Field(..., description="Base64 string of the file contents")
    file_name: str = Field(..., description="Destination file name")
