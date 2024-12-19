from fastapi import FastAPI
from src.api import router 

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(router)
