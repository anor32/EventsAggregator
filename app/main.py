from fastapi import FastAPI

from .enpoints import router

app = FastAPI()
app.include_router(router)
