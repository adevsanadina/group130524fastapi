from pydantic import BaseModel
from datetime import datetime

class NewTour(BaseModel):
    title: str
    description: str
    price: float
    destination: str

class SavedTour(NewTour):
    id: int
    created_at: datetime

class TourPrice(BaseModel):
    price: float

class DeletedTour(BaseModel):
    id: int
