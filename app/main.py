from fastapi import FastAPI
from app.users.router import router as router_users
from app.services.router import router as router_services
from app.incidents.router import router as router_incidents
from app.dialogs.router import router as router_dialogs
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home_page():
    return {"message": None}


app.include_router(router_users)
app.include_router(router_services)
app.include_router(router_incidents)
app.include_router(router_dialogs)
