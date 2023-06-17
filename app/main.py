from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import os,time


from config import settings
from router import auth, report, resources_access


app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(report.router, tags=['Report'], prefix='/api/report')
app.include_router(resources_access.router, tags=['Report'], prefix='/api/report')

