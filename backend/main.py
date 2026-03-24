from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.acp.factory import shutdown_providers
from backend.routers.chat import router as chat_router
from backend.routers.data import router as data_router
from backend.routers.skills import router as skills_router
from backend.routers.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await shutdown_providers()


app = FastAPI(title="xyf-competition-mvp API", lifespan=lifespan)
app.include_router(tasks_router)
app.include_router(chat_router)
app.include_router(data_router)
app.include_router(skills_router)


@app.get("/")
def root():
    return {"message": "xyf-competition-mvp backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
