from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from client_site.pages.router import router as router_pages


app = FastAPI()
app.mount('/static', StaticFiles(directory='client_site/static'), 'static')


@app.get("/")
def home_page():
    return {"message": None}


app.include_router(router_pages)
