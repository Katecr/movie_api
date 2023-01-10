from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: Optional[int] = None
    title:str = Field(min_length=5,max_length=15)
    overview:str = Field(min_length=15,max_length=50)
    year:int = Field(gt=1900,le=2023)
    rating:float = Field(ge=1, le=10)
    category:str = Field(min_length=5,max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "title": "The Shawshank",
                "overview": "Descripción de la pelicula lorem",
                "year": 1994,
                "rating": 9.3,
                "category": "Drama",
            }
        }