from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.models import Foodstuff, InventoryItem  # noqa: F401 - imported so metadata includes models
from app.routers import foodstuffs, inventory


def build_lifespan(create_db_on_startup: bool):
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        if create_db_on_startup:
            Base.metadata.create_all(bind=engine)
        yield

    return lifespan


def create_app(create_db_on_startup: bool = True) -> FastAPI:
    app = FastAPI(title=settings.app_name, lifespan=build_lifespan(create_db_on_startup))
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(foodstuffs.router)
    app.include_router(inventory.router)
    return app


app = create_app()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
