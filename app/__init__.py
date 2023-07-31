from decouple import config
from fastapi import FastAPI
from .router import router

OPENAI_API_KEY = config("OPENAI_API_KEY")


app = FastAPI()
app.include_router(router)
