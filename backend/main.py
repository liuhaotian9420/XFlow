from fastapi import FastAPI

app = FastAPI(title="xyf-competition-mvp API")

@app.get("/")
def root():
    return {"message": "xyf-competition-mvp backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
