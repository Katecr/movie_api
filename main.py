from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi.security import HTTPBearer

from jwt_manager import create_token, validate_token

app = FastAPI()

# Cambiar el titulo de la documentación
app.title = 'API MY MOVIE'

# Cambiar la versión de la documentación
app.version = "0.0.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@mail.com":
            raise HTTPException(status=403, detail="Credenciales incorrectas")


class User(BaseModel):
    email:str
    password:str


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
                "id": 9999,
                "title": "The Shawshank Redemption",
                "overview": "Two imprisoned",
                "year": 1994,
                "rating": 9.3,
                "genre": "Drama",
            }
        }


#variable de peliculas
movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    }
]


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1 style=color:red> hola mundo </h1>')

@app.post('/login',tags=['auth'])
def login(user: User):
    if user.email == 'admin@mail.com' and user.password == 'admin':
        token:str = create_token(user.dict())
        return JSONResponse(status_code=200,content=token)

@app.get('/movies', tags=['movies'], response_model=List[Movie],status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200,content=movies)

@app.get('/movies/{id}', tags=['movies'],response_model= Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    movie = list(filter(lambda x: x['id'] == id,movies))
    return JSONResponse(content=movie) if len(movie) > 0 else JSONResponse(status_code=404,content=[])

@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    movie = list(filter(lambda x: x['category'] == category,movies))
    return JSONResponse(content=movie) if len(movie) > 0 else JSONResponse(tatus_code=404,content=[])

@app.post('/movies', tags=['movies'], response_model=dict,status_code=201)
def create_movie(movie:Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201,content={"message":"Se ha registrado la película"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict,status_code=200)
def update_movie(id:int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
    return JSONResponse(status_code=200,content={"message":"Se ha modificado la película"})
        
@app.delete('/movies/{id}', tags=['movies'], response_model=dict,status_code=200)
def delete_movie(id:int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
    return JSONResponse(status_code=200,content={"message":"Se ha eliminado la película"})
