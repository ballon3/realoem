from typing import List, Optional
from pydantic import BaseModel

class Part(BaseModel):
    set_id: int 
    url: str = None
    title: str = None
    img_url: str = None

class PartList(BaseModel):
    Parts: List[Part] = None

class ParNum(BaseModel):
    no: str
    description: str = None 
    supp: str = None 
    qty: str = None 
    date_from: str = None 
    date_to: str = None
    partnum: str = None 
    price: str = None 
