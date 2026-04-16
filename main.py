import os
import sys

PROJECT_ROOT = os.path.dirname(__file__)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi import FastAPI
from database import Base, engine
from school.routers import school, score

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(school.router)
app.include_router(score.router)
