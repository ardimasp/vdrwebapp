from typing import List
from pydantic import BaseModel

class CreatedFolders(BaseModel):
    paths: List[str]

class DownloadedFiles(BaseModel):
    paths: List[str]

class DeletedFiles(BaseModel):
    paths: List[str]

class DeletedFolders(BaseModel):
    paths: List[str]