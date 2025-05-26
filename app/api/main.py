from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.appointments import router as appointment_router
from app.database.base import Base
from app.database.session import engine

app = FastAPI(title="Yandress Apointments API", version="0.1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # o lista de orígenes específicos, por ejemplo ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


for router in [appointment_router]:
    app.include_router(router)
