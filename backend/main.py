from fastapi import FastAPI

from backend.routers.tasks import router as tasks_router

app = FastAPI(title="xyf-competition-mvp API")
app.include_router(tasks_router)

@app.get("/")
def root():
    return {"message": "xyf-competition-mvp backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
