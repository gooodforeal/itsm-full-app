from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.users.router import router as router_users
from app.services.router import router as router_services
from app.incidents.router import router as router_incidents
from app.dialogs.router import router as router_dialogs
from app.pages.router import router as router_pages


app = FastAPI()
app.mount('/static', StaticFiles(directory='app/static'), 'static')


@app.get("/")
def home_page():
    return {"message": None}


app.include_router(router_users)
app.include_router(router_services)
app.include_router(router_incidents)
app.include_router(router_dialogs)
app.include_router(router_pages)
