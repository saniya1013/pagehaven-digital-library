from pydantic import BaseModel
from typing import List

class Book(BaseModel):
    title: str
    author: str
    category: List[str]
    description: str
    rating: float
    pdf_url: str