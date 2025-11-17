import asyncio

from fastapi import FastAPI

from core.database import init_database
from api.incidents import router as incidents_router


def create_application() -> FastAPI:
    application = FastAPI(
        title="UCar Incident API",
        description="API для учета инцидентов в UCar",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    application.include_router(
        incidents_router,
        prefix="/api/v1/incidents",
        tags=["incidents"],
    )

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    await asyncio.sleep(5)
    init_database()


@app.get("/")
async def root():
    return {"message": "UCar Incident API Service"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}