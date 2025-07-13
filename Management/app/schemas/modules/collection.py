from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class FileModel(BaseModel):
    """Metadata about a file on the agent."""

    name: str = Field(..., alias="Name", description="File name with extension")
    icon: str = Field(..., alias="Icon", description="Base64 encoded file icon")
    size: int = Field(..., alias="Size", ge=0, description="Size of the file in bytes")
    last_write_time_utc: datetime = Field(
        ..., alias="LastWriteTimeUtc", description="Last modified time in UTC"
    )
    creation_time_utc: datetime = Field(
        ..., alias="CreationTimeUtc", description="File creation time in UTC"
    )
    path: str = Field(..., alias="Path", description="Full file path")

    model_config = ConfigDict(populate_by_name=True)


class DirectoriesModel(BaseModel):
    """Directory listing."""

    items: List[str] = Field(..., alias="Items", description="List of directory paths")

    model_config = ConfigDict(populate_by_name=True)


class FileExplorerStreamResponse(BaseModel):
    """Response for directory snapshot requests."""

    files: List[FileModel] = Field(
        ..., alias="Files", description="List of files in the directory"
    )
    directories: DirectoriesModel = Field(
        ..., alias="Directories", description="Nested directories structure"
    )
    root_path: str = Field(
        ..., alias="RootPath", description="Root path of the directory"
    )

    model_config = ConfigDict(populate_by_name=True)


class FileCollectionRequest(BaseModel):
    """Path request payload."""

    path: str = Field(..., description="Path on the agent's filesystem")

    model_config = ConfigDict(populate_by_name=True)


class UploadBase64FileRequest(FileCollectionRequest):
    """Upload base64 encoded file to the agent."""

    file_base64: str = Field(..., description="Base64 string of the file contents")
    file_name: str = Field(..., description="Destination file name")
