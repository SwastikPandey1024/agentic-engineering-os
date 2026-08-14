from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.logging import setup_logging, RequestIDMiddleware

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Production service starting...")
    yield
    print("Production service stopped.")

app = FastAPI(title="Production Enterprise Service", version="1.0.0", lifespan=lifespan)
app.add_middleware(RequestIDMiddleware)

@app.get("/api/v1/health", tags=["system"])
def health_check():
    return {"status": "ok", "service": "production-service", "version": "1.0.0"}
