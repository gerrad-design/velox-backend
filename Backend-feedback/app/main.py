from fastapi import FastAPI
from . import models
from .database import engine
from .routes import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Velox Feedback API",
    description="Submit feedback securely via JWT authentication.",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {"message": "Feedback API is running 🚀"}

app.include_router(router)
