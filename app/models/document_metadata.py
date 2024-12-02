from pydantic import BaseModel
from typing import Dict

class DocumentMetadata(BaseModel):
    url: str
    title: str

class DocumentsConfig(BaseModel):
    documents: Dict[str, DocumentMetadata]