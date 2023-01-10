from fastapi import FastAPI
from fastapi.responses import HTMLResponse


from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()

# Cambiar el titulo de la documentación
app.title = 'API MY MOVIE'

# Cambiar la versión de la documentación
app.version = "0.0.1"

# Middleware de error
app.add_middleware(ErrorHandler)

#Routers
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)




@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1 style=color:red> hola mundo </h1>')




