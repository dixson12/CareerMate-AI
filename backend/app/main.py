from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

from app.routers import upload, chat, resume, visa


app = FastAPI(
    title=settings.app_name,
    docs_url=None,      # disables /docs
    redoc_url=None,      # disables /redoc
)
app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(resume.router)
app.include_router(visa.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://careermate-frontend.livelywater-d53e09d2.switzerlandnorth.azurecontainerapps.io",
        "http://localhost:8501",  # keep for local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}