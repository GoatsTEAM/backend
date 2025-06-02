from fastapi import FastAPI
from api.rest_handler import router as user_router

app = FastAPI()
app.include_router(user_router)
