from fastapi import FastAPI
from src.api import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:8080", "http://localhost:5173"]
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(router)
