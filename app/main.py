from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.init_db import create_tables

from app.routers.users import router as users_router
from app.routers.venues import router as venues_router

create_tables()

app = FastAPI(
    title="ITicket API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(venues_router)
