from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
app = FastAPI(title="Python Service Template", version="0.1.0")

@app.get("/api/v1/health", tags=["system"])
def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}
