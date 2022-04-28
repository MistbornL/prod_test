import motor.motor_asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from beanie import init_beanie

from .config import settings
from prod.app.documents.document import User
from prod.app.router.test import router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(router)
    # app.mount("/ws", s_app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    async def startup_event():
        client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
        await init_beanie(database=client[settings.MONGODB_DATABASE_NAME],
                          document_models=[User])

    return app
